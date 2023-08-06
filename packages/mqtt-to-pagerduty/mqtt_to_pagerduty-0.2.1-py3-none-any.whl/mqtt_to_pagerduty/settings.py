#!/usr/bin/env python3
#
# Copyright 2022 Joseph Block <jpb@unixorn.net>
# License: Apache 2.0

import logging

from thelogrus.yaml import readYamlFile


def loadRelaySettings(cli):
    """
    Create a settings dict using a combination of values found in
    the settings YAML file and cli options.

    cli options override settings specified in the YAML file
    """
    settings = readYamlFile(cli.settings_file)
    logging.debug(f"Raw settings: {settings}")

    if cli.api_token:
        settings["pagerduty-api-token"] = cli.api_token
    if "pagerduty-api-token" not in settings:
        raise ValueError(
            "You must specify a PagerDuty API token, either in the settings file or via the cli."
        )
    else:
        logging.debug(f"pagerduty-api-token: {settings['pagerduty-api-token']}")

    if cli.duration:
        logging.debug(f"duration: {cli.duration}")
        settings["duration"] = cli.duration
    if "duration" not in settings:
        # By default, we want to run until we're explicitly stopped
        settings["duration"] = 0

    if cli.mqtt_server:
        settings["mqtt-server"] = cli.mqtt_server
    if "mqtt-server" not in settings:
        raise ValueError(
            "You must specify the MQTT server, either in the settings file or via the cli."
        )

    if cli.topic:
        settings["topic"] = cli.topic
    if "topic" not in settings:
        raise ValueError(
            "You must specify the MQTT topic, either in the settings file or via the cli."
        )

    if cli.sender:
        settings["default-sender"] = cli.sender
    if "default-sender" not in settings:
        raise ValueError(
            "You must specify a default sender email address, either in the settings file or via the cli."
        )
    else:
        logging.debug(f"Default sender: {settings['default-sender']}")

    if cli.service_id:
        settings["service_id"] = cli.service_id
    if "service_id" not in settings:
        raise ValueError(
            "You must specify a PagerDuty service id, either in the settings file or via the cli."
        )
    else:
        logging.debug(f"Service ID: {settings['service_id']}")

    return settings
