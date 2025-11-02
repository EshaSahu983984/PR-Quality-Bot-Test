import re

def validate_pattern(value, pattern):
    return bool(re.match(pattern, value))
