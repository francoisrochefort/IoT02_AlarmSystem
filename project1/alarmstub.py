import time
import paho.mqtt.client as mqtt
import json
from mqtt import *
from ialarm import IAlarm
from alarm import Alarm
from ialarmlistener import IAlarmListener


class AlarmStub(IAlarmListener):
    """
    Responsible to abstract the bidirectional communication
    mechanism between the the AlarmProxy and the Alarm. 
    The class implements the IAlarmListener interface
    """

    def __init__(self) -> None:

        # create an alarm
        self.alarm: IAlarm = Alarm(self)

        # init. MQTT
        self.client = mqtt.Client(CLIENT_ALARM_STUB)
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
        if msg['id'] == CLIENT_ALARM_PROXY:

            # dispatch the command to the alarm
            if msg['cmd'] == SYSALARM_CMD_ON:
                self.alarm.turn_on()

            elif msg['cmd'] == SYSALARM_CMD_OFF:
                self.alarm.turn_off()

    # alarm listener interface implementation
    def on_alarm_on(self):
        msg = {'id': CLIENT_ALARM_STUB, 'cmd': SYSALARM_STATE_ON}
        self.client.publish(TOPIC_STATE, json.dumps(msg))

    def on_alarm_off(self):
        msg = {'id': CLIENT_ALARM_STUB, 'cmd': SYSALARM_STATE_OFF}
        self.client.publish(TOPIC_STATE, json.dumps(msg))

    def on_alarm_ring(self):
        msg = {'id': CLIENT_ALARM_STUB, 'cmd': SYSALARM_STATE_RING}
        self.client.publish(TOPIC_STATE, json.dumps(msg))


if __name__ == "__main__":
    stub: AlarmStub = AlarmStub()
    while True:
        time.sleep(0.5)
