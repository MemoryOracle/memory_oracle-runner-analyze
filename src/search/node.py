#!/usr/bin/env python
# -*- encoding UTF-8 -*-


class NodeClassification(object):

    _key = 0

    def __init__(self, obj):
        self.object = obj

    def build_memory(self, instance):
        raise NotImplementedError()

    @classmethod
    def key(cls):
        return cls._key


class ValueAdaptor(SpeciesAdaptor):

    _key = 159174462870776748034522926590157110402

    def build_memory(self)

