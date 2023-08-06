r"""NIKLJSON Objects

"""

from __future__ import annotations
from .base import NIKLJSON
import re

class CorpusMetadata(NIKLJSON):
    def __init__(self, iterable=(), **extra):
        self.title = None
        self.creator = None
        self.distributor = None
        self.year = None
        self.category = None
        self.annotation_level = []
        self.sampling = None
        
        super().__init__(iterable)
        self.update(extra)
    
class Corpus(NIKLJSON):
    def __init__(self, id=None, metadata=CorpusMetadata(), document=[]):
        self.id = id
        self.metadata = metadata
        self.document = document 

class DocumentMetadata(NIKLJSON):
    def __init__(self, iterable=(), **extra):
        self.title = None
        self.author = None
        self.publisher = None
        self.date = None
        self.topic = None
        self.url = None
        
        super().__init__(iterable)
        self.update(extra)
    

class Document(NIKLJSON):
    """
    Document(id, metadata=DocumentMetadata(), sentence=[])

    ::

        >>> d = Document('X200818')
        >>> print(d)
        {
          "id": "X200818",
          "metadata": {
            "title": "",
            "author": "",
            "publisher": "",
            "date": "",
            "topic": "",
            "url": ""
          },
          "sentence": []
        }
       
    """
    def __init__(self, id=None, metadata=DocumentMetadata(), sentence=[]):
        self.id = id
        self.metadata = metadata
        self.sentence = sentence

    
class Sentence(NIKLJSON):
    """
    Sentence(id, form)

    ::

        >>> s = Sentence('X200818', '아이들이 책을 읽는다.')
        >>> print(s)
        {
          "id": "X200818",
          "form": "아이들이 책을 읽는다.",
          "word": [
              {
                "id": 1,
                "form": "아이들이",
                "begin": 0,
                "end": 4
              },
              {
                "id": 2,
                "form": "책을",
                "begin": 5,
                "end": 7
              },
              {
                "id": 3,
                "form": "읽는다.",
                "begin": 8,
                "end": 12
              }
          ]
        }    

    """
    def __init__(self, id: str, form: str):
       self.id = id
       self.form = form
       self.word = []
       beg = 0
       i = 0
       for tok in re.split('(\s+)', self.form):
           if tok == '' : continue
           elif re.match('\s', tok[0]) : beg += len(tok)
           else:
               i += 1
               self.word.append(Word(i, tok, beg, beg + len(tok))) 
               beg += len(tok)
           
class Word(NIKLJSON):
    """
    Word
    """
    def __init__(self, id : int, form : str, begin : int, end : int):
        self.id = id
        self.form = form
        self.begin = begin
        self.end = end

class Morpheme(NIKLJSON):
    """
    Morpheme
    """
    def __init__(self, id: int, form: str, label: str, word_id: int, position: int):
        self.id = id
        self.form = form
        self.label = label
        self.word_id = word_id
        self.position = position

class WSD(NIKLJSON):
    """
    WSD (Word Sense Disambiguation)
    """
    def __init__(self, word: str, sense_id: int, pos : str, begin: int, end: int):
        self.word = word
        self.sense_id = sense_id
        self.pos = pos
        self.begin = begin
        self.end = end

class NE(NIKLJSON):
    """
    NE (Named Entity)
    """
    def __init__(self, id: int, form: str, label: str, begin:int, end: int):
        self.id = id
        self.form = form
        self.label = label
        self.begin = begin
        self.end = end

class DP(NIKLJSON):
    """
    DP (Denpendency Parsing)
    """
    def __init__(self, word_id: int, word_form: str, head: int, label: str, depdendent: list[int]):
        self.word_id = word_id
        self.word_form = word_form
        self.head = head
        self.label = label
        self.dependent = dependent
    
class SRLPredicate(NIKLJSON):
    def __init__(self, form: str, begin: int, end: int, lemma: str, sense_id: int):
        self.form = form
        self.begin = begin
        self.end = end
        self.lemma = lemma
        self.sense_id = sense_id

class SRLArgument(NIKLJSON):
    def __init__(self, form: str, label: str, begin: int, end: int):
        self.form = form
        self.label = label
        self.begin = begin
        self.end = end

class SRL(NIKLJSON):
    """
    SRL (Semantic Role Labeling)
    
    consists of a predicate and a list of arguments::
    
        >>> SRL(SRLPredicate(), [SRLArgument()])
    """
    def __init__(self, predicate: SRLPredicate, argument: []):
        """
        :param argument: list(SRLArgument)
        
        ``argument`` is a list of Argument.
        """
        self.predicate = predicate
        self.argument = argument



class CRMention(NIKLJSON):
    def __init__(self, form : str, NE_id : int, sentence_id : int, begin : int, end : int):
        self.form = form
        self.NE_id = NE_id
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end

class CR(NIKLJSON):
    """
    CR (Cross Reference)
    """
    def __init__(self, mention: list(CRMention)):
        """
        """
        self.mention = mention


class ZAPredicate(NIKLJSON):
    def __init__(self, form: str, sentence_id: int, begin: int, end: int):
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end

class ZAAntecedent(NIKLJSON):
    def __init__(self, type: str, form: str, sentence_id: int, begin: int, end: int):
        self.type = type
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        
class ZA(NIKLJSON):
    def __init__(self, predicate: ZAPredicate, antecedent: list(ZAAntecedent)):
       self.predicate = predicate
       self.antecedent = antecedent
