## Test Case 1: test_wifi_security_wpa2_personal_configuration_propagation_from_controller_to_agent

### Objective

Verify that WPA2-Personal security configured on the Multi-AP Controller is successfully synchronized to the Agent and client can connect using the updated security configuration.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA2-Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA2-Personal |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA2-Personal using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration `sudo nmcli device wifi rescan` and `nmcli -f BSSID,SSID,SECURITY device wifi list \| grep <SSID>` | Security configuration should be wpa2-personal |
| 4 | N/A | N/A | connect to the network with updated security configuration | Client should successfully connect using WPA2-Personal security |
| 5 | N/A | N/A | disconnect from the network | Client should successfully disconnect from the network |

---

## Test Case 2: test_wifi_security_wpa2_personal_configuration_persistence_after_controller_reboot

### Objective

Verify that WPA2-Personal security configuration is retained on  Controller after reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA2-Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA2-Personal |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA2-Personal using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be wpa2-personal |
| 4 | Reboot Controller | N/A | N/A | Controller reboots successfully |
| 5 | Wait for Controller to recover and EasyMesh services to become operational | N/A | N/A | EasyMesh network becomes operational |
| 6 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 3: test_wifi_security_wpa2_personal_configuration_persistence_after_extender_reboot

### Objective

Verify that WPA2-Personal security configuration is retained on the Agent after Agent reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA2-Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA2-Personal |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA2-Personal using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be wpa2-personal |
| 4 | N/A | Reboot extender | N/A | extender reboots successfully |
| 5 | Wait for extender to recover and become operational | N/A | N/A | extender is reachable over ssh |
| 6 | N/A | N/A | verify that extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 4: test_wifi_security_open_configuration_propagation_from_controller_to_agent

### Objective

Verify that open security configured on the Multi-AP Controller is successfully synchronized to the Agent and client can connect using the updated security configuration.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | Open Security Network Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | Open |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as Open using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be Open |
| 4 | N/A | N/A | connect to the network with updated security configuration | Client should successfully connect using Open security |
| 5 | N/A | N/A | disconnect from the network | Client should successfully disconnect from the network |
---

## Test Case 5: test_wifi_security_open_configuration_persistence_after_controller_reboot

### Objective

Verify that Open security configuration is retained on  Controller after reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | Open Security Network Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | Open |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as Open using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be Open |
| 4 | Reboot Controller | N/A | N/A | Controller reboots successfully |
| 5 | Wait for Controller to recover and EasyMesh services to become operational | N/A | N/A | EasyMesh network becomes operational |
| 6 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 6: test_wifi_security_open_configuration_persistence_after_extender_reboot

### Objective

Verify that Open security configuration is retained on the Agent after Agent reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | Open Security Network Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | Open |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as Open using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be Open |
| 4 | N/A | Reboot extender | N/A | extender reboots successfully |
| 5 | Wait for extender to recover and become operational | N/A | N/A | extender is reachable over ssh |
| 6 | N/A | N/A | verify that extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 7: test_wifi_security_Enhanced_Open_configuration_propagation_from_controller_to_agent

### Objective

Verify that Enhanced Open (OWE) security configured on the Multi-AP Controller is successfully synchronized to the Agent and client can connect using the updated security configuration

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | Enhanced Open (OWE) Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | Enhanced Open (OWE) |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as Enhanced Open (OWE) using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security mode should be displayed as Enhanced Open (OWE) |
| 4 | N/A | N/A | connect to the network with updated security configuration | Client should successfully connect using Enhanced Open (OWE) security |
| 5 | N/A | N/A | disconnect from the network | Client should successfully disconnect from the network |

---

## Test Case 8: test_wifi_security_Enhanced_Open_configuration_persistence_after_controller_reboot

### Objective

Verify that Enhanced Open (OWE) security configuration is retained on  Controller after reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | Enhanced Open (OWE) Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | Enhanced Open (OWE) |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as Enhanced Open (OWE) using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be Enhanced Open (OWE) |
| 4 | Reboot Controller | N/A | N/A | Controller reboots successfully |
| 5 | Wait for Controller to recover and EasyMesh services to become operational | N/A | N/A | EasyMesh network becomes operational |
| 6 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 9: test_wifi_security_enhanced_open_configuration_persistence_after_extender_reboot

### Objective

Verify that enhanced open (OWE) security configuration is retained on the Agent after Agent reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA2-Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | Enhanced Open (OWE) |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as Enhanced Open (OWE) using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be Enhanced Open (OWE) |
| 4 | N/A | Reboot extender | N/A | extender reboots successfully |
| 5 | Wait for extender to recover and become operational | N/A | N/A | extender is reachable over ssh |
| 6 | N/A | N/A | verify that extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 10: test_wifi_security_wpa3_personal_configuration_propagation_from_controller_to_agent

