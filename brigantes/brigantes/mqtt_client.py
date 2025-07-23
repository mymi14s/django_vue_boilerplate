# myapp/mqtt_client.py
import paho.mqtt.client as mqtt
from django.conf import settings
import json # If you expect JSON payloads

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # Use VERSION2 for modern Paho


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        if settings.MQTT_USER and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
        self.connect()


    def connect(self):
        try:
            self.client.connect(
                host=settings.MQTT_SERVER,
                port=settings.MQTT_PORT,
                keepalive=settings.MQTT_KEEPALIVE
            )
            self.client.loop_start()  # Start the loop in a non-blocking way
        except Exception as e:
            print(f"Could not connect to MQTT broker: {e}")

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker: {settings.MQTT_SERVER}:{settings.MQTT_PORT}")
            # Subscribe to topics here, if needed
            self.client.subscribe(settings.MQTT_TOPIC_SUBSCRIBE)
        else:
            print(f"Failed to connect, return code {rc}\n")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # Process the MQTT message here.
        # You might want to:
        # - Save to Django models
        # - Send data to connected websockets (using Django Channels)
        # - Trigger other Django logic
        try:
            payload = json.loads(msg.payload.decode())
            print(f"Parsed JSON payload: {payload}")
            # Example: Save to a model (assuming you have a SensorReading model)
            # from myapp.models import SensorReading
            # SensorReading.objects.create(topic=msg.topic, value=payload.get('value'))
        except json.JSONDecodeError:
            print("Payload is not JSON.")
        except Exception as e:
            print(f"Error processing message: {e}")
    def publish(self, topic, payload, qos=0, retain=False):
        try:
            self.client.publish(topic, payload, qos, retain)  # Use qos=1 for at least once delivery
            print(f"Published `{payload}` to `{topic}` topic")
        except Exception as e:
            print(f"Failed to publish message: {e}")



