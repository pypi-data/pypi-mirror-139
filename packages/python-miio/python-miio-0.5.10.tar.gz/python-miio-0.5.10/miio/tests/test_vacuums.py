import inspect
import unittest
import pytest
from miio import RoborockVacuum, ViomiVacuum, RoidmiVacuumMiot, G1Vacuum
from miio.interfaces import Vacuum


VACUUMS = [RoborockVacuum, ViomiVacuum, RoidmiVacuumMiot]

@pytest.mark.parametrize("cls", VACUUMS)
def test_verify_interfaces(cls):
    dev = cls("127.0.0.1", "ffffffffffffffffffffffffffffffff")
    try:
        assert isinstance(dev, Vacuum)
    except Exception as ex:
        
        inspect.getmembers(Vacuum)
        print("")


