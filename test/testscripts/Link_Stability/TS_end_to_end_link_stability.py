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
from rdkbmeshzap.common_utils import client_utils, device_utils, report_logger
from rdkbmeshzap.common_utils.link_stability_utils import *

def test_em_end_to_end_link_performance_stability(initialize):
    """
    Verify end-to-end throughput, latency, and packet-loss stability between WLAN clients and the Controller.
    """
    report_logger.print_test("Entering test_em_end_to_end_link_performance_stability")
    try:
        present_clients = device_utils.get_enabled_clients(initialize)
        present_extenders = set(device_utils.get_enabled_extenders(initialize))
        clients = [
            client
            for client in present_clients
            if client.rsplit("_wlan_client_", 1)[0] in present_extenders]
        if not clients:
            report_logger.print_error("No WLAN clients owned by present extenders are available for end-to-end validation")
            return
        report_logger.print_step("STEP 1: Connect enabled WLAN clients before stability monitoring")
        try:
            ssid, password = initialize.get_fronthaul_credentials("controller")
        except Exception as err:
            report_logger.print_error(f"Unable to retrieve WLAN credentials: {err}")
            return
        connected_clients = []
        for client in clients:
            if client_utils.remove_and_connect_client(initialize, client, ssid, password):
                connected_clients.append(client)
            else:
                report_logger.print_error(f"{client}: unable to connect to the EasyMesh SSID")
        clients = connected_clients
        if not clients:
            report_logger.print_error("No extender-owned WLAN clients connected successfully")
            return
        report_logger.print_info(f"Connected WLAN clients: {', '.join(clients)}")
        gateway_ip = initialize.read_from_database("controller", "bridge_ip")
        baseline = {}
        iperf_server_started = False
        report_logger.print_step("STEP 2: Prepare throughput monitoring and capture client performance baselines")
        report_logger.print_step("STEP 2.1: Start the controller iperf3 server")
        try:
            initialize.execute_command("controller", f"rm -f {IPERF_SERVER_LOG}")
            initialize.start_iperf_server("controller", gateway_ip, IPERF_SERVER_LOG)
            iperf_server_started = True
            report_logger.print_info(f"INFO: Controller iperf3 server started on {gateway_ip}; throughput baselines are enabled")
        except Exception as err:
            report_logger.print_error(f"Throughput monitoring is unavailable because the controller iperf3 server could not start: {err}")
        report_logger.print_step("STEP 2.2: Capture and validate baseline ping metrics for each connected client")
        for index, client in enumerate(clients, start=1):
            report_logger.print_step(f"STEP 2.2.{index}: Ping baseline for {client}")
            try:
                ping_metrics = run_ping(initialize, client, gateway_ip, PING_COUNT)
            except Exception as err:
                report_logger.print_error(f"STEP 2.2.{index} FAILED: {client} baseline ping measurement failed: {err}")
                continue
            if ping_metrics["loss_percent"] > MAX_PACKET_LOSS_PERCENT:
                report_logger.print_error(f"STEP 2.2.{index} FAILED: {client} baseline packet loss is {ping_metrics['loss_percent']:.2f}%")
                continue
            baseline[client] = ping_metrics
            report_logger.print_success(f"PASS: STEP 2.2.{index}: {client} baseline accepted with avg latency={ping_metrics['avg_ms']:.2f} ms and packet loss={ping_metrics['loss_percent']:.2f}%")
            if iperf_server_started:
                report_logger.print_step(f"STEP 2.3.{index}: Measure baseline throughput for client {client}")
                try:
                    throughput = run_iperf(initialize, client, gateway_ip)
                    baseline[client]["throughput_mbps"] = throughput
                    report_logger.print_success(f"PASS: STEP 2.3.{index}: {client} baseline throughput={throughput:.2f} Mbps")
                except Exception as err:
                    report_logger.print_error(f"STEP 2.3.{index} FAILED: {client} baseline throughput measurement failed: {err}")
        if not baseline:
            report_logger.print_error("No connected WLAN clients passed the baseline reachability check")
            return
        report_logger.print_step("STEP 3: Monitor end-to-end client performance")
        start = time.time()
        poll = 0
        while time.time() - start < TEST_DURATION_SEC:
            poll += 1
            for index, client in enumerate(baseline, start=1):
                report_logger.print_step(f"STEP 3.{poll}.{index}: Ping check for {client}")
                try:
                    ping_metrics = run_ping(
                        initialize, client, gateway_ip, PING_COUNT)
                    errors = validate_link_metrics(ping_metrics, baseline[client])
                    if iperf_server_started and "throughput_mbps" in baseline[client]:
                        throughput = run_iperf(initialize, client, gateway_ip)
                        minimum_throughput = (baseline[client]["throughput_mbps"]* MIN_THROUGHPUT_RATIO)
                        if throughput < minimum_throughput:
                            errors.append(f"throughput {throughput:.2f} Mbps is below {minimum_throughput:.2f} Mbps baseline floor")
                except Exception as err:
                    report_logger.print_error(f"{client}: Performance sample failed: {err}")
                    continue
                if errors:
                    report_logger.print_error(f"{client}: Performance instability detected: {'; '.join(errors)}")
                else:
                    report_logger.print_success(f"PASS: Poll #{poll}: {client} latency={ping_metrics['avg_ms']:.2f} ms, loss={ping_metrics['loss_percent']:.2f}%")
            time.sleep(POLL_INTERVAL_SEC)
        report_logger.print_step("STEP 4: Final end-to-end performance validation")
        for index, client in enumerate(baseline, start=1):
            try:
                final_ping = run_ping(initialize,client,gateway_ip,FINAL_PING_COUNT,deadline=FINAL_PING_DEADLINE_SEC,)
                errors = validate_link_metrics(final_ping, baseline[client])
                if iperf_server_started and "throughput_mbps" in baseline[client]:
                    final_throughput = run_iperf(
                        initialize, client, gateway_ip)
                    minimum_throughput = (baseline[client]["throughput_mbps"]* MIN_THROUGHPUT_RATIO)
                    if final_throughput < minimum_throughput:
                        errors.append(f"throughput {final_throughput:.2f} Mbps is below {minimum_throughput:.2f} Mbps baseline floor")
            except Exception as err:
                report_logger.print_error(f"{client}: Final performance validation failed: {err}")
                continue
            if errors:
                report_logger.print_error(f"{client}: Final performance validation failed: {'; '.join(errors)}")
                continue
            report_logger.print_success(f"PASS: Client #{index} {client} final latency={final_ping['avg_ms']:.2f} ms, packet loss={final_ping['loss_percent']:.2f}%")
    finally:
        if locals().get("iperf_server_started", False):
            try:
                initialize.stop_iperf_server("controller")
            except Exception as err:
                report_logger.print_error(f"Unable to stop controller iperf3 server: {err}")
        report_logger.print_test("Exiting test_em_end_to_end_link_performance_stability")