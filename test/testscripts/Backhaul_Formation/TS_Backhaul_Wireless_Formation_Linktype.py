# If not stated otherwise in this file or this component LICENSE file the
# following copyright and licenses apply:
#
# Copyright 2026 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import backhaul_formation_utils
from zaero.utils import zi_logger
from packet_analyzer.ieee1905_utils import MSG_TYPE_TOPOLOGY_DISCOVERY, MSG_TYPE_AP_AUTOCONFIG_SEARCH
from packet_analyzer import packet_dissector
from rdkbmeshzap.common_utils import device_utils, report_logger, recovery_utils

def test_backhaul_wireless_formation_linktype(initialize):
    """
    Verify the Agent forms a wireless backhaul to the Controller after reboot.
    """
    report_logger.print_test("Entering test_backhaul_wireless_formation_linktype")
    capture_name = None
    try:
        # Start the Controller capture (prints the STEP 1 heading) and pick the Agent under test.
        capture_name = device_utils.start_capture(initialize, "controller", "test_backhaul_wireless_formation_linktype", step="1", include_device=True)
        agents = device_utils.get_enabled_extenders(initialize)
        if not agents:
            report_logger.print_error("FAIL: No enabled Extenders found in infra.yaml")
            return
        agent = agents[0]
        report_logger.print_success(f"PASS: Agent under test: {agent}")

        # Reboot the Agent and wait for it to recover within the KPI.
        report_logger.print_step("STEP 2: Reboot the Agent and wait for recovery")
        reboot_time = initialize.get_time_stamp("controller")
        initialize.reboot_device(agent, method="cli")
        report_logger.print_info(f"INFO: Reboot command executed for {agent}")
        results = {}
        recovery_utils.recover_device(initialize=initialize, device=agent, started_at=time.monotonic(), results=results, recovery_type="agent")
        result = results.get(agent)
        if isinstance(result, BaseException) or result is False or result is None:
            report_logger.print_error(f"FAIL: {agent} did not recover within the KPI")
            return
        report_logger.print_success(f"PASS: {agent} recovered in {result:.1f}s")
        # The SSH retries while the Agent rebooted are expected, so drop their zaero error logs.
        zi_logger.clear_error_logs()

        # Poll the backhaul link until it is connected, then check BSSID and SSID.
        report_logger.print_step("STEP 3: Verify wireless backhaul association")
        backhaul_iface = initialize.read_from_database(agent, "backhaul_interface")
        expected_ssid = initialize.read_from_database("controller", "mesh_backhaul_ssid")
        report_logger.print_info(f"INFO: Backhaul interface: {backhaul_iface}; expected SSID: {expected_ssid}")
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
            return
        report_logger.print_success(f"PASS: {agent} {backhaul_iface} is connected")
        bssids = [bssid for bssid in initialize.get_iw_link_details(agent, backhaul_iface, "bssid") if backhaul_formation_utils.MAC_PATTERN.match(bssid)]
        if bssids:
            report_logger.print_success(f"PASS: {agent} is connected to BSSID {bssids[0]}")
        else:
            report_logger.print_error(f"FAIL: {agent} reported no valid BSSID on {backhaul_iface}")
        ssids = initialize.get_iw_link_details(agent, backhaul_iface, "ssid")
        if expected_ssid in ssids:
            report_logger.print_success(f"PASS: {agent} backhaul SSID is {expected_ssid}")
        else:
            report_logger.print_error(f"FAIL: {agent} backhaul SSID is {ssids}, expected {expected_ssid}")

        # The Controller AL MAC must be learned on the wireless backhaul port, not a wired one.
        report_logger.print_step("STEP 4: Verify the backhaul link type is wireless")
        controller_al_mac = initialize.get_al_mac_address("controller", "cli")
        report_logger.print_info(f"INFO: Controller AL MAC: {controller_al_mac}")
        try:
            port = initialize.get_bridge_fdb_port(agent, controller_al_mac)
        except Exception as error:
            port = None
            report_logger.print_error(f"FAIL: {agent}: Controller AL MAC is not learned on any port: {error}")
        if port == backhaul_iface:
            report_logger.print_success(f"PASS: {agent}: Controller AL MAC is learned on wireless backhaul {port}")
        elif port:
            report_logger.print_error(f"FAIL: {agent}: Controller AL MAC is learned on {port}, expected {backhaul_iface}")

        # Let topology messages settle, then collect the capture taken since the reboot.
        report_logger.print_step("STEP 5: Validate IEEE 1905 messages in the Controller capture")
        report_logger.print_info(f"INFO: Waiting {backhaul_formation_utils.ONBOARDING_SETTLE_SECONDS}s for topology messages")
        time.sleep(backhaul_formation_utils.ONBOARDING_SETTLE_SECONDS)
        capture_path = device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
        capture_name = None
        report_logger.print_success(f"PASS: Controller capture collected at {capture_path}")
        # Keep only packets seen after the reboot and check the Agent's messages.
        packets = [pkt for pkt in packet_dissector.reassemble_packets(capture_path) if pkt.time >= reboot_time]
        agent_al_mac = initialize.get_al_mac_address(agent, "cli")
        report_logger.print_info(f"INFO: {agent} AL MAC: {agent_al_mac}; packets after reboot: {len(packets)}")
        for message_type, message_name in ((MSG_TYPE_TOPOLOGY_DISCOVERY, "Topology Discovery"), (MSG_TYPE_AP_AUTOCONFIG_SEARCH, "AP Autoconfig Search")):
            if packet_dissector.check_message_presence(packets, message_type, src_mac=agent_al_mac):
                report_logger.print_success(f"PASS: {message_name} from {agent_al_mac} was found in the capture")
            else:
                report_logger.print_error(f"FAIL: {message_name} from {agent_al_mac} was not found in the capture")
        recovery_utils.validate_topology_capture(packets, agent, agent_al_mac)
    finally:
        # Stop the capture if the test ended before STEP 5 collected it.
        if capture_name:
            try:
                device_utils.stop_and_collect_capture(initialize, "controller", capture_name)
            except Exception as error:
                report_logger.print_error(f"FAIL: Could not stop Controller capture during cleanup: {error}")
        report_logger.print_test("Exiting test_backhaul_wireless_formation_linktype")
