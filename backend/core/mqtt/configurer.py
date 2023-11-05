import os
import ssl

from dotenv import load_dotenv
from fastapi_mqtt.fastmqtt import FastMQTT, MQTTConfig
from uvicorn.config import logger


def get_configured_mqtt_client() -> FastMQTT:
    """Get configured MQTT client."""
    load_dotenv(verbose=True)
    logger.debug("MQTT client configuration")
    logger.debug(os.environ)
    client_config = {
        "client_id": os.getenv("MQTT_CLIENT_ID"),
        "clean_session": os.getenv("MQTT_CLEAN_SESSION"),
        "optimistic_acknowledgement": os.getenv("MQTT_OPTIMISTIC_ACK"),
    }
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(cafile=os.getenv("MQTT_CAFILE_PATH"))
    connection_config = MQTTConfig(
        host=os.getenv("MQTT_HOST"),
        port=int(os.getenv("MQTT_PORT")),
        username=os.getenv("MQTT_USERNAME"),
        password=os.getenv("MQTT_PASSWORD"),
        reconnect_retries=int(os.getenv("MQTT_RECONNECT_RETRIES")),
        ssl=ssl_context,
    )
    client = FastMQTT(connection_config, **client_config)

    @client.on_connect()
    def connect(client, flags, rc, properties):
        client.subscribe(os.getenv("MQTT_TOPIC_NAMESPACE"), qos=2)
        logger.info("MQTT client connected")

    @client.on_message()
    async def message(client, topic, payload, qos, properties):
        logger.info("MQTT client message received")
        logger.info(f"{topic}: {payload.decode()}")

    @client.on_disconnect()
    def disconnect(client, packet, exc=None):
        logger.info("MQTT client disconnected")

    return client
