import time
import backhaul_formation_utils
from packet_analyzer.ieee1905_utils import MSG_TYPE_TOPOLOGY_DISCOVERY, MSG_TYPE_TOPOLOGY_NOTIFICATION, MSG_TYPE_AP_TOPOLOGY_RESPONSE, MSG_TYPE_AP_AUTOCONFIGURATION_WSC
from packet_analyzer import packet_dissector
from rdkbmeshzap.common_utils import device_utils, report_logger

def test_backhaul_wireless_formation_negative_invalidcredentials(initialize):
    """
    Verify no Agent forms the wireless backhaul when its backhaul passphrase is invalid.
    """
    report_logger.print_test("Entering test_backhaul_wireless_formation_negative_invalidcredentials")
    capture_name = None
    changed_agents = []
    try:
        # Pick the Agents, confirm each backhaul is up and that the Controller can ping it before any change.
        report_logger.print_step("STEP 1: Verify the Agents are connected and reachable from the Controller")
        agents = device_utils.get_enabled_extenders(initialize)
        if not agents:
            report_logger.print_error("FAIL: No enabled Extenders found in infra.yaml")
            return
        agent_ips = {}
        ready = True
        for agent in agents:
            backhaul_iface = initialize.read_from_database(agent, "backhaul_interface")
            agent_ips[agent] = initialize.read_from_database(agent, "bridge_ip")
            if not initialize.get_wireless_backhaul_connection_status(agent, interface=backhaul_iface):
                report_logger.print_error(f"FAIL: {agent} {backhaul_iface} is not connected before the test")
                ready = False
                continue
            report_logger.print_info(f"INFO: {agent} {backhaul_iface} is connected")
            loss = backhaul_formation_utils.get_packet_loss(initialize, "controller", agent_ips[agent])
            if loss is None or loss >= 100:
                report_logger.print_error(f"FAIL: {agent} ({agent_ips[agent]}) is not reachable from the Controller before the test")
                ready = False
                continue
            report_logger.print_success(f"PASS: {agent} is connected on {backhaul_iface} and reachable from the Controller at {agent_ips[agent]}")
        if not ready:
            return

        # Start the Controller capture to record the 1905 traffic.
        capture_name = device_utils.start_capture(initialize, "controller", "test_backhaul_wireless_formation_negative_invalidcredentials", step="2", include_device=True)

        # Back up the config, set the invalid passphrase and reboot each Agent.
        report_logger.print_step("STEP 3: Set an invalid backhaul passphrase on the Agents and reboot them")
        agent_al_macs = {agent: initialize.get_al_mac_address(agent, "cli") for agent in agents}
        controller_al_mac = initialize.get_al_mac_address("controller", "cli")
        for agent in agents:
            # Record the Agent first so the manual restore message is printed even if the update fails part way.
            changed_agents.append(agent)
            if not backhaul_formation_utils.set_invalid_backhaul_passphrase(initialize, agent):
                return

        # Reboot all Agents at once and verify none of them comes back.
        report_logger.print_step("STEP 4: Reboot the Agents and verify they go down")
        if not backhaul_formation_utils.reboot_and_verify_down(initialize, agents, agent_ips):
            return
        # Give the Agents time to boot and try the invalid credentials, then start the observation window.
        time.sleep(backhaul_formation_utils.ONBOARDING_SETTLE_SECONDS)
        observation_start = initialize.get_time_stamp("controller")

        # Ping every Agent for the whole window, every ping must be lost.
        report_logger.print_step(f"STEP 5: Verify the Agents stay unreachable for {backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS}s")
        losses = {agent: [] for agent in agents}
        started = time.monotonic()
        while time.monotonic() - started < backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS:
            for agent in agents:
                loss = backhaul_formation_utils.get_packet_loss(initialize, "controller", agent_ips[agent])
                if loss is None:
                    return
                losses[agent].append(loss)
            time.sleep(backhaul_formation_utils.POLL_INTERVAL_SECONDS)
        for agent in agents:
            replied = [loss for loss in losses[agent] if loss < 100]
            if replied:
                report_logger.print_error(f"FAIL: {agent} answered {len(replied)} of {len(losses[agent])} pings during the observation")
            else:
                report_logger.print_success(f"PASS: {agent} did not answer any of the {len(losses[agent])} pings")

        # Stop the capture and collect it.
        report_logger.print_step("STEP 6: Stop the Controller capture")
        capture_path = device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
        capture_name = None
        report_logger.print_success(f"PASS: Controller capture collected at {capture_path}")

        # Keep only the observation window. The Controller must still send Topology Discovery and no onboarding or topology exchange may involve any Agent.
        report_logger.print_step("STEP 7: Validate the IEEE 1905 messages in the Controller capture")
        packets = [pkt for pkt in packet_dissector.reassemble_packets(capture_path) if pkt.time >= observation_start]
        if packet_dissector.check_message_presence(packets, MSG_TYPE_TOPOLOGY_DISCOVERY, src_mac=controller_al_mac):
            report_logger.print_info(f"INFO: Topology Discovery from controller ({controller_al_mac}) was found in the capture")
        else:
            report_logger.print_error(f"FAIL: Topology Discovery from controller ({controller_al_mac}) was not found, the capture is not valid")
        for agent in agents:
            agent_al_mac = agent_al_macs[agent]
            none_found = True
            for message_type, message_name, src_device, src_mac, dst_mac in (
                (MSG_TYPE_AP_AUTOCONFIGURATION_WSC, "AP Autoconfiguration WSC", "controller", controller_al_mac, agent_al_mac),
                (MSG_TYPE_AP_TOPOLOGY_RESPONSE, "Topology Response", agent, agent_al_mac, controller_al_mac),
                (MSG_TYPE_TOPOLOGY_DISCOVERY, "Topology Discovery", agent, agent_al_mac, None),
                (MSG_TYPE_TOPOLOGY_NOTIFICATION, "Topology Notification", agent, agent_al_mac, None),
            ):
                if packet_dissector.check_message_presence(packets, message_type, src_mac=src_mac, dst_mac=dst_mac):
                    none_found = False
                    report_logger.print_error(f"FAIL: {message_name} from {src_device} ({src_mac}) was found in the capture")
                else:
                    report_logger.print_info(f"INFO: {message_name} from {src_device} ({src_mac}) was not found in the capture")
            if none_found:
                report_logger.print_success(f"PASS: No onboarding or topology messages involving {agent} ({agent_al_mac}) were found in the capture")
    finally:
        # Stop the capture if the test ended before STEP 6 collected it.
        if capture_name:
            try:
                device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
            except Exception as error:
                report_logger.print_error(f"FAIL: Could not stop Controller capture during cleanup: {error}")
        # The Agents are unreachable with the invalid passphrase, so the valid credentials must be restored manually.
        for agent in changed_agents:
            report_logger.print_info(f"INFO: Restore {agent} manually: cp -f {backhaul_formation_utils.AGENT_BACKHAUL_CONFIG_BACKUP} {backhaul_formation_utils.AGENT_BACKHAUL_CONFIG} && sync; reboot")
        report_logger.print_test("Exiting test_backhaul_wireless_formation_negative_invalidcredentials")
