from enum import Enum


class UserType(Enum):
    CUSTOMER = 'CUSTOMER'
    # DRIVER = ('DRIVER')


class DriveType(Enum):
    REAR_WHEEL_DRIVE = 'RWD'
    FOUR_WHEEL_DRIVE = '4WD'
    ALL_WHEEL_DRIVE = 'AWD'
    FRONT_WHEEL_DRIVE = 'FWD'
    TWO_WHEEL_DRIVE = '2WD'


class BedCoverType(Enum):
    OPEN = 'OPEN'
    CAMPER = 'CAMPER'
    COVERED = 'COVERED'


class FuelType(Enum):
    GAS = 'GAS'
    HYBRID = 'HYBRID'
    ELECTRIC = 'ELECTRIC'
    DIESEL = 'DIESEL'
    ETHANOL = 'ETHANOL'


class BallSizeType(Enum):
    ONE_AND_THREE_FOURTHS = '1 3/4"'
    TWO = '2"'
    THREE = '3"'
    PIN_AND_KEY = 'PIN and KEY'


class EngineSizeType(Enum):
    THREE_LITER = '3 LITER'
    FIVE_LITER = '5 LITER'
    V6 = 'V6'
    V8 = 'V8'


class RearGlassType(Enum):
    SLIDE = 'SLIDE'
    UP_DOWN = 'UP/DOWN'
    REMOVABLE = 'REMOVABLE'


class BackSeatType(Enum):
    BUCKET_SEAT = 'BUCKET SEAT'
    FOLD_DOWN = 'FOLD DOWN'
    BENCH = 'BENCH'
    SIXTY_FORTY = '60/40'


class FrontSeatType(Enum):
    BUCKET_SEAT = 'BUCKET SEAT'
    BENCH = 'BENCH'


class GenderType(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


class InsuranceCoverageType(Enum):
    COMPLETE = 'COMPLETE'
    COLLISION = 'COLLISION'
    ROADSIDE = 'ROADSIDE'
    LIABILITY = 'LIABILITY'
    UNINSURED = 'UNINSURED'


class DeliveryStatusType(Enum):
    REQUESTED = 'REQUESTED'
    SCHEDULED = 'SCHEDULED'
    IN_PROGRESS = 'IN PROGRESS'
    COMPLETED = 'COMPLETED'
    REJECTED = 'REJECTED'
