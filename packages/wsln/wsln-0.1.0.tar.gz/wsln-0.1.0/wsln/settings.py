from pathlib import Path
from wsln.parser import PatternSetHandler

version = "0.1"
patterns_file = Path(__file__).absolute().parent / "patterns/patterns.json"
pattern_handler = PatternSetHandler()
pattern_handler.read_patterns_from_file(patterns_file)