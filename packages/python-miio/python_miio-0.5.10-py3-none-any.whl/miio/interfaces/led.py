from enum import Enum, auto
from typing import Protocol, runtime_checkable
from abc import abstractmethod


class LedBrightness(Enum):
    Bright = auto()
    Dim = auto()
    Off = auto()


@runtime_checkable
class SupportsLed(Protocol):
    """Device supports LED setting."""
    @abstractmethod
    def set_led(self, led: bool):
        """Set the led on/off."""

    @abstractmethod
    def set_led_brightness(self, brightness: LedBrightness):
        """Set the led brightness.

        TBD: this could be no-op per default? Or there could be a feature flag.
        """


@runtime_checkable
class SupportsLedStatus(Protocol):
    """Status containers supporting led controls should implement this protocol."""
    @property
    @abstractmethod
    def led(self) -> bool:
        """Return True if LED is on."""

    @property
    @abstractmethod
    def led_brightness(self) -> Optional[LedBrightness]:
        """Return LED brightness, if supported.

        If LED brightness is not supported, this should return None.
        """