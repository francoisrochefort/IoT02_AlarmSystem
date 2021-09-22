import paho.mqtt.client as mqtt
import json
from project1.mqtt import *
from project1.ialarmlistener import IAlarmListener
from project1.ialarm import IAlarm


class AlarmProxy(IAlarm):
    """
    Responsible to abstract the bidirectional communication
    mechanism between the the MainWindow and the AlarmStub. 
    The class implements the IAlarm interface
    """
    def on_message(self, client, message):

        if self.listener is None:
            return

        # unpack the event from the message
        msg = json.loads(str(message.payload.decode("utf-8")))
        if msg['id'] == CLIENT_ALARM_STUB:

            # dispatch the event to the listener
            if msg['cmd'] == SYSALARM_STATE_OFF:
                self.listener.on_alarm_off()
            elif msg['cmd'] == SYSALARM_STATE_ON:
                self.listener.on_alarm_on()
            elif msg['cmd'] == SYSALARM_STATE_RING:
                self.listener.on_alarm_ring()

    def __init__(self, listener: IAlarmListener = None) -> None:

        # init. MQTT
        self.client = mqtt.Client(CLIENT_ALARM_PROXY)
        self.client.connect(MQTT_BROKER) 
        self.client.loop_start()
        self.client.subscribe(TOPIC_STATE)
        self.client.on_message = lambda client, userdata, message: self.on_message(client, message)

        # init. the listener
        self.listener: IAlarmListener = listener

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    # alarm interface implementation
    def turn_on(self):
        msg = {'id': CLIENT_ALARM_PROXY, 'cmd': SYSALARM_CMD_ON}
        self.client.publish(TOPIC_COMMAND, json.dumps(msg))

    def turn_off(self):
        msg = {'id': CLIENT_ALARM_PROXY, 'cmd': SYSALARM_CMD_OFF}
        self.client.publish(TOPIC_COMMAND, json.dumps(msg))
