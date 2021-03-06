#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from .text import Text
from textplot.matrix import Matrix
from textplot.graphs import Skimmer


def frequent(path, term_depth=500, skim_depth=10, d_weights=False,
             stopwordfile=None, postags=None, disambiguate=False, **kwargs):

    """
    Use most frequent terms.
    """
    
    t = Text.from_file(path, stopwordfile=stopwordfile, postags=postags,
                       disambiguate=disambiguate)
    m = Matrix(t)

    print('Indexing terms:')
    m.index(t.most_frequent_terms(term_depth), **kwargs)

    g = Skimmer()

    print('Generating graph:')
    g.build(m, skim_depth, d_weights)

    return g