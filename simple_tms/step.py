from .bug import Bug

class Step:
    def __init__(self, description: str, expected: str, actual: str, bug: Bug = None):
        self.descripton = description
        self.expected = expected
        self.actual = actual
        self.bug = bug