# File: app/models/content_section.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ContentSection:
    level: str
    content: str = ""
    exercises: List[Dict] = None

    def __post_init__(self):
        if self.exercises is None:
            self.exercises = []
    
    def to_dict(self):
        return {
            'level': self.level,
            'content': self.content,
            'exercises': self.exercises
        }