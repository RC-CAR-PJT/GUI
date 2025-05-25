import paho.mqtt.client as mqtt
from mqtt.handlers import setup_mqtt_callbacks

class MqttManager:
    def __init__(self, parent_ui):
        self.command_client = mqtt.Client(client_id="command_client", callback_api_version=mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
        self.sensing_client = mqtt.Client(client_id="sensing_client", callback_api_version=mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
        setup_mqtt_callbacks(self, parent_ui)

    def connect_clients(self):
        self.command_client.connect("70.12.227.91", 1883, 60)
        self.sensing_client.connect("70.12.227.91", 1883, 60)
        self.command_client.loop_start()
        self.sensing_client.loop_start()
