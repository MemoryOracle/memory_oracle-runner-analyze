#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import abc

# Not currently sure where this should go
# def run(self):
#
#     Oracle._extract_symbols()
#
#     searchers = [Searcher() for i in range(1)]
#
#     for searcher in searchers:
#         searcher.daemon = True
#         # searcher.start()
#         searcher.run()
#
#     gdb.write("Joined!\n")


class MemoryExtractor(metaclass=abc.ABCMeta):
    """
    Interface for memory extractors.
    """

    def run(self):
        """
        Start exploring.
        """
        raise NotImplementedError("run method not implemented")

    def extract_object(self, x):
        """
        Extract object x in the inferior.
        """
        raise NotImplementedError("extract_object method not implemented")

    ## I likely need to move this to a different interface.
    ## It is not really the extractor's job to articulate data to the oracle.
    # def describe_object(self, x):
    #     """
    #     Describe object x in the inferior.
    #     """
    #     raise NotImplementedError("describe_object method not implemented")

    def extract_array(self, x):
        """
        Extract an array in the inferior.
        """
        raise NotImplementedError("extract_array method not implemented")

    def extract_struct(self, x):
        """
        Extract a structure / class instance in the inferior.
        """
        raise NotImplementedError("extract_struct method not implemented")

    def extract_pointer(self, x):
        """
        Extract a pointer in the inferior
        """
        raise NotImplementedError("extract_pointer method not implemented")
