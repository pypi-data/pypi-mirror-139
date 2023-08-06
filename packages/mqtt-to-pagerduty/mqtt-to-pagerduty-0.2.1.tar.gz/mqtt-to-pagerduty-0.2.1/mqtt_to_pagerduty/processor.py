#!/usr/bin/env python3
#
# Copyright 2022 Joseph Block <jpb@unixorn.net>
# License: Apache 2.0

import json
import logging
import socket
import time

import paho.mqtt.client as mqtt

pagerDuty = None


def processMessage(client, userdata, message):
    """
    Take an individual MQTT message, decode its JSON and generate an alert
    if it has all the necessary dictionary keys

    Args:
        client (_type_): _description_
        userdata (_type_): _description_
        message (_type_): _description_
    """
    data = str(message.payload.decode("utf-8"))
    logging.debug(f"Recieved {data}, decoding")
    logging.debug(f"pagerduty: {data}")

    logging.debug(f"raw data - {message.payload}")

    try:
        alertInfo = json.loads(data)
        incident = pagerDuty.createIncident(
            title=alertInfo["title"],
            service_id=alertInfo["service_id"],
            message=alertInfo["message"],
        )
        logging.debug(f"Created incident {incident}.")
        logging.info(f"Incident number: {incident['incident_number']}")
        logging.info(f"Incident title: {incident['title']}")
        logging.info(f"Description: {incident['description']}")
        logging.info(f"Created At: {incident['created_at']}")
    except KeyError:
        logging.error(f"Incoming message {data} was missing keys")
    except json.decoder.JSONDecodeError:
        logging.error(f"Invalid JSON: {data}")


def topicReader(
    server: str,
    topic: str,
    clientName: str = socket.gethostname(),
    pagerduty=None,
    duration: int = 0,
):
    """
    Read a MQTT topic and process messages there

    Args:
        server (str): _description_
        topic (str): _description_
        clientName (str, optional): _description_. Defaults to socket.gethostname().
        duration (int, optional): _description_. Defaults to 0.
        pagerduty (_type_, optional): _description_. Defaults to None.
    """
    global pagerDuty

    pagerDuty = pagerduty
    logging.debug(f"Set pagerDuty to {pagerDuty}")

    logging.debug(f"Creating mqtt client '{clientName}'")
    client = mqtt.Client(clientName)
    logging.info(f"Connecting to MQTT server {server} as {clientName}")
    client.connect(server)

    if duration > 0:
        logging.warning(
            f"Beginning topic scan for only {duration} seconds of {topic} on {server}"
        )
    else:
        logging.info(f"Beginning topic scan of {topic} on {server}")
    client.loop_start()

    logging.debug(f"subscribing to {topic}")
    client.subscribe(topic)

    client.on_message = processMessage
    if duration > 0:
        logging.debug(
            f"Scanning {topic} for alert messages for the next {duration} seconds"
        )
        time.sleep(duration)
    else:
        logging.debug(f"Scanning {topic} for alert messages.")
        while True:
            time.sleep(60)
            logging.debug(f"Scanning {topic} for alert messages...")
    client.loop_stop()
