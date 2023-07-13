from enum import Enum


class MeasurementType(Enum):
    CALIBRATION = auto()
    SAMPLE = auto()
    PROCESSED = auto()
