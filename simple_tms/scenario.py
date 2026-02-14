from .tester import Tester
from .step import Step

class Scenario:
    def __init__(self, title: str, steps: list[Step], author: Tester):
        self.title = title
        self.steps = steps
        self.author = author
