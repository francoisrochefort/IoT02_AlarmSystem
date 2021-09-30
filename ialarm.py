from abc import ABC, abstractmethod


class IAlarm(ABC):
    """
    implemented by both the Alarm and the AlarmProxy classes
    """
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass
