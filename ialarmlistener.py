
from abc import ABC, abstractmethod


class IAlarmListener(ABC):
    """
    implemented by the main window and the alarm stub
    """
    @abstractmethod
    def on_alarm_on(self):
        pass

    @abstractmethod
    def on_alarm_off(self):
        pass

    @abstractmethod
    def on_alarm_ring(self):
        pass
