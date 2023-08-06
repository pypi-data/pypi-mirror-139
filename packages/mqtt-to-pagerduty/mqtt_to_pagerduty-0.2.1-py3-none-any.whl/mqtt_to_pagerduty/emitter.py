#!/usr/bin/env python3
#
# Emissions Test Driver
#
# Copyright 2022, Joe Block <jpb@unixorn.net>

import argparse
import json
import logging

import paho.mqtt.client as mqtt
from thelogrus.yaml import readYamlFile


def writeMessage(
    server: str,
    topic: str,
    sender: str,
    title: str,
    message: str,
    service_id: str = None,
):
    """
    Create a message in JSON format with the required keys for being
    converted to a PagerDuty alert, then write it to the MQTT topic that
    mqtt-topic-to-pd is listening on.

    Args:
        server (str): _description_
        topic (str): _description_
        sender (str): _description_
        title (str): _description_
        message (str): _description_
        service_id (str, optional): _description_. Defaults to None.
    """
    logging.debug("Creating mqtt client")
    client = mqtt.Client("hot-needle-of-inquiry")

    logging.info(f"Connecting to {server}...")
    client.connect(server)

    payload = json.dumps(
        {
            "title": title,
            "sender": sender,
            "server": server,
            "message": message,
            "title": title,
            "service_id": service_id,
        }
    )

    logging.info(f"Writing {payload} to topic {topic} on {server}")
    client.publish(topic, payload)


def parseCLI():
    """
    Parse the command line options
    """
    parser = argparse.ArgumentParser(description="Emit messages into a MQTT topic")
    parser.add_argument("-d", "--debug", help="Debug setting", action="store_true")
    parser.add_argument(
        "-l",
        "--log-level",
        type=str.upper,
        help="set log level",
        choices=["DEBUG", "INFO", "ERROR", "WARNING", "CRITICAL"],
        default="DEBUG",
    )
    parser.add_argument(
        "--settings-file",
        "--settings",
        type=str,
        default="/config/mqtt-to-pagerduty.yaml",
        help="Path to settings file. Settings in the file are overridden by command line options",
    )
    parser.add_argument(
        "--sender", help="Email address to send alerts from", default="user@example.com"
    )
    parser.add_argument(
        "--mqtt-server", help="MQTT Server to use", type=str, default="mqtt.example.com"
    )
    parser.add_argument(
        "--title",
        help="Message title",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--service-id", help="PagerDuty service ID to alert", type=str, required=True
    )
    parser.add_argument("--message", help="Message to send", type=str)
    parser.add_argument(
        "--topic", help="MQTT topic to write to", default="hass/alerts", type=str
    )

    cli = parser.parse_args()
    loglevel = getattr(logging, cli.log_level.upper(), None)
    logFormat = "[%(asctime)s][%(levelname)8s][%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=loglevel, format=logFormat)
    logging.info("Set log level to %s", cli.log_level.upper())
    return cli


def loadEmitterSettings(cli):
    """
    Create a settings dict using a combination of values found in
    the settings YAML file and cli options.

    cli options override settings specified in the YAML file
    """
    settings = readYamlFile(cli.settings_file)
    logging.debug(f"Raw settings: {settings}")

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

    if cli.title:
        settings["title"] = cli.title
    if "title" not in settings:
        raise ValueError(
            "You must specify the alert title, either in the settings file or via the cli."
        )

    if cli.sender:
        settings["default-sender"] = cli.sender
    if "default-sender" not in settings:
        raise ValueError(
            "You must specify a sender email address, either in the settings file or via the cli."
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


def createAlertMessage():
    """
    Emit a mqtt message to trigger a PD alert
    """
    cli = parseCLI()
    settings = loadEmitterSettings(cli)
    writeMessage(
        server=settings["mqtt-server"],
        topic=settings["topic"],
        service_id=settings["service_id"],
        title=settings["title"],
        sender=settings["default-sender"],
        message=cli.message,
    )


if __name__ == "__main__":
    createAlertMessage()
