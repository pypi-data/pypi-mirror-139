#!/usr/bin/env python3
#
# Copyright 2022 Joseph Block <jpb@unixorn.net>
# License: Apache 2.0

import argparse
import logging

from mqtt_to_pagerduty.processor import topicReader
from mqtt_to_pagerduty.settings import loadRelaySettings
from pdcrier.pagerduty import PagerDuty


def topicReaderCLI():
    """
    Parse the command line options
    """
    parser = argparse.ArgumentParser(
        description="Read an MQTT queue and create PagerDuty alerts"
    )
    parser.add_argument("--api-token", help="PagerDuty api token", type=str)
    parser.add_argument(
        "-l",
        "--log-level",
        type=str.upper,
        help="set log level",
        choices=["DEBUG", "INFO", "ERROR", "WARNING", "CRITICAL"],
        default="INFO",
    )
    parser.add_argument(
        "--settings-file",
        "--settings",
        type=str,
        default="/config/mqtt-to-pagerduty.yaml",
        help="Path to settings file. Settings in the file are overridden by command line options",
    )

    parser.add_argument(
        "--duration",
        help="How long to read the topic, in seconds - <= 0 for run until killed",
        type=int,
        default=-1,
    )
    parser.add_argument("--sender", help="Email address to send alerts from")
    parser.add_argument("--service-id", help="Service ID to create an alert")
    parser.add_argument("--mqtt-server", help="MQTT server", type=str)
    parser.add_argument("--topic", help="MQTT topic to read", type=str)

    cli = parser.parse_args()
    loglevel = getattr(logging, cli.log_level.upper(), None)
    logFormat = "[%(asctime)s][%(levelname)8s][%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=loglevel, format=logFormat)
    logging.info("Set log level to %s", cli.log_level.upper())
    logging.debug(f"cli: {cli}")
    return cli


def topicReaderCommand():
    """
    topicReaderCommand() is the launcher for reading a MQTT topic and
    generating PagerDuty alerts.
    """
    cli = topicReaderCLI()
    settings = loadRelaySettings(cli=cli)
    logging.debug(f"Settings: {settings}")

    pager = PagerDuty(
        api_token=settings["pagerduty-api-token"], sender=settings["default-sender"]
    )

    topicReader(
        server=settings["mqtt-server"],
        topic=settings["topic"],
        duration=settings["duration"],
        pagerduty=pager,
    )
