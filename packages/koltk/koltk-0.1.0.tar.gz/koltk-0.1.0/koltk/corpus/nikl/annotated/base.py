"""
from koltk.corpus.nikl.json import 
"""

try: 
    import simplejson as json
except ImportError:
    import json

class Niklanson(dict):
    """
    NIKL Annotated Corpus JSON 
    """ 
    def __init__(self, parent=None):
        self.__parent = parent
        
    @classmethod
    def from_dict(cls, dic, parent=None):
        if type(dic) is not dict:
            raise ValueError

        return cls(**dic, parent=parent)

    @classmethod
    def from_json(cls, json_str):
        return cls(**json.loads(json_str))

    @property
    def parent(self):
        return self.__parent
    
    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)


    def json(self, ensure_ascii=False, **kwargs):
        return json.dumps(self, ensure_ascii=False, **kwargs)

    def __getattr__(self, name):
        if not name.startswith('_'):
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)
        else:
            try:
                return super().__getattr__(name)
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self[name] = value
            
    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            del self[name]

class NiklansonList(list):
    """NiklansonList: NIKL ANnotated Corpus JSON List

    element_type : set the type of the element of the list
   
    For example) self.element_type = Sentence
    """
    def __init__(self, xlist, parent=None):
        self.__parent = parent
        
        if type(xlist) is type(self):
            # TODO: implement clone
            raise NotImplementedError
        elif type(xlist) is list:
            self.__init_from_list(xlist, parent)

        self.postprocess()

    @property
    def parent(self):
        return self.__parent
    
    def postprocess(self):
        pass
            
    def __init_from_list(self, xlist, parent):
        for x in xlist:
            list.append(self, self.element_type.from_dict(x, parent=parent))
