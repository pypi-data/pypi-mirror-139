from typing import Protocol, Union, runtime_checkable, Dict, _ProtocolMeta
from enum import Flag, auto
from datetime import timedelta
from miio.utils import pretty_seconds
from miio.click_common import DeviceGroupMeta
from abc import abstractmethod, abstractproperty, ABC

class VacuumFeatures(Flag):
    SupportsMop = auto()
    SupportsPercentageFanspeed = auto()
    SupportsFind = auto()
    SupportsPresets = auto()

FanspeedPresets = Dict[str, int]


class VacuumCleaningSummary(ABC):
    @property
    @abstractproperty
    def total_duration(self) -> timedelta:
        """Total cleaning duration."""

    @property
    @abstractproperty
    def total_area(self) -> float:
        """Total cleaned area."""

    @property
    @abstractproperty
    def count(self) -> int:
        """Number of cleaning runs."""

class VacuumConsumableStatus(Protocol):
    @property
    def main_brush(self) -> timedelta:
        """Main brush usage time."""

    @property
    def main_brush_total(self) -> timedelta:
        """Return how long main brush should last."""

    @property
    def main_brush_left(self) -> timedelta:
        """How long until the main brush should be changed."""
        return self.main_brush_total - self.main_brush

    @property
    def side_brush_total(self) -> timedelta:
        """Return how long main brush should last."""

    @property
    def side_brush(self) -> timedelta:
        """Side brush usage time."""

    @property
    def side_brush_left(self) -> timedelta:
        """How long until the side brush should be changed."""
        return self.side_brush_total - self.side_brush

    @property
    def filter(self) -> timedelta:
        """Filter usage time."""

    @property
    def filter_total(self) -> timedelta:
        """How long between filter cleanups."""
        return self.filter_total - self.filter

    @property
    def filter_left(self) -> timedelta:
        """How long until the filter should be changed."""
        return self.filter_total - self.filter

    @property
    def sensor_dirty(self) -> timedelta:
        """Return ``sensor_dirty_time``"""

    @property
    def sensor_dirty_total(self) -> timedelta:
        """Return ``sensor_dirty_total``"""

    @property
    def sensor_dirty_left(self) -> timedelta:
        return self.sensor_dirty_total - self.sensor_dirty

class Vacuum(ABC):
    @abstractmethod
    def start(self):
        """Start vacuuming."""

    @abstractmethod
    def pause(self):
        """Pause vacuuming."""

    @abstractmethod
    def stop(self):
        """Stop vacuuming."""

    @abstractmethod
    def status(self):
        """Return status container for the device."""

    @abstractmethod
    def home(self):
        """Return back to base."""

    @abstractmethod
    def find(self):
        """Request vacuum to play a sound to reveal its location."""

    @abstractmethod
    def consumable_status(self) -> 'VacuumConsumableStatus':
        pass

    @abstractmethod
    def clean_history(self) -> VacuumCleaningSummary:
        pass

    @abstractmethod
    def set_fan_speed(self, int):
        """Set fan speed."""

    @abstractmethod
    def fan_speed_presets(self) -> FanspeedPresets:
        pass

    #@abstractmethod
    #def supported_features(self) -> 'VacuumFeatures':
    #    """A enumflag to indicate available features."""
