from datetime import date, datetime
from typing import Any, AnyStr, Callable, Dict, List, Tuple, Union

from .dictcomparer import DictComparer

class RowKey():
    """Encapsulates the fields used as the primary key for a record"""

    def __init__(self, *keys):
        """Encapsulates the fields used as the primary key for a record.
        ``keys``:  One of more key names (strings)"""
        self.keys = keys
    
    def __call__(self, row : dict):
        """
        Returns a tuple of values from ``row`` which correspond to the given keys
        """
        if isinstance(row, dict):
            return tuple([row.get(key, None) for key in self.keys])
        raise NotImplementedError()
        
    def group_rows(self, rows : List[dict]):
        """Returns a dict where ``rows`` are grouped by this key"""
        document = {}
        for row in rows:
            document.setdefault(self(row), []).append(row)            
        return document
    
    def __iter__(self):
        """Iterates the key names"""
        return iter(self.keys)
