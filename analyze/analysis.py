#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import gdb
# import gdb.types
import re
import time
import graph_tool.all as gt






class x86_64(object):

    @staticmethod
    def get_arg(num):
        return int(gdb.selected_frame().read_register(['rdi', 'rsi'][num]))

    @staticmethod
    def get_ret():
        return int(gdb.selected_frame().read_register('rax'))


class NewFinishBreak(gdb.FinishBreakpoint):

    def __init__(self, size):
        super(NewFinishBreak, self).__init__(internal=True)
        self.size = size
        self.silent = True

    def stop(self):
        addr = x86_64.get_ret()
        NewBreak.allocated[addr] = self.size
        Oracle.explored.discard(addr)
        return False


class NewBreak(gdb.Breakpoint):

    allocated = dict()

    def __init__(self, internal=True, temporary=False):
        super(NewBreak, self).__init__("operator new", internal=internal, temporary=temporary)
        self.silent = True

    def stop(self):
        size = x86_64.get_arg(0)
        fb = NewFinishBreak(size)
        return False


class NewArrayBreak(gdb.Breakpoint):

    def __init__(self, internal=True, temporary=False):
        super(NewArrayBreak, self).__init__("operator new[]", internal=internal, temporary=temporary)
        self.silent = True

    def stop(self):
        size = x86_64.get_arg(0)
        # gdb.write("Broke on array allocation of size " + str(size) + "\n")
        fb = NewFinishBreak(size)
        return False

# b = NewBreak()
b2 = NewArrayBreak()
