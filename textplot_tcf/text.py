#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict

from textplot.text import Text as Text_
from tcflib.tcf import TextCorpus

class Text(Text_):
    """
    Implementation of `textplot.Text` that reads an annotated text in TCF
    format instead of processing plain text.

    """

    @classmethod
    def from_file(cls, path, **kwargs):
        """
        Read corpus from a TCF file.

        """
        # Since it is an XML file, read it in binary format.
        return cls(open(path, 'rb').read(), **kwargs)

    def __init__(self, text, stopwordfile=None, postags=None,
                 disambiguate=False):
        """
        Parse the annotated TCF file into a `TextCorpus`.
        
        :param stopwordfile: The stopword file, one stopword per line.
            If `stopwordfile` is None, the default stopword file is used.
            If `stopwordfile` is an empty string (``''``), no stopword list is
            used.
        :param postags: List of MAF part-of-speech tags that are taken into
            account.
        :param disambiguate: Use wordsenses information from TCF to
            disambiguate lemmas.

        """
        self.stopwordfile = stopwordfile
        
        self.postags = postags
        layers = ['text', 'tokens', 'lemmas']
        if self.postags:
            from tcflib.tagsets import TagSet
            self.tagset = TagSet('DC-1345')
            self.postags = [self.tagset[tag] for tag in postags]
            layers.append('POStags')
            
        self.disambiguate = disambiguate
        if self.disambiguate:
            layers.append('wsd')
        
        self.corpus = TextCorpus(text, layers=layers)
        self.text = self.corpus.text.text

        self.tokenize()

    def tokens_from_corpus(self):
        """
        Create a token stream in textplots dict format from a `TextCorpus`.

        """
        for offset, token in enumerate(self.corpus.tokens):
            if self.disambiguate:
                stemmed = '{} ({})'.format(token.lemma,
                                           ', '.join(token.wordsenses))
            else:
                stemmed = token.lemma
            yield { # Emit the token.
                'stemmed':      stemmed,
                'unstemmed':    token.text,
                'offset':       offset,
                'left':         None,
                'right':        None,
                'tcftoken':     token,
            }

    def stopwords(self, path='stopwords.txt'):
        """
        Load a set of stopwords.

        Copied from textplot so the local stopword file is used.

        """
        if self.stopwordfile == '':
            return []
        elif self.stopwordfile is None:
            path = os.path.join(os.path.dirname(__file__), path)
        else:
            path = self.stopwordfile
        with open(path) as f:
            return set(f.read().splitlines())

    def test_pos(self, token):
        """
        Test if token has one of the allowed POS tags.
        
        """
        if not self.postags:
            # Do not test, always return True.
            return True
        token = token['tcftoken']
        for postag in self.postags:
            if token.postag.is_a(postag):
                return True
        return False

    def tokenize(self):
        """
        Tokenize the text and filter the token stream.

        """
        self.tokens = []
        self.terms = OrderedDict()
        # Load stopwords.
        stopwords = self.stopwords()

        # Generate tokens.
        for token in self.tokens_from_corpus():
            # Ignore stopwords.
            if (token['unstemmed'] in stopwords or 
                token['stemmed'] in stopwords or
                not self.test_pos(token)):
                self.tokens.append(None)
            else:
                # Token:
                self.tokens.append(token)
                # Term:
                offsets = self.terms.setdefault(token['stemmed'], [])
                offsets.append(token['offset'])

    def unstem(self, term):
        """
        Since this implementation uses lemmas instead of stems, it is not
        neccessary to unstem terms.

        """
        return term