### Objective

Verify that WPA3-Personal security configured on the Multi-AP Controller is successfully synchronized to the Agent and client can connect using the updated security configuration

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA3-Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA3-Personal |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA3-Personal using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security mode should be displayed as WPA3-Personal |
| 4 | N/A | N/A | connect to the network with updated security configuration | Client should successfully connect using WPA3-Personal security |
| 5 | N/A | N/A | disconnect from the network | Client should successfully disconnect from the network |

---

## Test Case 11: test_wifi_security_wpa3_personal_configuration_persistence_after_controller_reboot

### Objective

Verify that WPA3-Personal security configuration is retained on  Controller after reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA3-personal capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA3-Personal |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA3-Personal using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is correctly applied on all devices with WPA3-Personal |
| 4 | Reboot Controller | N/A | N/A | Controller reboots successfully |
| 5 | Wait for Controller to recover and EasyMesh services to become operational | N/A | N/A | EasyMesh network becomes operational |
| 6 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 12: test_wifi_security_wpa3_personal_configuration_persistence_after_extender_reboot

### Objective

Verify that WPA3-Personal security configuration is retained on the Agent after Agent reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA3-Personal Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA3-Personal |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA3-Personal using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration | Security configuration should be WPA3-Personal |
| 4 | N/A | Reboot extender | N/A | extender reboots successfully |
| 5 | Wait for extender to recover and become operational | N/A | N/A | extender is reachable over ssh |
| 6 | N/A | N/A | verify that extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 13: test_wifi_security_wpa3_transition_mode_configuration_propagation_from_controller_to_agent

### Objective

Verify that WPA3-transition mode security configured on the Multi-AP Controller is successfully synchronized to the Agent and client can connect using the updated security configuration

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA3-Transition  Capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA3-Transition |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA3-Transition using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration should be WPA3-Transition |
| 4 | N/A | N/A | connect to the network with updated security configuration | Client should successfully connect using WPA3-transition security |
| 5 | N/A | N/A | disconnect from the network | Client should successfully disconnect from the network |

---

## Test Case 14: test_wifi_security_wpa3_transition_configuration_persistence_after_controller_reboot

### Objective

Verify that WPA3-Transition security configuration is retained on  Controller after reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA3-Transition capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA3-Transition |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA3-Transition using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is correctly applied on all devices with WPA3-Transition |
| 4 | Reboot Controller | N/A | N/A | Controller reboots successfully |
| 5 | Wait for Controller to recover and EasyMesh services to become operational | N/A | N/A | EasyMesh network becomes operational |
| 6 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---

## Test Case 15: test_wifi_security_wpa3_transition_configuration_persistence_after_extender_reboot

### Objective

Verify that WPA3-Transition security configuration is retained on the Agent after Agent reboot.

### Test Type

**Positive**

---

### Test Environment

| Component | Description |
|-----------|-------------|
| Controller | EasyMesh Controller |
| Extender | EasyMesh Agent |
| Packet Analyzer | IEEE 1905 Packet Analysis Tool |
| Wi-Fi Client | WPA3-Transition capable Client |

---

### Pre-Requisites

1. Controller and all Extenders are onboarded with active EasyMesh backhaul connections.
2. The Controller and all Extenders are reachable over SSH.
3. The capture interface, IEEE 1905 filter, remote capture directory, and local capture directory are configured for the Controller and every Extender.
4. The AL MAC address and profile type are configured for the Controller, collocated Agent, and all Extenders.
5. `RDKBCLI` is available and accessible or the DE 'Device.WiFi.DataElements.Network.SetSSID()' is accessible for configuring AKMsAllowed.

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Security mode | WPA3-Transition |
| Network Topology | Controller and 3 Extenders in an active EasyMesh Hybrid topology |

---

### Test Procedure and Expected Results

| Step Number | Controller | Extender | Client | Expected Result |
| ------------- | ------------ | ---------- | ----------------- | --- |
| 1 | Configure security mode as WPA3-Transition using RDKBCLI or DE 'Device.WiFi.DataElements.Network.SetSSID()' | N/A | N/A | Security mode configured successfully |
| 2 | Wait for Controller to provision Agent | N/A | N/A | Agent receives updated security configuration |
| 3 | N/A | N/A | verify that controller's and all extender's fronthaul ssid are broadcasting with updated security configuration | Security configuration should be WPA3-Transition |
| 4 | N/A | Reboot extender | N/A | extender reboots successfully |
| 5 | Wait for extender to recover and become operational | N/A | N/A | extender is reachable over ssh |
| 6 | N/A | N/A | verify that extender's fronthaul ssid are broadcasting with updated security configuration  | Security configuration is persisted after reboot |

---
