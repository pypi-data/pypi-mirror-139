# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mqtt_to_pagerduty']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0',
 'pdcrier>=0.2.0,<0.3.0',
 'pyaml>=21.10.1,<22.0.0',
 'thelogrus>=0.6.3,<0.7.0']

entry_points = \
{'console_scripts': ['mqtt-alerter = '
                     'mqtt_to_pagerduty.emitter:createAlertMessage',
                     'mqtt-topic-to-pd = '
                     'mqtt_to_pagerduty.cli:topicReaderCommand']}

setup_kwargs = {
    'name': 'mqtt-to-pagerduty',
    'version': '0.2.1',
    'description': 'Read messages in a MQTT topic and create PagerDuty alerts',
    'long_description': '# mqtt-to-pagerduty\n\nRead from a MQTT topic and generate a alert in PagerDuty.\n\n[![GitHub Super-Linter](https://github.com/unixorn/mqtt-to-pagerduty/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)\n\n## Installation\n\n### Direct install\n\n`pip install mqtt_to_pagerduty`\n\n### Docker\n\n`docker pull unixorn/mqtt-to-pagerduty`\n\n## Configuration\n\n`mqtt-to-pagerduty` looks for a yaml configuration file in `~/.hass-tools/mqtt-to-pagerduty.yaml`, or `/config/mqtt-to-pagerduty.yaml` when run in a container.\n\n### Configuration example\n\n```yaml\npagerduty-api-token: XYZZY\nmqtt-server: mqtt.example.com\ntopic: hass/alerts\ndefault-sender: your_pd_user@example.com\nservice_id: XYZZY\n```\n\n## Tools\n\n### mqtt-alerter\n\nCreates an alert message and writes it to a MQTT topic for processing by `mqtt-topic-to-pd`.\n\n```shell\nusage: mqtt-alerter [-h] [-d] [-l {DEBUG,INFO,ERROR,WARNING,CRITICAL}] [--settings-file SETTINGS_FILE] [--sender SENDER]\n                    [--mqtt-server MQTT_SERVER] --title TITLE --service-id SERVICE_ID [--message MESSAGE] [--topic TOPIC]\n\nEmit messages into a MQTT topic\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -d, --debug           Debug setting\n  -l {DEBUG,INFO,ERROR,WARNING,CRITICAL}, --log-level {DEBUG,INFO,ERROR,WARNING,CRITICAL}\n                        set log level\n  --settings-file SETTINGS_FILE, --settings SETTINGS_FILE\n                        Path to settings file. Settings in the file are overridden by command line options\n  --sender SENDER       Email address to send alerts from\n  --mqtt-server MQTT_SERVER\n                        MQTT Server to use\n  --title TITLE         Message title\n  --service-id SERVICE_ID\n                        PagerDuty service ID to alert\n  --message MESSAGE     Message to send\n  --topic TOPIC         MQTT topic to write to\n```\n\n### mqtt-topic-to-pd\n\nListens to a MQTT topic and when it sees an alert message, creates a corresponding PagerDuty alert.\n\n```shell\nusage: mqtt-topic-to-pd [-h] [--api-token API_TOKEN] [-l {DEBUG,INFO,ERROR,WARNING,CRITICAL}] [--settings-file SETTINGS_FILE]\n                        [--duration DURATION] [--sender SENDER] [--service-id SERVICE_ID] [--mqtt-server MQTT_SERVER]\n                        [--topic TOPIC]\n\nRead an MQTT queue and create PagerDuty alerts\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --api-token API_TOKEN\n                        PagerDuty api token\n  -l {DEBUG,INFO,ERROR,WARNING,CRITICAL}, --log-level {DEBUG,INFO,ERROR,WARNING,CRITICAL}\n                        set log level\n  --settings-file SETTINGS_FILE, --settings SETTINGS_FILE\n                        Path to settings file. Settings in the file are overridden by command line options\n  --duration DURATION   How long to read the topic, in seconds\n  --sender SENDER       Email address to send alerts from\n  --service-id SERVICE_ID\n                        Service ID to create an alert\n  --mqtt-server MQTT_SERVER\n                        MQTT server\n  --topic TOPIC         MQTT topic to read\n```',
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unixorn/mqtt-to-pagerduty',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
