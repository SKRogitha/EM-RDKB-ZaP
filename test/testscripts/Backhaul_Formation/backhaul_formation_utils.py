import re

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
