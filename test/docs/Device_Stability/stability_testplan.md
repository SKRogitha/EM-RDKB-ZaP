# Test Case 1: test_stability_long_duration_validation

## Objective

Validate system stability over the configured endurance duration (24 hours by default) by monitoring and analyzing CPU and memory usage of `onewifi_em_agent`, `onewifi_em_ctrl`, and `OneWifi` on the Controller, checking for Controller core dumps, and verifying wireless backhaul connectivity on all agents included in the test.

## Test Type

**Positive**

---

## Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extenders | 3 EasyMesh Agents |
| Network Topology Type | Hybrid Topology |
| Packet Analyzer | IEEE 1905 packet analysis tool |

---

## Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Endurance_test_duration_in_seconds | 86400 second (by default) |
| resources to be validated | cpu and memory |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

## Test Procedure and Expected Results

| Step Number | Controller | EM Agents (all) | Expected Result |
|-------------|------------|----------------|-----------------|
| 1 | Retrieve the configured test duration. | N/A | Test duration should be greater than zero . |
| 2 | Start the resource-monitoring tool and allow a short startup delay. | N/A | Monitoring is initiated on the Controller. the tool will record cpu usage, memory usage and pid change of OneWifi, onewifi_em_ctrl, onewifi_em_agent |
| 3 | Check for core dump files matching `/tmp/*dmp`. Stop the monitoring loop if any are detected. | N/A | No core dumps are detected on the Controller. |
| 4 | N/A | Verify wireless backhaul connectivity for each agent included in the test. Log disconnected agents or connectivity-check errors and exclude those agents from subsequent checks. | All checked agents remain connected to the wireless backhaul. |
| 5 | Repeat the core-dump check throughout the configured duration. | Repeat backhaul checks for agents still being monitored. | Checks repeat with a 60-second wait between cycles until the configured duration expires or a Controller core dump is detected. |
| 6 | Stop the resource-monitoring tool after the monitoring loop ends. | N/A | Controller resource monitoring is stopped. |
| 7 | Check for the configured resource-usage logs and transfer available logs to a timestamped directory on the orchestrator. Delete each remote log after downloading it. | N/A | Available logs are collected locally; missing logs are reported as errors. |
| 8 | Analyze each downloaded resource-usage log using the configured log analyzer. | N/A | Collected logs are analyzed and the results are reported. |

---

# Test Case 2: test_stability_ssid_update_stress

## Objective

Verify that repeated fronthaul SSID changes (100 changes total) are correctly applied on the Controller and reflected all EM Agents, ensure that `onewifi_em_agent`, `onewifi_em_ctrl`, and `OneWifi` remain stable with no continuous increase in memory or CPU usage.

## Test Type

**Positive**

---

## Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extenders | 3 EasyMesh Agents |
| Network Topology Type | Hybrid Topology |
| Packet Analyzer | IEEE 1905 packet analysis tool |

---

## Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `rdkbcli` is available and accessible or the  DE Device.WiFi.DataElements.Network.SetSSID() should be available

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| ssid_update_max_count | 100 (by default) |
| resources to be validated | cpu and memory |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

## Test Procedure and Expected Results

| Step Number | Controller | EM Agent (all ) | Expected Result |
|-------------|------------|-----------------------------|-----------------|
| 1 | Retrieve and validate `ssid_update_max_count`. | N/A | The configured count is greater than zero. |
| 2 | Start resource monitoring and record the initial SSID for later restoration. | N/A | Monitoring is initiated, the tool will record cpu usage, memory usage and pid change of OneWifi, onewifi_em_ctrl, onewifi_em_agent.Also  the initial SSID is retrieved successfully. |
| 3 | Generate and apply a random fronthaul SSID, then wait for the update to propagate. | N/A | The new SSID is applied successfully; an update exception fails the test. |
| 4 | Verify the updated SSID if included in the validation list. | Verify the updated SSID on each included agent. | Each checked device reports the expected SSID. Validation errors are logged, and affected devices are excluded from subsequent checks. |
| 5 | Repeat steps 3-4 until `ssid_update_max_count` updates are completed or no devices remain in the validation list. | Continue validation while included in the list. | The configured update count is reached, or the loop stops when all devices have been excluded. |
| 6 | Stop resource monitoring after the update loop ends. | N/A | Controller resource monitoring is stopped. |
| 7 | Transfer available resource-usage logs to the orchestrator, then delete the downloaded remote logs. | N/A | Available logs are collected locally; missing logs are reported as errors. |
| 8 | Analyze each downloaded resource-usage log on the orchestrator. | N/A | Resource-usage analysis results are reported. |
| 9 | Restore the initial SSID and wait for the update to propagate. | N/A | The initial SSID is reapplied successfully; a restoration exception fails the test. |

---

# Test Case 3: test_stability_channel_change_stress

## Objective

Verify that repeated channel changes for 2.4GHs radio (100 changes total) are correctly applied on the Controller and reflected on all EM Agents.

## Test Type

**Positive**

---

## Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extenders | 3 EasyMesh Agents |
| Network Topology Type | Hybrid Topology |
| Packet Analyzer | IEEE 1905 packet analysis tool |

---

## Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `rdkbcli`  should be available

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| channel_update_max_count | 100 (by default) |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

## Test Procedure and Expected Results

