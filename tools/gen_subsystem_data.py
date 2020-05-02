#! /usr/bin/env python3

import requests

# Send request to generate a new datapoint for the subsystems metrics
# Should be set as the following cron 0 0 * * 3 - “At 00:00 on Wednesday.”
r = requests.get('http://localhost/gen_subsystem_data')
print(r.content)
