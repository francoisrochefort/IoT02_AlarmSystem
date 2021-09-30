

__all__ = ["MQTT_BROKER", 
           "CLIENT_ALARM_PROXY", 
           "CLIENT_SMARTPLUG_PROXY",
           "CLIENT_SMARTPLUG_STUB",
           "CLIENT_ALARM_STUB",
           "CLIENT_LIGHT",
           "CLIENT_ALL",
           "TOPIC_STATE",
           "TOPIC_COMMAND",
           "SYSALARM_STATE_OFF",
           "SYSALARM_STATE_ON",
           "SYSALARM_CMD_OFF",
           "SYSALARM_CMD_ON",
           "SYSALARM_STATE_RING",
           "SMARTPLUG_STATE_OFF",
           "SMARTPLUG_STATE_ON",
           "SMARTPLUG_CMD_OFF",
           "SMARTPLUG_CMD_ON",
           "LIGHT_STATE_OFF",
           "LIGHT_STATE_ON",
           "LIGHT_CMD_OFF",
           "LIGHT_CMD_ON"]


"""MQTT broker"""
MQTT_BROKER = "127.00.00.01"

"""MQTT clients"""
CLIENT_ALARM_PROXY = "AlarmProxy"
CLIENT_ALARM_STUB = "SysAlarmStub"
CLIENT_SMARTPLUG_PROXY = "SmartPlugProxy"
CLIENT_SMARTPLUG_STUB = "SmartPlugStub"
CLIENT_LIGHT = "Light"
CLIENT_ALL = "All IoT"

"""MQTT topics"""
TOPIC_STATE = "Gills/Etats"
TOPIC_COMMAND = "Gills/Commandes"

"""SmartPlug1 states"""
SMARTPLUG_STATE_OFF = "off"
SMARTPLUG_STATE_ON  = "on"

"""SmartPlug1 commands"""
SMARTPLUG_CMD_OFF = "off"
SMARTPLUG_CMD_ON  = "on"

"""System alarm states"""
SYSALARM_STATE_OFF = "off"
SYSALARM_STATE_ON  = "on"
SYSALARM_STATE_RING  = "ring"

"""System alarm commands"""
SYSALARM_CMD_OFF = "off"
SYSALARM_CMD_ON  = "on"

"""Light states"""
LIGHT_STATE_OFF = "off"
LIGHT_STATE_ON  = "on"

"""Light commands"""
LIGHT_CMD_OFF = "off"
LIGHT_CMD_ON  = "on"

