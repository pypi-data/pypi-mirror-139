r"""NIKL ANnotated Corpus JSON (Niklanson) Objects

.. code-block::

  Corpus
    CorpusMetadata
    DocumentList
      Document
        DocumentMetadata
        SentenceList
          Sentence
            WordList, Word
            MorphemeList, Morpheme
            WSDList, WSD
            NEList, NE
            DPList, DP
            SRLList, SR
        ZAList, ZA
        CRList, CR



"""


from __future__ import annotations
from .base import Niklanson, NiklansonList
import re
import json

class CorpusMetadata(Niklanson):
    def __init__(self,
                 parent: Corpus = None,
                 title: str = '',               # required
                 creator: str = '',             # required
                 distributor: str = '',         # required
                 year: str = '',                # required
                 category: str = '',            # required
                 annotation_level = [],         # required
                 sampling: str = '',            # required for news, written, spoken, web
                 **kwargs):
        super().__init__(parent=parent)
        self.title = title
        self.creator = creator
        self.distributor = distributor
        self.year = year
        self.category = category
        self.annotation_level = annotation_level
        self.sampling = sampling
        self.update(kwargs)
    
class Corpus(Niklanson):
    """Corpus: the top level object.

    - id
    - :class:`.CorpusMetadata`
    - :class:`.DocumentList`

    JSON:
    
    .. code-block:: json
      
      {
        "id" : "",
        "metadata" : {},
        "document" : []
      }
    
    Args:
        corpus (Corpus) : corpus
    

    Example:
    
    .. code-block:: python

        Corpus()
        Corpus(id=None, metadata=None, document=[])

    """
    def __init__(self,
                 id: str = None,
                 metadata : {} = {},
                 document: [] = [],
                 **kwargs):
        self.id = id
        self.metadata = CorpusMetadata(**metadata)
        self.document = DocumentList(document, parent=self)
        self.update(kwargs)

    @classmethod
    def strict(cls, id, metadata, document):
        return cls(id, metadata, document)
        
    @property
    def document_list(self):
        """ :class:`.DocumentList`
        """
        #if self.document_list is None:
        #    self.__document_list = DocumentList(self.__json['document'])

        return self.document

    def __repr__(self):
        return 'Corpus(id={})'.format(self.id)

class DocumentMetadata(Niklanson):
    def __init__(self,
                 parent: Document = None,
                 title : str = '',            # required
                 author : str = '',           # required
                 publisher : str = '',        # required
                 date : str = '',             # required
                 topic : str = '',            # required for news, spoken, messenger
                 url : str = None,            # optional attribute
                 **kwargs):
        super().__init__(parent=parent)
        self.title = title 
        self.author = author
        self.publisher = publisher
        self.date = date
        self.topic = topic
        if url is not None: self.url = url
        self.update(kwargs)

    @classmethod
    def strict(title, author, publisher, date, topic, url):
        return cls(title, author, publisher, date, topic, url)
    
class Document(Niklanson):
    """
    Document()

    ::

        >>> d = Document(id='X200818')
      
    """
    def __init__(self,
                 parent = None,
                 id = None,
                 metadata = {},
                 sentence = [],
                 **kwargs):
        super().__init__(parent=parent)
        self.id = id
        self.metadata = DocumentMetadata.from_dict(metadata, parent=self)
        self.sentence = SentenceList(sentence, parent=self)
        for name, value in kwargs.items():
            if name == 'CR' : self.CR = CRList(value, parent=self)
            elif name == 'ZA' : self.ZA = ZAList(value, parent=self)
            else: setattr(self, name, value)

    @classmethod
    def strict(cls, id=None, metadata={}, sentence = [], CR = [], ZA = []):
        return cls(id, metadata, sentence, CR, ZA)

    @property
    def fwid(self):
        toks = self.id.split('.')
        if len(toks) == 1:
            # This option (for 2019 spoken annotated corpus) will be deprecated.
            #
            # - (2019 spoken annotated corpus) document id example: SARW180000004
            # - (2020 version) document id example: SARW180000004.1
            #
            return '{}-0001'.format(toks[0])
        elif len(toks) == 2:
            return '{}-{:04d}'.format(toks[0], int(toks[1]))
        else:
            raise Exception('document id error: {}'.format(self.id))
   
    @property
    def sentence_list(self):
        return self.sentence
        
    @property
    def za_list(self):
        return self.ZA
  
    @property
    def cr_list(self):
        return self.CR
  
    def __repr__(self):
        return 'Document(id={})'.format(self.id)
    
    def __str__(self):
        return json.dumps(self, ensure_ascii=False)

    def getSentenceById(self, sentence_id):
        if not hasattr(self, '__sentence_id2index'):
            self.__sentence_id2index = {}
            for i, sent in enumerate(self.sentence_list):
                self.__sentence_id2index[sent.id] = i
                
        return self.sentence_list[self.__sentence_id2index[sentence_id]]

 
