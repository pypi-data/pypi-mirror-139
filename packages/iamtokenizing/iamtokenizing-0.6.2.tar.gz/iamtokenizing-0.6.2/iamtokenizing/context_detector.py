#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ContextTokenization class allows to tokenize a part of a string into a context.
The context is the left and right parts around a token.
"""

from tokenspan import Span

from .base_tokenizer import BaseTokenizer
from .base_tokenizer import _warning_tokens
from . import NGrams
from . import RegexDetector

class ContextDetector(BaseTokenizer):
    """
ContextDetector class allows splitting of a big text into chunks given by the `splitter` REGEX parameter of the `tokenize` method, then it detects the `selector` REGEX  inside each chunk, and associates the context to each of the detection. The context are given by the sub-strings in between different detections. By default `ContextDetector` detects digits inside sentence (or paragraph, that is, part of the string separated by newline character).
    """

    def __init__(self,
                 string=str(),
                 subtoksep=chr(32),
                 ranges=None,
                 ):
        """
ContextDetector has all the parameters of a Span object, namely `string` (the string to be tokenized), a `subtoksep` that will be inserted between the different sub-tokens of a Span object (default is a free space), and a `ranges` list of range objects. 

The different attributes will store : 
    - `context`: all the NGrams that represent the splitter selection (macro token)
    - `tokens` : all the ContextDetector.s instances that represent the selector selection (micro token)
    - `context_left`: the NGrams left to the ContextDetector token
    - `context_right`: the NGRams right to the ContextDetector token
    - `context_parent`: the position into the `context` that represents the parent
        """
        if isinstance(string, ContextDetector):
            args = {k:v for k,v in string.__dict__.items() 
                    if k in ['string', 'subtoksep', 'ranges']}
        else:
            args = {'string': string, 'subtoksep': subtoksep, 'ranges': ranges}
        BaseTokenizer.__init__(self, **args)
        self.context = None
        self.context_left = None
        self.context_right = None
        self.context_parent = None
        return None
    
    def __call__(self, 
                 string=str(),
                 subtoksep=chr(32),
                 ranges=None,
                 splitter='\n+', 
                 selector='\d+',
                 splitter_flags=0,
                 selector_flags=0):
        """
Apply the `.tokenize` method to a new string. Returns a new `ContextDetector` instance. All parameters from `ContextDetector` and/or `ContextDetector.tokenize` are available, except `inplace`, which is always `False`.
        """
        ct = ContextDetector(string=str(string),
                             subtoksep=subtoksep,
                             ranges=ranges)
        return ct.tokenize(splitter=splitter,
                           selector=selector,
                           splitter_flags=0,
                           selector_flags=0,
                           inplace=False)
    
    def _append_token(self, position, detection, start, stop):
        """Append a ContextDetector to the tokens attribute"""
        ct = ContextDetector(detection)
        ct.context_parent = position
        ct.context_left = NGrams(string=detection.string,
                                 ranges=[range(start, detection.start),],
                                 subtoksep=detection.subtoksep)
        ct.context_right = NGrams(string=detection.string,
                                  ranges=[range(detection.stop, stop),],
                                  subtoksep=detection.subtoksep)
        self.tokens.append(ct)
        return None
    
    def _several_detections(self, position, context, detections):
        """Constructs the different tokens in case there are more than one detections"""
        start = context.start
        for detection1, detection2 in zip(detections[:-1], detections[1:]):
            self._append_token(position, detection1, start, detection2.start)
            start = detection1.stop
        self._append_token(position, detection2, start, context.stop)
        return None
    
    def tokenize(self, 
                 splitter='\n+', 
                 selector='\d+', 
                 inplace=True,
                 splitter_flags=0,
                 selector_flags=0):
        """
Detects the `selector` REGEX inside the parent string and associate a context to each detection, the context being given by the remaining parts of the tokens given by the `splitter` REGEX expressions.
`selector` uses the `RegexDetector` tokenization, and `splitter` uses the `NGrams` tokenization.

Parameters | Type | Details
--- | --- | --- 
`splitter` | str | the REGEX that will be used to split the complete string into context sub-strings.
`splitter_flags` | some REGEX flags | The flags that will be transmitted to the `NGrams.tokenize` method of the splitting. flags are inherited from `re` package, and can be combined using a pipe symbol, for instance `flags=re.DOTALL|re.MULTILINE` apply both DOTALL (special character '.' also accepts new line) and MULTILINE (special characters '^' and '$' match begining and end of each new line). By default `splitter_flags=0`.
`selector` | str | the REGEX that will be used to detect a part of the context string.
`selector_flags` | some REGEX flags | The flags that will be transmmitted to the `RegexDetector.tokenize` method of the detection. flags are inherited from `re` package, and can be combined using a pipe symbol, for instance `flags=re.DOTALL|re.MULTILINE` apply both DOTALL (special character '.' also accepts new line) and MULTILINE (special characters '^' and '$' match begining and end of each new line). By default `selector_flags=0`.
`inplace` | boolean | whether the method changes the object in place (`inplace=True`, by default) or returns a new object
        """
        if not inplace:
            self = ContextDetector(self)
        contexts = NGrams(self)
        self.context = contexts.tokenize(regex=splitter, 
                                         inplace=False, 
                                         flags=splitter_flags)
        ranges_ = []
        for position, context in enumerate(self.context):
            detections = RegexDetector(context)
            detections = detections.tokenize(regex=selector, 
                                             inplace=False, 
                                             flags=selector_flags)
            ranges_.extend(detections.ranges)
            if len(detections.subspans) == 1:
                # works since detections.start = detections.ranges[0].start
                # and detections.stop = detections.ranges[-1].start
                # and len(detections.ranges) == 1
                self._append_token(position, detections, 
                                     context.start, context.stop)
            elif len(detections.subspans) > 1:
                self._several_detections(position, context, detections)
        self.ranges = ranges_
        return self
    
    @property
    def context_tokens(self):
        """Deprecated"""
        _warning_tokens()
        return self.tokens
