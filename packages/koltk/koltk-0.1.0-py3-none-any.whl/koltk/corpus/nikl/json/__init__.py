r"""NIKLJSON


::
    >>> from koltk.corpus.nikl.json import *
::

    corpus
        list(document)
            id
            metadata
                title
                author
                publisher
                date
                topic
                url
            list(sentence)
                id
                form
                list(word) : id, form, begin, end
                list(morpheme) : id, form, label, word_id, position
                list(WSD) : word, sense_id, pos, begin, end
                list(NE) : id, form, label, begin, end
                list(DP) : word_id, word_form, head, label, dependent
                list(SRL)
                    predicte(form, begin, end, lemma)
                    list(argument) : Argument(form, label, begin, end)
            list(CR)
            list(ZA)



- Document
- Sentence
- Word(id, form, begin, end)
- Morpheme(id, form, label, word_id, position)
- WSD(word, sense_id, pos, begin, end)
- NE(id, form, label, begin, end)
- DP(word_id, word_form, head, label, dependent)
- SRL(predicate, argument)
  - Predicate(form, begin, end, lemma, sense_id)
  - Argument(form, label, begin, end)
- CR(mention)
  - Mention(form, ne_id, sentence_id, begin, end)
- ZA(predicate: Predicate, antecedent: list(Antecedent))
  - Predicate(form, sentence_id, begin, end)
  - Antecedent(type, form, sentence_id, begin, end)


"""
from .object import *
from .base import NIKLJSON
