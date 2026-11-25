import re
import time
import backhaul_formation_utils
from packet_analyzer.ieee1905_utils import MSG_TYPE_TOPOLOGY_DISCOVERY, MSG_TYPE_TOPOLOGY_NOTIFICATION, MSG_TYPE_AP_TOPOLOGY_RESPONSE, MSG_TYPE_AP_AUTOCONFIGURATION_WSC
from packet_analyzer import packet_dissector
from rdkbmeshzap.common_utils import device_utils, report_logger

def test_backhaul_wireless_formation_negative_invalidcredentials(initialize):
    """
    Verify the Agent does not form the wireless backhaul when its backhaul passphrase is invalid.
    """
    report_logger.print_test("Entering test_backhaul_wireless_formation_negative_invalidcredentials")
    capture_name = None
    config_changed = False
    agent = None
    try:
        # Pick the Agent, confirm its backhaul is up and that the Controller can ping it before any change.
        report_logger.print_step("STEP 1: Verify the Agent is connected and reachable from the Controller")
        agents = device_utils.get_enabled_extenders(initialize)
        if not agents:
            report_logger.print_error("FAIL: No enabled Extenders found in infra.yaml")
            return
        agent = agents[0]
        backhaul_iface = initialize.read_from_database(agent, "backhaul_interface")
        agent_ip = initialize.read_from_database(agent, "bridge_ip")
        if not initialize.get_wireless_backhaul_connection_status(agent, interface=backhaul_iface):
            report_logger.print_error(f"FAIL: {agent} {backhaul_iface} is not connected before the test")
            return
        report_logger.print_success(f"PASS: {agent} {backhaul_iface} is connected")
        # initialize.ping_ipv4 cannot be used because the Controller has no data_iface.
        output = initialize.execute_command("controller", f"ping -4 -c {backhaul_formation_utils.PING_COUNT} -W 2 {agent_ip}")
        match = re.search(r"(\d+(?:\.\d+)?)% packet loss", str(output))
        if not match:
            report_logger.print_error(f"FAIL: Packet loss not found in the ping output: {str(output).strip()!r}")
            return
        if float(match.group(1)) >= 100:
            report_logger.print_error(f"FAIL: {agent} ({agent_ip}) is not reachable from the Controller before the test")
            return
        report_logger.print_success(f"PASS: {agent} ({agent_ip}) is reachable from the Controller")

        # Start the Controller capture (prints the STEP 2 heading) to record the 1905 traffic.
        capture_name = device_utils.start_capture(initialize, "controller", "test_backhaul_wireless_formation_negative_invalidcredentials", step="2", include_device=True)

        # Back up the config, set the invalid passphrase and reboot the Agent. Then wait for the link to drop and the Agent to boot.
        report_logger.print_step("STEP 3: Set an invalid backhaul passphrase on the Agent and reboot it")
        agent_al_mac = initialize.get_al_mac_address(agent, "cli")
        controller_al_mac = initialize.get_al_mac_address("controller", "cli")
        # Back up the config and continue only if the backup holds the passphrase key.
        config = backhaul_formation_utils.AGENT_BACKHAUL_CONFIG
        backup_config = backhaul_formation_utils.AGENT_BACKHAUL_CONFIG_BACKUP
        backup = initialize.execute_command(agent, f"cp -f {config} {backup_config} && sync && grep -c Backhaul_KeyPassphrase {backup_config}")
        if str(backup).strip().splitlines()[-1:] != ["1"]:
            report_logger.print_error(f"FAIL: Could not back up the backhaul config on {agent}")
            return
        # Replace the Backhaul_KeyPassphrase value with the invalid passphrase and check it was written.
        pattern = r'\("Backhaul_KeyPassphrase"[[:space:]]*:[[:space:]]*"\)\([^"\\]\|\\.\)*"'
        replacement = r"\1" + backhaul_formation_utils.INVALID_PASSPHRASE + '"'
        initialize.execute_command(agent, "sed -i 's/" + pattern + "/" + replacement + "/' " + config + " && sync")
        applied = initialize.execute_command(agent, f"grep -c {backhaul_formation_utils.INVALID_PASSPHRASE} {config}")
        if str(applied).strip().splitlines()[-1:] != ["1"]:
            report_logger.print_error(f"FAIL: Could not set the invalid passphrase on {agent}")
            return
        config_changed = True
        report_logger.print_success(f"PASS: Invalid backhaul passphrase set on {agent}")
        initialize.reboot_device(agent, method="cli")
        # Poll the Agent until it stops answering, which means the old backhaul is gone.
        link_down = False
        deadline = time.monotonic() + backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            output = initialize.execute_command("controller", f"ping -4 -c {backhaul_formation_utils.PING_COUNT} -W 2 {agent_ip}")
            match = re.search(r"(\d+(?:\.\d+)?)% packet loss", str(output))
            if not match:
                report_logger.print_error(f"FAIL: Packet loss not found in the ping output: {str(output).strip()!r}")
                return
            if float(match.group(1)) >= 100:
                link_down = True
                break
            time.sleep(backhaul_formation_utils.POLL_INTERVAL_SECONDS)
        if not link_down:
            report_logger.print_error(f"FAIL: {agent} did not go down within {backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS}s of the reboot")
            return
        report_logger.print_success(f"PASS: {agent} is down after the reboot")
        # Give the Agent time to boot and try the invalid credentials, then start the observation window.
        time.sleep(backhaul_formation_utils.ONBOARDING_SETTLE_SECONDS)
        observation_start = initialize.get_time_stamp("controller")

        # Ping the Agent for the whole window, every ping must be lost.
        report_logger.print_step(f"STEP 4: Verify the Agent stays unreachable for {backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS}s")
        losses = []
        started = time.monotonic()
        while time.monotonic() - started < backhaul_formation_utils.ONBOARDING_TIMEOUT_SECONDS:
            output = initialize.execute_command("controller", f"ping -4 -c {backhaul_formation_utils.PING_COUNT} -W 2 {agent_ip}")
            match = re.search(r"(\d+(?:\.\d+)?)% packet loss", str(output))
            if not match:
                report_logger.print_error(f"FAIL: Packet loss not found in the ping output: {str(output).strip()!r}")
                return
            losses.append(float(match.group(1)))
            time.sleep(backhaul_formation_utils.POLL_INTERVAL_SECONDS)
        replied = [loss for loss in losses if loss < 100]
        if replied:
            report_logger.print_error(f"FAIL: {agent} answered {len(replied)} of {len(losses)} pings during the observation")
        else:
            report_logger.print_success(f"PASS: {agent} did not answer any of the {len(losses)} pings")

        # Stop the capture and collect it.
        report_logger.print_step("STEP 5: Stop the Controller capture")
        capture_path = device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
        capture_name = None
        report_logger.print_success(f"PASS: Controller capture collected at {capture_path}")

        # Keep only the observation window. The Controller must still send Topology Discovery and no onboarding or topology exchange may involve the Agent.
        report_logger.print_step("STEP 6: Validate the IEEE 1905 messages in the Controller capture")
        packets = [pkt for pkt in packet_dissector.reassemble_packets(capture_path) if pkt.time >= observation_start]
        if packet_dissector.check_message_presence(packets, MSG_TYPE_TOPOLOGY_DISCOVERY, src_mac=controller_al_mac):
            report_logger.print_success(f"PASS: Topology Discovery from {controller_al_mac} was found in the capture")
        else:
            report_logger.print_error(f"FAIL: Topology Discovery from {controller_al_mac} was not found, the capture is not valid")
        for message_type, message_name, src_mac, dst_mac in (
            (MSG_TYPE_AP_AUTOCONFIGURATION_WSC, "AP Autoconfiguration WSC", controller_al_mac, agent_al_mac),
            (MSG_TYPE_AP_TOPOLOGY_RESPONSE, "Topology Response", agent_al_mac, controller_al_mac),
            (MSG_TYPE_TOPOLOGY_DISCOVERY, "Topology Discovery", agent_al_mac, None),
            (MSG_TYPE_TOPOLOGY_NOTIFICATION, "Topology Notification", agent_al_mac, None),
        ):
            if packet_dissector.check_message_presence(packets, message_type, src_mac=src_mac, dst_mac=dst_mac):
                report_logger.print_error(f"FAIL: {message_name} from {src_mac} was found in the capture")
            else:
                report_logger.print_success(f"PASS: {message_name} from {src_mac} was not found in the capture")
    finally:
        # Stop the capture if the test ended before STEP 5 collected it.
        if capture_name:
            try:
                device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
            except Exception as error:
                report_logger.print_error(f"FAIL: Could not stop Controller capture during cleanup: {error}")
        # The Agent is unreachable with the invalid passphrase, so the valid credentials must be restored manually.
        if config_changed:
            report_logger.print_info(f"INFO: Restore {agent} manually: cp -f {backhaul_formation_utils.AGENT_BACKHAUL_CONFIG_BACKUP} {backhaul_formation_utils.AGENT_BACKHAUL_CONFIG} && sync; reboot")
        report_logger.print_test("Exiting test_backhaul_wireless_formation_negative_invalidcredentials")
