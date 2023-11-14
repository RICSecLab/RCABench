import sys
from abc import ABC, abstractmethod

class Predicate(ABC):
    def __init__(self, location: str):
        self.location = location

    @abstractmethod
    def compare_to(self, other) -> int:
        pass
    
    @abstractmethod
    def __str__(self):
        pass

class ComparePredicate(Predicate):
    def __init__(self, destination: str, compare: str, value: int, location: str):
        super().__init__(location)
        self.destination = destination
        self.compare = compare
        self.value = value

    def compare_to(self, other) -> int:
        # Check if the other object is an instance of ComparePredicate
        if not isinstance(other, ComparePredicate):
            return -1

        # Check if destination and compare match
        if self.location != other.location or \
           self.destination != other.destination or \
           self.compare != other.compare:
            return -1
        # Return the absolute difference of values
        return abs(self.value - other.value)

    def __str__(self):
        return f"ComparePredicate(destination={self.destination}, "\
               f"compare={self.compare}, value={self.value})"

class EdgePredicate(Predicate):
    def __init__(self, source: int, transition: str, destination: int, location: str):
        super().__init__(location)
        self.source = source
        self.transition = transition
        self.destination = destination

    def compare_to(self, other) -> int:
        # Check if the other object is an instance of EdgePredicate
        if not isinstance(other, EdgePredicate):
            return -1

        return int(self.location == other.location and
                   self.source == other.source and
                   self.transition == other.transition and
                   self.destination == other.destination)

    def __str__(self):
        return f"EdgePredicate(source={self.source}, "\
               f"transition={self.transition}, destination={self.destination})"

class FlagSet(Predicate):
    def __init__(self, flag, location: str):
        super().__init__(location)
        self.flag = flag

    def compare_to(self, other) -> int:
        # Check if the other object is an instance of FlagSet
        if not isinstance(other, FlagSet):
            return -1

        return int(self.location == other.location and self.flag == other.flag)

    def __str__(self):
        return f"FlagSet(flag={self.flag})"

class Visited(Predicate):
    def __init__(self, location: str):
        super().__init__(location)

    def compare_to(self, other) -> int:
        # Check if the other object is an instance of Visited
        if not isinstance(other, Visited):
            return -1

        return int(self.location == other.location)

    def __str__(self):
        return "Visited"

class Unsupported(Predicate):
    def __init__(self, location: str):
        super().__init__(location)

    def compare_to(self, other) -> int:
        return -1

    def __str__(self):
        return "Unsupported"

def decode_predicate(predicate: str, location: str) -> Predicate:
    parts = predicate.split()
    if len(parts) == 3:
        if "reg_val" in parts[1]:
            return ComparePredicate(parts[0], parts[1], int(parts[2][2:], 16), location)
        if "edge" in parts[1]:
            source = int(parts[0][2:], 16)
            destination = int(parts[2][2:], 16)
            return EdgePredicate(source, parts[1], destination, location)
        else:
            print(f"Unknown predicate format: {predicate}", file=sys.stderr)
            return Unsupported(location)
    elif len(parts) == 1:
        if parts[0].endswith("flag_set"):
            return FlagSet(parts[0], location)
        elif parts[0] == "is_visited":
            return Visited(location)
        else:
            print(f"Unknown predicate format: {predicate}", file=sys.stderr)
            return Unsupported(location)
    else:
        print(f"Unknown predicate format: {predicate}", file=sys.stderr)
        return Unsupported(location)
