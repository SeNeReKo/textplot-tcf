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
    def from_file(cls, path):
        """
        Read corpus from a TCF file.

        """
        # Since it is an XML file, read it in binary format.
        return cls(open(path, 'rb').read())

    def __init__(self, text):
        """
        Parse the annotated TCF file into a `TextCorpus`.

        """
        self.corpus = TextCorpus(text)
        self.text = self.corpus.text.text
        self.tokenize()

    def tokens_from_corpus(self):
        """
        Create a token stream in textplots dict format from a `TextCorpus`.

        """
        for offset, token in enumerate(self.corpus.tokens):
            yield { # Emit the token.
                'stemmed':      token.lemma,
                'unstemmed':    token.text,
                'offset':       offset,
                'left':         None,
                'right':        None,
            }

    def stopwords(self, path='stopwords.txt'):
        """
        Load a set of stopwords.

        Copied from textplot so the local stopword file is used.

        """
        path = os.path.join(os.path.dirname(__file__), path)
        with open(path) as f:
            return set(f.read().splitlines())

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
                token['stemmed'] in stopwords):
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