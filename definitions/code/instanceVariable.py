from dataclasses import dataclass


@dataclass
class InstanceVariable:
    """
    Represents a variable that is in a instance of a java class.
    Holds the name, the type and the actual (java) value of the variable.
    """

    name: str
    variable_type: str
    value: object
