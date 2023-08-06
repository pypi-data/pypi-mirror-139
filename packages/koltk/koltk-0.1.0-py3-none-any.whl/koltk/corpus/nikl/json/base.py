"""
from koltk.corpus.nikl.json import 
"""

try: 
    import simplejson as json
except ImportError:
    import json

class NIKLJSON(dict):
    """
    NIKLJSON object.
    """ 

    def __init__(self, iterable=(), **extra):
        """
        :return: a NIKLJSON object
        """
        super().__init__(iterable)
        self.update(extra)

    def __repr__(self):
        return json.dumps(self, ensure_ascii=False)

    def __str__(self):
        return json.dumps(self, ensure_ascii=False, indent=2)
    
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    @classmethod
    def decode(s):
        return self(json.loads(s))
