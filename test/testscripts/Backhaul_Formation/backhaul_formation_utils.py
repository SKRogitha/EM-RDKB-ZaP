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
