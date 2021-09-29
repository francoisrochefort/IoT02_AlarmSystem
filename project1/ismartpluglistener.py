from abc import ABC, abstractmethod


class ISmartPlugListener(ABC):
    """
    implemented by the main window and the smart plug stub
    """
    @abstractmethod
    def on_smartplug_on(self):
        pass

    @abstractmethod
    def on_smartplug_off(self):
        pass
