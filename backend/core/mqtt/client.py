from core.mqtt.configurer import get_configured_mqtt_client
from fastapi_mqtt.fastmqtt import FastMQTT


class MQTTClient:
    """Singleton MQTT client implementation."""

    instance = None
    factory_method = get_configured_mqtt_client

    def __new__(cls) -> FastMQTT:
        if cls.instance is None:
            cls.instance = cls.factory_method()
        return cls.instance


def get_mqtt_client() -> FastMQTT:
    return MQTTClient()
