#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import gdb
import graph_tool.all
import sortedcontainers
import re

_arch = None


def _block_key(block):
    return (block.start, block.end, block.is_global, block.is_static)


class BlockGraph(object):

    def __init__(self, linetable=None):
        if linetable is None:
            self._linetable = gdb.selected_frame().find_sal().symtab.linetable()
        else:
            self._linetable = linetable
        self._network = graph_tool.Graph(directed=True)
        self._block_property = self._network.new_vertex_property("python::object")
        self._network.vertex_properties.label = self._network.new_vertex_property("string")
        self._blocks = dict()
        self._lookupVertex = dict()
        self._extract_all_blocks()
        self._build_block_graph()
        self._disassembly = dict()
        for key, block in self._blocks.items():
            self._disassembly[key] = map_block(block)

        for key, asmMap in self._disassembly.items():
            for line, instrs in asmMap.items():
                for pc, instr in instrs.items():
                    print(str(line) + "\t" + instr)

    def _extract_all_blocks(self):
        for entry in self._linetable:
            block = gdb.block_for_pc(entry.pc)
            self._add_block_to_graph(block)

    def _add_block_to_graph(self, block):
        key = _block_key(block)
        if key in self._blocks:
            return None
        self._blocks[key] = block
        v = self._network.add_vertex()
        self._block_property[v] = block
        self._network.vertex_properties.label[v] = self._block_label(key, block)
        self._lookupVertex[key] = v
        for symbol in block:
            childV = self._network.add_vertex()
            self._block_property[childV] = None
            self._network.vertex_properties.label[childV] = self._symbol_label(symbol)
            self._network.add_edge(v, childV)
        if block.global_block is not None:
            self._add_block_to_graph(block.global_block)
        if block.static_block is not None:
            self._add_block_to_graph(block.static_block)
        return v

    def _print_all_symbols(self):
        for key, block in self._blocks.items():
            print(self._block_label(key, block))
            for sym in block:
                print("  ", sym.name)

    @classmethod
    def _block_label(cls, key, block):
        if block.function is not None:
            return block.function.name
            # return block.function.name + " :: " + hex(key[0]) + " to " + hex(key[1])
        else:
            if block.is_static:
                return "static"
                print("labeled static block")
            elif block.is_global:
                print("labeled global block")
                return "global"
            else:
                return "no block name"
            # return " no block name :: " + hex(key[0]) + " to " + hex(key[1])

    @classmethod
    def _symbol_label(cls, symbol):
        if symbol.type.name is not None:
            return symbol.type.name + " " + symbol.name
        else:
            return "(?)" + symbol.name

    def _build_block_graph(self):
        queue = list(self._blocks.items())
        while queue:
            key, block = queue.pop()
            if block.superblock is None:
                continue
            superblock = block.superblock
            superblockKey = _block_key(superblock)
            if superblockKey not in self._blocks:
                parent = self._add_block_to_graph(superblock)
                queue.append((superblockKey, superblock))
            else:
                parent = self._lookupVertex[superblockKey]
            child = self._lookupVertex[key]
            self._network.add_edge(parent, child)

    def save(self, filename="blockgraph.dot"):
        self._network.save(filename)


def disassemble_block(block=None):
    global _arch
    if block is None:
        _block = gdb.selected_frame().block()
    else:
        _block = block
    if _arch is None:
        _arch = gdb.selected_frame().architecture()
    return _arch.disassemble(_block.start, _block.end)


def map_block(block=None):
    disas = disassemble_block(block)
    lineDict = dict()
    for entry in disas:
        sal = gdb.find_pc_line(entry["addr"])
        if sal.line not in lineDict:
            lineDict[sal.line] = dict()
        lineDict[sal.line][sal.pc] = entry["asm"]
    return lineDict









