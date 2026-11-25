import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from rdkbmeshzap.common_utils import report_logger

# Seconds to wait after a reboot so the Agent boots and topology messages reach the capture.
ONBOARDING_SETTLE_SECONDS = 60
# Maximum seconds to wait for the backhaul link to come up (or, in the negative test, the seconds it must stay down).
ONBOARDING_TIMEOUT_SECONDS = 300
# Seconds between backhaul link polls and pings.
POLL_INTERVAL_SECONDS = 10
# Colon-delimited MAC address.
MAC_PATTERN = re.compile(r"^[0-9a-f]{2}(:[0-9a-f]{2}){5}$", re.I)

# File on the Agent that holds the provisioned backhaul credentials.
AGENT_BACKHAUL_CONFIG = "/nvram/EasymeshCfg.json"
# Backup of the valid Agent backhaul configuration, used for the manual restore.
AGENT_BACKHAUL_CONFIG_BACKUP = "/nvram/EasymeshCfg.json.tc10.bak"
# Deliberately wrong backhaul passphrase (must not contain / & or backslash, it is used in a sed expression).
INVALID_PASSPHRASE = "InvalidBackhaulPassphrase_TC10"
# Echo requests sent per ping from the Controller.
PING_COUNT = 2

def get_packet_loss(initialize, device, ip):
    """
    Ping the IP from the device and return the packet loss percentage, or None if it is not found.
    """
    # initialize.ping_ipv4 cannot be used because it needs a data_iface and the rdkbmeshzap platform has no ping_ipv4.
    output = initialize.execute_command(device, f"ping -4 -c {PING_COUNT} -W 2 {ip}")
    match = re.search(r"(\d+(?:\.\d+)?)% packet loss", str(output))
    if not match:
        report_logger.print_error(f"FAIL: Packet loss not found in the ping output: {str(output).strip()!r}")
        return None
    return float(match.group(1))

def set_invalid_backhaul_passphrase(initialize, agent):
    """
    Back up the Agent backhaul config and set the invalid passphrase. Return True once it is written.
    """
    # Stop if the invalid passphrase is already there (earlier failed run), the backup would hold it and the later check could not prove this run changed it.
    existing = initialize.execute_command(agent, f"grep -c {INVALID_PASSPHRASE} {AGENT_BACKHAUL_CONFIG}")
    if str(existing).strip().splitlines()[-1:] != ["0"]:
        report_logger.print_error(f"FAIL: {agent} already has the invalid passphrase or the config could not be read, restore it manually before running")
        return False
    # Back up the config and continue only if the backup holds the passphrase key.
    backup = initialize.execute_command(agent, f"cp -f {AGENT_BACKHAUL_CONFIG} {AGENT_BACKHAUL_CONFIG_BACKUP} && sync && grep -c Backhaul_KeyPassphrase {AGENT_BACKHAUL_CONFIG_BACKUP}")
    if str(backup).strip().splitlines()[-1:] != ["1"]:
        report_logger.print_error(f"FAIL: Could not back up the backhaul config on {agent}")
        return False
    # Replace the Backhaul_KeyPassphrase value with the invalid passphrase and check it was written.
    pattern = r'\("Backhaul_KeyPassphrase"[[:space:]]*:[[:space:]]*"\)\([^"\\]\|\\.\)*"'
    replacement = r"\1" + INVALID_PASSPHRASE + '"'
    sed_output = initialize.execute_command(agent, "sed -i 's/" + pattern + "/" + replacement + "/' " + AGENT_BACKHAUL_CONFIG + " && sync && echo SED_OK")
    if "SED_OK" not in str(sed_output):
        report_logger.print_error(f"FAIL: The sed update of the backhaul config failed on {agent}: {str(sed_output).strip()!r}")
        return False
    # Match the key and value together so the passphrase is proven to sit under Backhaul_KeyPassphrase.
    applied = initialize.execute_command(agent, "grep -c '\"Backhaul_KeyPassphrase\"[[:space:]]*:[[:space:]]*\"" + INVALID_PASSPHRASE + "\"' " + AGENT_BACKHAUL_CONFIG)
    if str(applied).strip().splitlines()[-1:] != ["1"]:
        report_logger.print_error(f"FAIL: Could not set the invalid passphrase on {agent}")
        return False
    report_logger.print_success(f"PASS: {agent}: Backhaul_KeyPassphrase is set to the invalid passphrase in {AGENT_BACKHAUL_CONFIG}")
    return True

def reboot_and_verify_down(initialize, agents, agent_ips):
    """
    Reboot all Agents at once and verify none comes back. Return True if every Agent is unreachable from the Controller.
    """
    errors = {}
    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = {executor.submit(initialize.reboot_device, agent, method="cli"): agent for agent in agents}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as error:
                errors[futures[future]] = error
    for agent in agents:
        if agent in errors:
            report_logger.print_error(f"FAIL: {agent}: reboot command failed: {errors[agent]}")
        else:
            report_logger.print_info(f"INFO: Reboot command executed for {agent}")
    if errors:
        return False
    # Poll until every Agent stops answering, which means the old backhaul is gone.
    pending = list(agents)
    deadline = time.monotonic() + ONBOARDING_TIMEOUT_SECONDS
    while pending and time.monotonic() < deadline:
        for agent in list(pending):
            loss = get_packet_loss(initialize, "controller", agent_ips[agent])
            if loss is None:
                return False
            if loss >= 100:
                pending.remove(agent)
                report_logger.print_success(f"PASS: {agent} is down after the reboot")
        if pending:
            time.sleep(POLL_INTERVAL_SECONDS)
    if pending:
        report_logger.print_error(f"FAIL: {pending} did not go down within {ONBOARDING_TIMEOUT_SECONDS}s of the reboot")
        return False
    return True
