import argparse
import os
import ssl
import time

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

"""
MQTT Device Simulation
This script simulates an MQTT device by sending periodic messages to an MQTT broker.

Usage:
python mqtt_device_simulation.py -c <mqtt_config> [-i <message_interval>] [-p <message_payload>]

Arguments
-c, --mqtt-config (required): Path to the MQTT configuration file.
-i, --message-interval: Interval (in seconds) between sending messages. Default value is 5 seconds.
-p, --message-payload: Payload of the MQTT message to be sent. Default value is "1#CELCIUS#23".

Configuration File
The MQTT configuration file should be in the format of a dotenv file.
It must include the following environment variables:

MQTT_HOST: Hostname or IP address of the MQTT broker.
MQTT_PORT: Port number of the MQTT broker.
MQTT_CAFILE_PATH: Path to the CA certificate file for secure SSL/TLS connection.
MQTT_USERNAME: Username for authentication with the MQTT broker.
MQTT_PASSWORD: Password for authentication with the MQTT broker.
MQTT_TOPIC: MQTT topic to which messages will be published.

Usage Example
python mqtt_device_simulation.py -c mqtt_config.env -i 10 -p "1#CELCIUS#25"

This command will run the MQTT device simulation using the configuration specified in the mqtt_config.env file,
with a message interval of 10 seconds, and a custom payload "1#CELCIUS#25" for the MQTT messages.
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MQTT device simulation.")
    parser.add_argument(
        "-c",
        "--mqtt-config",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-i",
        "--message-interval",
        type=int,
    )
    parser.add_argument(
        "-p",
        "--message-payload",
        type=str,
    )
    args = parser.parse_args()
    load_dotenv(args.mqtt_config, verbose=True)

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("$SYS/#")

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    client = mqtt.Client()
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(cafile=os.getenv("MQTT_CAFILE_PATH"))
    client.tls_set_context(ssl_context)
    client.username_pw_set(os.getenv("MQTT_USERNAME"), password=os.getenv("MQTT_PASSWORD"))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")), 60)

    interval = args.message_interval if args.message_interval else 5
    payload = args.message_payload if args.message_payload else "1#CELCIUS#23"

    while True:
        time.sleep(interval)
        print(f"Sending message: {payload}")
        client.publish(os.getenv("MQTT_TOPIC"), payload)
