from enum import Enum, auto

class Status(Enum):
    Recieved = auto()
    Processing = auto()
    Payment_completed = auto()
    Shipping = auto()
    Completed = auto()
    Cancelled = auto()