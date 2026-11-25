import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import backhaul_formation_utils
from packet_analyzer.ieee1905_utils import MSG_TYPE_TOPOLOGY_DISCOVERY, MSG_TYPE_AP_AUTOCONFIG_SEARCH
from packet_analyzer import packet_dissector
from rdkbmeshzap.common_utils import device_utils, report_logger, recovery_utils

def test_backhaul_wireless_formation_linktype(initialize):
    """
    Verify every enabled Agent forms a wireless backhaul to the Controller after reboot.
    """
    report_logger.print_test("Entering test_backhaul_wireless_formation_linktype")
    capture_name = None
    try:
        # Pick the Agents under test.
        report_logger.print_step("STEP 1: Get the enabled Agents")
        agents = device_utils.get_enabled_extenders(initialize)
        if not agents:
            report_logger.print_error("FAIL: No enabled Extenders found in infra.yaml")
            return
        report_logger.print_success(f"PASS: Agents under test: {agents}")

        # Reboot each Agent and wait for it to recover within the KPI.
        report_logger.print_step("STEP 2: Reboot the Agents")
        reboot_time = initialize.get_time_stamp("controller")
        # Start one recovery timer, then reboot all Agents at once.
        started_at = time.monotonic()
        reboot_errors = {}
        with ThreadPoolExecutor(max_workers=len(agents)) as executor:
            reboot_futures = {executor.submit(initialize.reboot_device, agent, method="cli"): agent for agent in agents}
            for future in as_completed(reboot_futures):
                try:
                    future.result()
                except Exception as error:
                    reboot_errors[reboot_futures[future]] = error
        for agent in agents:
            if agent in reboot_errors:
                report_logger.print_error(f"FAIL: {agent}: reboot command failed: {reboot_errors[agent]}")
            else:
                report_logger.print_info(f"INFO: Reboot command executed for {agent}")

        # Start the Controller capture after the reboot, as in the Agent_Recovery tests.
        report_logger.print_step("STEP 3: Start packet capture on the Controller and wait for Agent recovery")
        capture_name = device_utils.start_capture(initialize, "controller", "test_backhaul_wireless_formation_linktype", step="3", include_device=True)

        # Recover the rebooted Agents in parallel within the KPI.
        results = {}
        threads = []
        for agent in agents:
            if agent in reboot_errors:
                continue
            thread = threading.Thread(target=recovery_utils.recover_device, kwargs={"initialize": initialize, "device": agent, "started_at": started_at, "results": results, "recovery_type": "agent"}, name=f"recover-{agent}")
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        recovered = []
        for agent in agents:
            result = results.get(agent)
            if isinstance(result, BaseException) or result is False or result is None:
                report_logger.print_error(f"FAIL: {agent} did not recover within the KPI")
                continue
            report_logger.print_success(f"PASS: {agent} recovered in {result:.1f}s")
            recovered.append(agent)
        # Poll each backhaul link until it is connected, then check BSSID and SSID.
        report_logger.print_step("STEP 4: Verify wireless backhaul association")
        expected_ssid = initialize.read_from_database("controller", "mesh_backhaul_ssid")
        connected_agents = []
        backhaul_ifaces = {}
        for agent in recovered:
            backhaul_iface = initialize.read_from_database(agent, "backhaul_interface")
            backhaul_ifaces[agent] = backhaul_iface
            report_logger.print_info(f"INFO: {agent} backhaul interface: {backhaul_iface}; expected SSID: {expected_ssid}")
            connected = False
            deadline = time.monotonic() + backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS
            while time.monotonic() < deadline:
                if initialize.get_wireless_backhaul_connection_status(agent, interface=backhaul_iface):
                    connected = True
                    break
                report_logger.print_info(f"INFO: {agent} {backhaul_iface} is not connected yet")
                time.sleep(backhaul_formation_utils.POLL_INTERVAL_SECONDS)
            if not connected:
                report_logger.print_error(f"FAIL: {agent} {backhaul_iface} did not connect within {backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS}s")
                continue
            report_logger.print_info(f"INFO: {agent} {backhaul_iface} is connected")
            connected_agents.append(agent)
            bssids = [bssid for bssid in initialize.get_iw_link_details(agent, backhaul_iface, "bssid") if backhaul_formation_utils.MAC_PATTERN.match(bssid)]
            if not bssids:
                report_logger.print_error(f"FAIL: {agent} reported no valid BSSID on {backhaul_iface}")
            ssids = initialize.get_iw_link_details(agent, backhaul_iface, "ssid")
            if expected_ssid not in ssids:
                report_logger.print_error(f"FAIL: {agent} backhaul SSID is {ssids}, expected {expected_ssid}")
            if bssids and expected_ssid in ssids:
                report_logger.print_success(f"PASS: {agent} is connected to BSSID {bssids[0]} with SSID {expected_ssid}")

        # The Controller AL MAC must be learned on the wireless backhaul port, not a wired one.
        report_logger.print_step("STEP 5: Verify the backhaul link type is wireless")
        controller_al_mac = initialize.get_al_mac_address("controller", "cli")
        report_logger.print_info(f"INFO: Controller AL MAC: {controller_al_mac}")
        for agent in connected_agents:
            try:
                port = initialize.get_bridge_fdb_port(agent, controller_al_mac)
            except Exception as error:
                port = None
                report_logger.print_error(f"FAIL: {agent}: Controller AL MAC is not learned on any port: {error}")
            if port == backhaul_ifaces[agent]:
                report_logger.print_success(f"PASS: {agent}: Controller AL MAC is learned on wireless backhaul {port}")
            elif port:
                report_logger.print_error(f"FAIL: {agent}: Controller AL MAC is learned on {port}, expected {backhaul_ifaces[agent]}")

        # Let topology messages settle, then collect the capture taken since the reboot.
        report_logger.print_step("STEP 6: Validate IEEE 1905 messages in the Controller capture")
        report_logger.print_info(f"INFO: Waiting {backhaul_formation_utils.ONBOARDING_SETTLE_SECONDS}s for topology messages")
        time.sleep(backhaul_formation_utils.ONBOARDING_SETTLE_SECONDS)
        capture_path = device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
        capture_name = None
        report_logger.print_info(f"INFO: Controller capture collected at {capture_path}")
        # Keep only packets seen after the first reboot and check each Agent's messages.
        packets = [pkt for pkt in packet_dissector.reassemble_packets(capture_path) if pkt.time >= reboot_time]
        report_logger.print_info(f"INFO: Packets after reboot: {len(packets)}")
        for agent in recovered:
            agent_al_mac = initialize.get_al_mac_address(agent, "cli")
            report_logger.print_info(f"INFO: {agent} AL MAC: {agent_al_mac}")
            # Discovery messages from an Agent behind another Agent do not reach the Controller capture, so check only direct Agents.
            parent, _ = device_utils.get_extender_parent_device(initialize, agent, ["controller", *agents])
            if parent == "controller":
                all_found = True
                for message_type, message_name in ((MSG_TYPE_TOPOLOGY_DISCOVERY, "Topology Discovery"), (MSG_TYPE_AP_AUTOCONFIG_SEARCH, "AP Autoconfig Search")):
                    if packet_dissector.check_message_presence(packets, message_type, src_mac=agent_al_mac):
                        report_logger.print_info(f"INFO: {message_name} from {agent} ({agent_al_mac}) was found in the capture")
                    else:
                        all_found = False
                        report_logger.print_error(f"FAIL: {message_name} from {agent} ({agent_al_mac}) was not found in the capture")
                if all_found:
                    report_logger.print_success(f"PASS: Topology Discovery and AP Autoconfig Search from {agent} ({agent_al_mac}) were found in the capture")
            else:
                report_logger.print_info(f"INFO: {agent} is connected through {parent}, Topology Discovery and AP Autoconfig Search are not checked in the Controller capture")
            recovery_utils.validate_topology_capture(packets, agent, agent_al_mac)
    finally:
        # Stop the capture if the test ended before STEP 6 collected it.
        if capture_name:
            try:
                device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
            except Exception as error:
                report_logger.print_error(f"FAIL: Could not stop Controller capture during cleanup: {error}")
        report_logger.print_test("Exiting test_backhaul_wireless_formation_linktype")