| Step Number | Controller | EM Agent (all agents) | Expected Result |
|-------------|------------|-----------------------------|-----------------|
| 1 | Retrieve and validate `channel_update_max_count`. | N/A | The configured update count is greater than zero; otherwise, the test fails. |
| 2 | Retrieve the current 2.4GHz operating channel at each iteration and save the first value for later restoration. | N/A | The current channel is retrieved successfully; a retrieval exception fails the test. |
| 3 | Request channel 6 when the current channel is not 6; otherwise request channel 1, using channel preference priority 14. Wait for `CHANNEL_UPDATE_WAITING_TIME`. | N/A | The requested channel is applied. Channel-setting exceptions are logged, and device validation still proceeds. |
| 4 | Verify the 2.4GHz operating channel if included in the validation list. | Verify the 2.4GHz operating channel on each included agent. | Each checked device reports the requested channel. Mismatches and retrieval errors are logged, and affected devices are excluded from subsequent validation. |
| 5 | Repeat steps 2-4 until `channel_update_max_count` update attempts are completed or no devices remain in the validation list. | Continue validation while included in the list. | The configured attempt count is reached, or the loop stops when all devices have been excluded. |
| 6 | Retrieve the current 2.4GHz channel and attempt to restore the initial channel, with priority 14, if it differs. | N/A | The initial channel is restored when needed. Retrieval or restoration exceptions are logged; no post-restoration device validation is performed. |

---

# Test Case 4: test_stability_security_mode_update_stress

## Objective

Verify that repeated security mode changes on the  fronthaul (WPA3 Personal ↔ WPA3 Transition, 100 changes total) are correctly applied on the Controller and reflected on EM Agents.

## Test Type

**Positive**

---

## Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extenders | 3 EasyMesh Agents |
| client | linux client |
| Network Topology Type | Hybrid Topology |
| Packet Analyzer | IEEE 1905 packet analysis tool |

---

## Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `rdkbcli` is available and accessible or the  DE Device.WiFi.DataElements.Network.SetSSID() should be available

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

## Test Procedure and Expected Results

| Step Number | Controller | EM Agent (all agents) | Client | Expected Result |
|-------------|------------|-----------------------------|--------|-----------------|
| 1 | Retrieve and store the initial security mode configuration as baseline | N/A | N/A | Initial security mode is successfully retrieved and stored for comparison. |
| 2 | Using `rdkbcli`, set security type to **WPA3 Personal** | N/A | N/A | Security type is successfully set to WPA3 Personal on Controller. |
| 3 | N/A | N/A | Scan and update WiFi networks (`sudo nmcli device wifi rescan && nmcli device wifi list`) | Client detects the fronthaul SSID with security mode: WPA3 Personal |
| 4 | Using `rdkbcli`, set security type to **WPA3 Transition** | N/A | N/A | Security type is successfully set to WPA3 Transition on Controller. |
| 5 | N/A | N/A | Scan and update WiFi networks (`sudo nmcli device wifi rescan && nmcli device wifi list`) | Client detects the fronthaul SSID with security mode: WPA3 Transition |
| 6 | **Repeat steps 2–4 for 49 more cycles** (50 total cycles of WPA3 Personal → WPA3 Transition alternation) | N/A | N/A | All 50 cycles (100 total mode switches) complete successfully with consistent security mode across Controller, EM agents. |
| 7 | Restore the initial security mode | N/A | N/A | N/A |

---

# Test Case 5: test_stability_fronthaul_toggle_stress

## Objective

Verify that repeated disable/enable of the fronthaul network profile (100 iterations) correctly reflect on controller and agents

## Test Type

**Positive**

---

## Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extenders | 3 EasyMesh Agents |
| Network Topology Type | Hybrid Topology |
| Packet Analyzer | IEEE 1905 packet analysis tool |

---

## Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `rdkbcli`  should be available

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| fronthaul_toggle_max_count | 100 (by default) |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

## Test Procedure and Expected Results

| Step Number | Controller | EM Agent (all agents) | Client | Expected Result |
|-------------|------------|-----------------------------|--------|-----------------|
| 1 | Retrieve test parameter `fronthaul_toggle_max_count` from database | N/A | N/A | Test parameter is successfully retrieved. `fronthaul_toggle_max_count` must be greater than 0. |
| 2 | Fetch current MLD status from the Controller | N/A | N/A | Current MLD status is retrieved and stored as baseline. |
| 3 | Toggle MLD status (invert boolean value) | N/A | N/A | New MLD status is calculated (opposite of current status). |
| 4 | Set fronthaul network state on Controller to the toggled MLD status using `set_fronthaul_network_state()` | N/A | N/A | Fronthaul network state is successfully set to the new MLD status on Controller. |
| 5 | Wait for `FRONTHAUL_TOGGLE_WAITING_TIME` seconds for the change to propagate | N/A | N/A | Propagation delay elapses. |
| 6 | Fetch current MLD status from controller | Fetch current MLD status from each EM Agent | N/A | Each EM Agent and controller  reports the expected MLD status. |
| 7 | Repeat steps 3–6 for all `fronthaul_toggle_max_count` iterations | N/A | N/A | All iterations complete successfully. If any device fails to sync MLD status, it is removed from validation list. Test fails if all devices are excluded before reaching max count. |
| 8 | Enable MLD status on Controller to clear any previous toggle state | N/A | N/A | Fronthaul network is enabled, returning to stable state. |
---
