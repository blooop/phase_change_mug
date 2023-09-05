# python3.6

import random

from paho.mqtt import client as mqtt_client
import time
import json
from datetime import datetime


class TemperatureSensor:
    def __init__(self) -> None:
        self.topic = "tele/sonoff/SENSOR"
        # self.topic = "#"
        self.client = self.connect_mqtt()
        self.subscribe(self.client)

        self.temperature = 0.0
        self.start_time = None
        self.time_relative = None
        self.time_abs = None

    def connect_mqtt(self) -> mqtt_client:
        broker = "192.168.0.17"
        port = 1883
        # Generate a Client ID with the subscribe prefix.
        client_id = f"subscribe-{random.randint(0, 100)}"

        def on_connect(client, userdata, flags, rc):  # noqa pylint :ignore
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port, 10)
        client.loop_start()
        return client

    def on_message(self, client, userdata, msg):  # noqa pylint :ignore
        decoded = msg.payload.decode()
        print(f"Received `{decoded}` from `{msg.topic}` topic")
        dat = json.loads(decoded)
        self.time_abs = datetime.strptime(dat["Time"], "%Y-%m-%dT%H:%M:%S")
        self.temperature = float(dat["DS18B20"]["Temperature"])

        if self.start_time is None:
            self.start_time = self.time_abs

        self.time_relative = self.time_abs - self.start_time
        print(self.time_abs)
        print(self.time_relative)
        print(self.temperature)

    def subscribe(self, client: mqtt_client):
        client.subscribe(self.topic)
        client.on_message = self.on_message

        return client

    def get_data(self):
        while self.start_time is None:
            print("waiting for data...")
            time.sleep(1)

        return {
            "time_abs": self.time_abs,
            "time_relative": self.time_relative,
            "temperature": self.temperature,
        }


if __name__ == "__main__":
    tmon = TemperatureSensor()

    while 1:
        dat1 = tmon.get_data()
        print(dat1)
        time.sleep(10)
