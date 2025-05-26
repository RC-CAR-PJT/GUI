import json
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv(override=True)

MQTT_HOST = os.getenv("MQTT_BROKER_IP", "localhost")
MQTT_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))


class MQTTHandler:
    def __init__(self):
        print(f"Connecting to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
        # Command client
        self.command_client = mqtt.Client(client_id="cmd", protocol=mqtt.MQTTv5)
        self.command_client.on_connect = self.on_connect
        self.command_client.on_disconnect = self.on_disconnect
        self.command_client.connect(MQTT_HOST, MQTT_PORT, 60)
        self.command_client.loop_start()

        # Sensing client
        self.sensing_client = mqtt.Client(client_id="sense", protocol=mqtt.MQTTv5)
        self.sensing_client.on_connect = self.on_sense_connect
        self.sensing_client.on_disconnect = self.on_disconnect
        self.sensing_client.on_message = self.on_message_received
        self.sensing_client.connect(MQTT_HOST, MQTT_PORT, 60)
        self.sensing_client.loop_start()

    def publish_command(self, command, value):
        if self.command_client.is_connected():
            topic = "rc_car/command"
            payload = json.dumps({"command": value})
            self.command_client.publish(topic, payload)
        else:
            print("MQTT not connected")

    # Command client callbacks
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"[Command Client] Connected to MQTT with result code {rc}")

    def on_disconnect(self, client, userdata, rc, properties=None):
        print(f"[MQTT] Disconnected from MQTT with result code {rc}")

    # Sensing client callbacks
    def on_sense_connect(self, client, userdata, flags, rc, properties=None):
        print(f"[Sensing Client] Connected with result code {rc}")
        client.subscribe("rc_car/sensing")

    def on_message_received(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"[Sensing Client] Received message on topic '{msg.topic}': {payload}")

    def shutdown(self):
        self.command_client.loop_stop()
        self.command_client.disconnect()
        self.sensing_client.loop_stop()
        self.sensing_client.disconnect()
