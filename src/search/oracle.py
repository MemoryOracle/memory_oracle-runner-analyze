#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import gdb
import memory.exception
import collections

import graph_tool.all as gt

class Oracle(object):

    _selectedFrame = gdb.selected_frame()
    _initialProcessor = True
    found = collections.deque()
    described = collections.deque()
    explored = set()
    arrays = dict()

    network = nx.DiGraph()

    _lookup = {
        gdb.TYPE_CODE_PTR: "Pointer",
        gdb.TYPE_CODE_ARRAY: "Array",
        gdb.TYPE_CODE_STRUCT: "Struct",
        gdb.TYPE_CODE_UNION: "Union",
        gdb.TYPE_CODE_ENUM: "Enum",
        gdb.TYPE_CODE_FUNC: "Function",
        gdb.TYPE_CODE_INT: "Int",
        gdb.TYPE_CODE_FLT: "Float",
        gdb.TYPE_CODE_VOID: "Void",
        gdb.TYPE_CODE_STRING: "String",
        gdb.TYPE_CODE_ERROR: "TypeDetectionError",
        gdb.TYPE_CODE_METHOD: "Method",
        gdb.TYPE_CODE_METHODPTR: "MethodPointer",
        gdb.TYPE_CODE_MEMBERPTR: "MemberPointer",
        gdb.TYPE_CODE_REF: "Reference",
        gdb.TYPE_CODE_CHAR: "Character",
        gdb.TYPE_CODE_BOOL: "Bool",
        gdb.TYPE_CODE_COMPLEX: "ComplexFloat",
        gdb.TYPE_CODE_TYPEDEF: "AliasedAddressable",
        gdb.TYPE_CODE_NAMESPACE: "Namespace",
        gdb.TYPE_CODE_INTERNAL_FUNCTION: "DebuggerFunction",
    }

    knownIndexes = set()


    @classmethod
    def _extract_symbols(cls):
        try:
            for symbol in cls._selectedFrame.block():
                try:
                    foundObj = dict()
                    foundObj["value"] = symbol.value(Oracle._selectedFrame)
                    foundObj["name"] = symbol.name
                    foundObj["parent"] = None
                    foundObj["is_valid"] = symbol.is_valid()
                    foundObj.update(cls._extract(foundObj["value"]))
                    cls.found.append(foundObj)
                except memory.exception.AlreadyFound:
                    continue
        except RuntimeError as e:
            gdb.write(str(e))

    @classmethod
    def _extract(cls, v):
        foundObj = dict()
        foundObj["frame"] = str(Oracle._selectedFrame)
        foundObj["address"] = str(v.address)
        foundObj["type"] = cls.true_type_name(v.type)
        foundObj["tag"] = v.type.tag
        foundObj["type_code"] = v.type.code
        addr = foundObj["address"]
        code = foundObj["type_code"]
        index = (code, addr, foundObj["type"])
        foundObj["index"] = index
        if index not in Oracle.knownIndexes:
            Oracle.knownIndexes.add(index)
            # gdb.write("Found index " + Oracle._lookup[index[0]] + " " + index[1] + "\n")
        else:
            # gdb.write("Already knew " + Oracle._lookup[index[0]] + " " + index[1] + "\n")
            raise memory.exception.AlreadyFound("Already found index " + str(index))
        return foundObj


    #hack!
    @staticmethod
    def true_type_name(typ):
        t = typ.strip_typedefs()
        typeName = collections.deque()
        while t.code in {gdb.TYPE_CODE_PTR, gdb.TYPE_CODE_ARRAY}:
            if t.code == gdb.TYPE_CODE_ARRAY:
                start, end = t.range()
                typeName.append("[" + str(end - start) + "]")
            elif t.code == gdb.TYPE_CODE_PTR:
                typeName.append("*")
            t = t.target()

        name = t.name

        while len(typeName):
            name += typeName.pop()

        return name