class DocumentList(NiklansonList):
    element_type = Document
    
   
class Sentence(Niklanson):
    """
    Sentence(id, form)

    ::

        >>> s = Sentence('X200818', '아이들이 책을 읽는다.')
   """
    def __init__(self,
                 parent: Document = None,
                 num: int = None,
                 id: str = None,
                 form: str = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.__num = num
        self.id = id
        self.form = form
        for name, value in kwargs.items():
            if name == 'word' : self.word = WordList(value, parent=self)
            elif name == 'morpheme' : self.morpheme = MorphemeList(value, parent=self)
            elif name == 'WSD' : self.WSD = WSDList(value, parent=self)
            elif name == 'NE' or name == 'ne' : self.NE = NEList(value, parent=self)
            elif name == 'DP' : self.DP = DPList(value, parent=self)
            elif name == 'SRL' : self.SRL = SRLList(value, parent=self)
            else: setattr(self, name, value)

    @classmethod
    def strict(cls, id, form, word, morpheme, WSD, NE, DP, SRL):
        return cls(id, form, word, morpheme, WSD, NE, DP, SRL)

    @property
    def word_list(self):
        if not hasattr(self, 'word'):
            self.word = []
            b = 0
            for i, wform in enumerate(self.form.split()):
                e = b + len(wform)
                self.word.append(Word(parent=self, id=i + 1, form=wform, begin=b, end=e))
                b = e + 1

        return self.word
    
    @property
    def morpheme_list(self):
        return self.morpheme
    
    @property
    def wsd_list(self):
        return self.WSD
        
    @property
    def ne_list(self):
        return self.NE
  
    @property
    def dp_list(self):
        return self.DP
  
    @property
    def srl_list(self):
        return self.SRL
  
    def __init_word_list_from_sentence_form(self):
        self.__word_list = []
        beg = 0
        i = 0
       
        for tok in re.split('(\s+)', self.form):
            if tok == '' : continue
            elif re.match('\s', tok[0]) : beg += len(tok)
            else:
                i += 1
                self.word.append(Word(i, tok, beg, beg + len(tok))) 
                beg += len(tok)
                
    @property
    def fwid(self):
        toks = self.id.split(".")
        if len(toks) == 2:
            # This option (for 2019 spoken annotated corpus) will be deprecated.
            #
            # - (2019 spoken annotated corpus) sentence id example: SARW180000004.3
            # - (2020 version) document id example: SARW180000004.1.1.3
            #
            docid, sentnum = toks
            fw_sid = "{}-{:04d}-{:05d}-{:05d}".format(docid, 1, 1, int(sentnum))
        elif len(toks) == 4:
            corpusid, docnum, paranum, sentnum = toks
            fw_sid = "{}-{:04d}-{:05d}-{:05d}".format(corpusid, int(docnum), int(paranum), int(sentnum))
        else:
            sys.exit(sid)

        return fw_sid

    @property
    def snum(self):
        """snum: sentence number prefixed with 's'
        """
        return 's{}'.format(self.__num)

    def __repr__(self):
        return 'Sentence(id={}, form={})'.format(self.id, self.form)
        

    def wordAt(self, charind):
        if not hasattr(self, '__charind2wordid'):
            self.__charind2wordid = [None] * len(self.form) 
            for i, w in enumerate(self.word_list):
                self.__charind2wordid[w.slice] = [w.id] * len(w.form)

        try:
            return self.word_list[self.__charind2wordid[charind] - 1]
        except:
            raise Exception('No word at {}: {}'.format(charind, self.form))

class SentenceList(NiklansonList):
    element_type = Sentence

    def __init__(self, sentence_dic_list, parent=None):
        """
        @param sentence_dic_list: a list of dict. 
        a dict is { id, form }
        """
        self.__parent = parent
        for i, s in enumerate(sentence_dic_list):
            list.append(self, Sentence(**s, parent=parent, num=i+1))
    
        
    @property
    def parent(self):
        return self.__parent
    
            
class Word(Niklanson):
    """
    Word
    """
    def __init__(self,
                 parent: Sentence = None,
                 id : int = None,
                 form : str = None,
                 begin : int = None,
                 end : int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.id = id
        self.form = form
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, id: int, form: str, begin: int, end: int):
        return cls(id, form, begin, end)
   
    @property
    def gid(self):
        return '{}_{:03d}'.format(self.parent.fwid, self.id)

    @property
    def swid(self):
        return '{}_{}'.format(self.parent.snum, self.id)

    def neighborAt(self, relative_index, default=None):
        """
        Return the neighbor word at the relative_index. Or default if index is out of range.

        :param relative_index:
          eg) +1 for the next word, -1 for the previous word
        
        :return: a Word object
        """
        ind = self.id - 1 + relative_index
        
        if 0 <= ind < len(self.parent.word_list) :
            return self.parent.word_list[ind]
        else:
            return default

    def neighbors(self, first=None, last=None):
        """
        Return list of the neighbor words from first to last.
        
       :param first: relative index of the first word
       :param last: relative index of the last word
        """
        ind1 = max(0, self.id - 1 + first) if first is not None else 0
        ind2 = self.id - 1 + last if last is not None else len(self.parent.word_list)
        return self.parent.word_list[ind1:(ind2+1)]

        
    @property
    def prev(self):
        return self.neighborAt(-1)

    @property
    def next(self):
        return self.neighborAt(1)

    def __next__(self):
        n = self.neighborAt(1)
        if n is None:
            raise StopIteration
        else:
            return n

    def __iter__(self):
        return self
    
class WordList(NiklansonList):
    element_type = Word

   

class Morpheme(Niklanson):
    """Morpheme
    """
    def __init__(self,
                 parent: Sentence = None,
                 id : int = None,
                 form: str = None,
                 label : str = None,
                 word_id : int = None,
                 position : int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.id = id
        self.form = form
        self.label = label
        self.word_id = word_id
        self.position = position
        self.update(kwargs)

    @classmethod
    def strict(cls, id, form, label, word_id, position):
        return cls(id, form, label, word_id, position)

    @property
    def str(self):
        if not hasattr(self, '__str'):
            self.__str = self.form + '/' + self.label

        return self.__str

class MorphemeList(NiklansonList):
   element_type = Morpheme 
 

class WSD(Niklanson):
    """
    WSD (Word Sense Disambiguation)
    """
    def __init__(self,
                 parent: Sentence = None,
                 word: str = None,
                 sense_id: int = None,
                 pos : str = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.word = word
        self.sense_id = sense_id
        self.pos = pos
        self.begin = begin
        self.end = end
        self.update(kwargs)
        
    @property
    def str(self):
        return '{}__{:03d}/{}'.format(self.word, self.sense_id, self.pos)

   
class WSDList(NiklansonList):
    element_type = WSD
       

class NE(Niklanson):
    """
    NE (Named Entity)
    """
    def __init__(self,
                 parent: Sentence = None,
                 id: int = None,
                 form: str = None,
                 label: str = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.id = id
        self.form = form
        self.label = label
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, id, form, label, begin, end):
        return cls(id, form, label, begin, end)

    @property
    def str(self):
        return '{}/{}'.format(self.form, self.label)
    
class NEList(NiklansonList):
    element_type = NE



class DP(Niklanson):
    """
    DP (Denpendency Parsing)
    """
    def __init__(self,
                 parent: Sentence = None,
                 word_id: int = None,
                 word_form: str = None,
                 head: int = None,
                 label: str = None,
                 dependent: list[int] = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.word_id = word_id
        self.word_form = word_form
        self.head = head
        self.label = label
        self.dependent = dependent
        self.update(kwargs)
        self.__dependent_nodes = None

    @property
    def head_node(self):
        if self.head != -1:
            return self.parent.dp_list[self.head - 1]
        else:
            return None
        
    @property
    def dependent_nodes(self):
        if self.__dependent_nodes is None:
           self.__dependent_nodes = []
           for d in self.dependent:
               self.__dependent_nodes.append(self.parent.dp_list[d - 1])

        return self.__dependent_nodes

    @property
    def prev_node(self):
        try:
            return self.parent.dp_list[self.word_id - 2]
        except IndexError:
            return None

    @property
    def next_node(self):
        try:
            return self.parent.dp_list[self.word_id]
        except IndexError:
            return None
        
        
class DPList(NiklansonList):
    element_type = DP

    @property
    def root_word_id(self) :
        for dp in self:
            if dp.head == -1:
                return dp.word_id

    @property
    def heads(self):
        if not hasattr(self, '_heads'):
            self._heads = []
            for dp in self:
                self._heads.append(dp.head)

        return self._heads
      
class SRLPredicate(Niklanson):
    def __init__(self,
                 parent: SRL = None,
                 form: str = None,
                 begin: int = None,
                 end: int = None,
                 lemma: str = None,
                 sense_id: int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.form = form
        self.begin = begin
        self.end = end
        self.lemma = lemma
        self.sense_id = sense_id
        self.update(kwargs)

    @classmethod
    def strict(cls, form: str, begin: int, end: int, lemma: str, sense_id: int):
        return cls(form, begin, end, lemma, sense_id) 

    @property
    def str(self):
        return '{}__{}'.format(self.lemma, self.sense_id)

    @property
    def first_word(self):
        if not hasattr(self, '__first_word'):
            self.__first_word = self.parent.parent.wordAt(self.begin)

        return self.__first_word
        
    @property
    def last_word(self):
        if not hasattr(self, '__last_word'):
            last_word_form = self.form.split()[-1]
            self.__last_word = self.parent.parent.wordAt(self.end - len(last_word_form))

        return self.__last_word



class SRLArgument(Niklanson):

    def __init__(self,
                 parent: SRL = None,
                 form: str = None,
                 label: str = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.form = form
        self.label = label
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, form: str, label: str, begin: int, end: int):
        return cls(form, label, begin, end)

    @property
    def str(self):
        return '{}/{}'.format(self.form.split()[-1], self.label)

    @property
    def first_word(self):
        if not hasattr(self, '__first_word'):
            self.__first_word = self.parent.parent.wordAt(self.begin)

        return self.__first_word
        
    @property
    def last_word(self):
        if not hasattr(self, '__last_word'):
            last_word_form = self.form.split()[-1]
            self.__last_word = self.parent.parent.wordAt(self.end - len(last_word_form))

        return self.__last_word

class SRLArgumentList(NiklansonList):
    element_type = SRLArgument

class SRL(Niklanson):
    """
    SRL (Semantic Role Labeling)
    
    consists of a predicate and a list of arguments::
    
        >>> SRL()
        >>> SRL(predicate={}, argument=[{}, {}])
    """
    def __init__(self,
                 parent: Sentence = None,
                 predicate: {} = {},
                 argument: [] = [],
                 **kwargs):
        super().__init__(parent=parent)
        self.predicate = SRLPredicate(**predicate, parent=self)
        self.argument = SRLArgumentList(argument, parent=self)
        self.update(kwargs)
        
    @classmethod
    def strict(cls, predicate: {}, argument: []):
        """
        """
        return cls(predicate, argument)

    @property
    def argument_list(self):
        return self.argument
    
class SRLList(NiklansonList):
    element_type = SRL
    
    
class CRMention(Niklanson):
    def __init__(self,
                 parent: CR = None,
                 form : str = None,
                 NE_id : int = None,
                 sentence_id : str = None,
                 begin : int = None,
                 end : int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.form = form
        self.NE_id = NE_id
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, form: str, sentence_id: str, being: int, end: int, NE_id : int):
        return cls(form, sentence_id, begin, end, NE_id)

class CRMentionList(NiklansonList):
    element_type = CRMention
    
class CR(Niklanson):
    """
    CR (Cross Reference)
    
    mention: list of mentions
    """
    def __init__(self,
                 parent: Document = None,
                 mention: [] = [],
                 **kwargs):
        """
        """
        super().__init__(parent=parent)
        self.mention = CRMentionList(mention, parent=self)
        self.update(kwargs)

    @classmethod
    def strict(cls, mention: []):
        return cls(mention)

    @property
    def mention_list(self):
        return self.mention
 
class CRList(NiklansonList):
    element_type = CR

class ZAPredicate(Niklanson):
    def __init__(self,
                 parent: ZA = None,
                 form: str = None,
                 sentence_id: int = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, form, sentence_id, begin, end):
        return cls(form, sentence_id, begin, end)

class ZAAntecedent(Niklanson):
    def __init__(self,
                 parent: ZA = None,
                 form: str = None,
                 type: str = None,
                 sentence_id: int = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        super().__init__(parent)
        self.type = type
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        self.update(kwargs)
        
    @classmethod
    def strict(cls, form, type, sentence_id, begin, end):
        return cls(form, type, sentence_id, begin, end)

class ZAAntencedentList(NiklansonList):
    element_type = ZAAntecedent
        
class ZA(Niklanson):
    def __init__(self,
                 parent: Document = None,
                 predicate: {} = {},
                 antecedent: [] = [],
                 **kwargs):
        
        super().__init__(parent)
        self.predicate = ZAPredicate(**predicate)
        self.antecedent = ZAAntencedentList(antecedent)

    @classmethod
    def strict(predicate: {}, antecedent: []):
        return cls(predicate, antecedent)
   
class ZAList(NiklansonList):
    element_type = ZA
