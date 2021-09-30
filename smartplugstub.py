import time
import paho.mqtt.client as mqtt
import json
from mqtt import *
from ismartplug import ISmartPlug
from smartplug import SmartPlug
from ismartpluglistener import ISmartPlugListener


class SmartPlugStub(ISmartPlugListener):
    """
    Responsible to abstract the bidirectional communication
    mechanism between the the SmartPlugProxy and the SmartPlug. 
    The class implements the ISmartPlugListener interface
    """

    def __init__(self) -> None:

        # create a smartplug
        self.smartplug: ISmartPlug = SmartPlug(self)

        # init. MQTT
        self.client = mqtt.Client(CLIENT_SMARTPLUG_STUB)
        self.client.connect(MQTT_BROKER)
        self.client.loop_start()
        self.client.subscribe(TOPIC_COMMAND)
        self.client.on_message = lambda client, userdata, message: self.on_message(client, message)

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_message(self, client, message):

        # unpack the command from the message
        msg = json.loads(str(message.payload.decode("utf-8")))
        if msg['id'] == CLIENT_SMARTPLUG_PROXY:

            # dispatch the command to the smartplug
            if msg['cmd'] == SMARTPLUG_CMD_ON:
                self.smartplug.turn_on()

            elif msg['cmd'] == SMARTPLUG_CMD_OFF:
                self.smartplug.turn_off()

    # smartplug listener interface implementation
    def on_smartplug_on(self):
        msg = {'id': CLIENT_SMARTPLUG_STUB, 'cmd': SMARTPLUG_STATE_ON}
        self.client.publish(TOPIC_STATE, json.dumps(msg))

    def on_smartplug_off(self):
        msg = {'id': CLIENT_SMARTPLUG_STUB, 'cmd': SMARTPLUG_STATE_OFF}
        self.client.publish(TOPIC_STATE, json.dumps(msg))


if __name__ == "__main__":
    stub: SmartPlugStub = SmartPlugStub()
    while True:
        time.sleep(0.5)
