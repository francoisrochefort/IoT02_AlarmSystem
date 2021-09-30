import paho.mqtt.client as mqtt
import json
from mqtt import *
from ismartpluglistener import ISmartPlugListener
from ismartplug import ISmartPlug


class SmartPlugProxy(ISmartPlug):
    """
    Responsible to abstract the bidirectional communication
    mechanism between the the MainWindow and the SmartPlugStub. 
    The class implements the ISmartPlug interface
    """
    def on_message(self, client, message):

        if self.listener:

            # unpack the event from the message
            msg = json.loads(str(message.payload.decode("utf-8")))
            if msg['id'] == CLIENT_SMARTPLUG_STUB:

                # dispatch the event to the listener
                if msg['cmd'] == SMARTPLUG_STATE_OFF:
                    self.listener.on_smartplug_off()
                elif msg['cmd'] == SMARTPLUG_STATE_ON:
                    self.listener.on_smartplug_on()

    def __init__(self, listener: ISmartPlugListener = None) -> None:

        # init. MQTT
        self.client = mqtt.Client(CLIENT_SMARTPLUG_PROXY)
        self.client.connect(MQTT_BROKER) 
        self.client.loop_start()
        self.client.subscribe(TOPIC_STATE)
        self.client.on_message = lambda client, userdata, message: self.on_message(client, message)

        # init. the listener
        self.listener: ISmartPlugListener = listener

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    # smartplug interface implementation
    def turn_on(self):
        msg = {'id': CLIENT_SMARTPLUG_PROXY, 'cmd': SMARTPLUG_CMD_ON}
        self.client.publish(TOPIC_COMMAND, json.dumps(msg))

    def turn_off(self):
        msg = {'id': CLIENT_SMARTPLUG_PROXY, 'cmd': SMARTPLUG_CMD_OFF}
        self.client.publish(TOPIC_COMMAND, json.dumps(msg))
