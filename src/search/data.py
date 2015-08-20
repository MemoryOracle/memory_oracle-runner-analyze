#!/usr/bin/env python
# -*- encoding UTF-8 -*-
"""
Interfaces and classes for debugee data submodule.

Contains GDBSpecies class, which implements the SpeciesInterface to identify
and assign a unique numeric code to each species within a program being
debugged by GDB.

Exceptions related to debugee data extraction.
"""

import re
import gdb
import gdb.types
import graph_tool.all
import graph_tool.search
import graph_tool.community
# import cProfile
# import re
# import traceback
import sortedcontainers
from uuid import uuid4 as unique_addr


class SpeciesIndex(object):
    """
    A static object which returns different codes for different "data species"
    found in the debugee.

    To be clear, "data species" is different from data type, although some
    overlap exists.  For instance, in C/C++ int is its own dataspecies, and its
    own data type.  But

    struct MyStruct{}

    and

    struct MyOtherStruct{}

    are the same data species (i.e. structure), while they are of different
    types (i.e. MyStruct and MyOtherStruct).

    In the case of the SpeciesIndex, the whole class is just a trivial
    wrappers around gdb.TYPE_CODE* type codes.

    The purpose of this class then is to establish the behavior of a species
    index now, making it simple to generalize other code to support different
    debuggers in the future (assuming that ever happens).
    """

    # Global

    """
    @return {int} Type detection error code
    """
    error = gdb.TYPE_CODE_ERROR

    """
    @return {int} internal debugger function type code.
    """
    internal_function = gdb.TYPE_CODE_INTERNAL_FUNCTION

    # C language and up

    """
    @return {int} array type code.
    """
    array = gdb.TYPE_CODE_ARRAY

    """
    @return {int} character type code.
    """
    character = gdb.TYPE_CODE_CHAR

    """
    @return {int} complex floating point number type code.
    """
    complex = gdb.TYPE_CODE_COMPLEX

    """
    @return {int} c style "enum" type code.
    """
    enum = gdb.TYPE_CODE_ENUM

    """
    @return {int} floating point number type code.
    """
    float = gdb.TYPE_CODE_FLT
    function = gdb.TYPE_CODE_FUNC

    """
    @return {int} integral number type code.
    """
    integer = gdb.TYPE_CODE_INT

    """
    @return {int} pointer type code.
    """
    pointer = gdb.TYPE_CODE_PTR

    """
    @return {int} structure / class type code.
    """
    struct = gdb.TYPE_CODE_STRUCT

    """
    @return {int} C/C++ typedef type code.
    """
    typedef = gdb.TYPE_CODE_TYPEDEF

    """
    @return {int} C/C++ style union type code.
    """
    union = gdb.TYPE_CODE_UNION

    """
    @return {int} no type / void type code.
    """
    void = gdb.TYPE_CODE_VOID

    # C++ language and up

    """
    @return {int} boolean type code.
    """
    boolean = gdb.TYPE_CODE_BOOL

    """
    @return {int} pointer to class data member type code.
    """
    member_pointer = gdb.TYPE_CODE_MEMBERPTR

    """
    @return {int} class method type code.
    """
    method = gdb.TYPE_CODE_METHOD

    """
    @return {int} pointer to class method type code.
    """
    method_pointer = gdb.TYPE_CODE_METHODPTR

    """
    @return {int} C++ style namespace type code.
    """
    namespace = gdb.TYPE_CODE_NAMESPACE

    """
    @return {int} C++ style reference type code.
    """
    reference = gdb.TYPE_CODE_REF

    """
    @return {int} C++ style std::string type code.
    @warning This is NOT for char[] or char* or anything like that.  Those
    will show up as array or pointer types (because they are).
    """
    string = gdb.TYPE_CODE_STRING

    frame = -1

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

    def __init__(self, *args, **kwargs):
        """
        Simply throw an error if someone attempts to init this class.
        """
        raise NotImplementedError("This is a pure static class!")


def species_code(obj):


def _extract_value(obj, frame=None):
    if isinstance(obj, gdb.Value):
        val = obj
    elif isinstance(obj, gdb.Symbol):
        if frame is not None:
            val = obj.value(frame)
        else:
            val = obj.value()
    elif isinstance(obj, gdb.Frame):
        val = obj.function().value(obj)
    else:
        raise ValueError("invalid obj of type: " + str(type(obj)))
    return val

def _extract_address(obj, frame=None):
    if isinstance(obj, (gdb.Value, gdb.Symbol)):
        val = _extract_value(obj, frame=frame).address
    elif isinstance(obj, gdb.Frame):
        val = obj.read_register(x86_64.stack_pointer)
    else:
        raise ValueError("invalid obj of type: " + str(type(obj)))
    return int(val) if val is not None else int(unique_addr())


class Node(object):

    def __init__(self, obj):
        self.classification = Node.compute_classification(obj)



class Memory(object):
    """

    A memory is a complete *exportable* description of a memory object (e.g. a
    named variable or a data structure) in the debugee at a particular point in
    the inferior's execution.

    """

    _ESCAPE = re.compile(r":")

    class _classification(object):
        frame = "frame"
        value = "value"
        symbol = "symbol"

    _EXTRACTABLE_TYPES = {
        SpeciesIndex.integer,
        SpeciesIndex.float,
        SpeciesIndex.boolean,
        SpeciesIndex.character,
        SpeciesIndex.string,
        SpeciesIndex.function
    }

    def __init__(self, raw, frame=None):
        """
        Extract raw in the debugee into a Description object.

        @param raw The gdb.Value in the debugee to be extracted.
        """

        self.address = _extract_address(raw, frame)
        if isinstance(raw, gdb.Value):
            self._init_from_value(raw)
            self.classification = Memory._classification.value
        elif isinstance(raw, gdb.Frame):
            self._init_from_frame(raw)
            self.classification = Memory._classification.frame
        elif isinstance(raw, gdb.Symbol):
            self._init_from_symbol(raw, frame=frame)
            self.classification = Memory._classification.symbol
        else:
            raise ValueError("invalid data type for raw")
        # self.value = Memory._ESCAPE.sub(r'\:', self.value)

    def _init_from_symbol(self, symbol, frame=None):
        if not symbol.needs_frame:
            self._init_from_value(symbol.value())
        elif frame is not None:
            self._init_from_value(symbol.value(frame))
        else:
            raise ValueError("can not gain value from symbol")
        self.name = symbol.name
        self.line = symbol.line

    def _init_from_value(self, value):
        self.is_optimized_out = value.is_optimized_out
        self.type_name = value.type.name
        self.dynamic_type_name = value.dynamic_type.name
        self.type_code = value.type.code
        if value.type.code in Memory._EXTRACTABLE_TYPES:
            # TODO: consider extracting value with more grace.
            # For example, ints as int, floats as float, and so forth.
            if self.dynamic_type_name:
                self.value = self.dynamic_type_name + " " + str(value)
            else:
                self.value = str(value)
        else:
            if self.dynamic_type_name:
                self.value = self.dynamic_type_name
            else:
                self.value = "@" + hex(self.address)
        self.name = None
        self.line = None

    def _init_from_frame(self, frame):
        function = frame.function()
        if function is not None:
            self._init_from_symbol(frame.function(), frame=frame)
        else:
            self.value = "UNKNOWN"
            self.dynamic_type_name = "[[[FRAME]]]"
            self.type_code = SpeciesIndex.frame
        stackPointer = hex(self.address)
        self.value = " ".join([self.value, "@FRAME<", stackPointer, ">"])
        frameName = frame.name()
        frameName = frameName if frameName is not None else "-unknown-"
        self.name = " ".join(["FRAME", frameName, "@", stackPointer])

    def is_real(self):
        return self.address is not None

    def is_null(self):
        return self.address == 0

    def id(self):
        return (self.type_code, self.name, self.type_name, self.address)

    def __hash__(self):
        return hash(self.id())

    def __eq__(self, rhs):
        return self.id() == rhs.id()


class AlreadyFound(Exception):
    """
    Exception to raise when an Extractor finds an item more than once.
    """
    pass


class BasicExtractor(graph_tool.search.AStarVisitor):

    """
    Specifically, Extractor instances must:

    * correctly remember objects which have already been extracted, and
    efficiently decide NOT to extract them again.
        - Instead, they create a Watcher object which emits updated information
          about the extracted data when the memory is written to or deleted,
          or when it goes out of scope.

    * not conflate objects with distinct Type or Species which happen to
    share an address in the debugee.  For instance, a int[2][2] object in a C
    program has *three* objects of *different* Type and Species which may share
    the same address, but which are *logically distinct* objects.  The
    int[2][2] object may have the same address as the first int[2] object
    within the two-dimensional array, which may share an address with the first
    int in the int[2] array.  Be careful not to skip objects when implementing
    this interface!

    * correctly note parent-child / source-target / ownership-owned by
    relationships which it may discover.  Specifically, "I found an int with
    abc value and xyz address" is not generally a sufficient extraction.  Other
    concerns exist:
        - Is the object a member variable of a larger struct?
        - Is the object a member of an array?
        - Does it live on the stack or the heap?
            - not sure about this requirement
    Basically, get all the useful information you can, and correctly fill out
    everything you can in the Description object you create.

    * never fail to call an appropriate method based on the *Species* of the
    data to be extracted.
        - In general, species is everything.  Unless you are making something
          "special purpose," (e.g. a Extractor targeted at standard
          library objects or something), do not make your extractor worry about
          the type of the object.  If you found an array of Foo or and array of
          Bar, that is mostly just "same stuff different day" to the
          Extractor.  As usual, Be as general and reusable as you can
          in your design.

    <not sure about this requirement yet>
    * correctly note circular access.
        - A trivial example is a pointer pointing to itself.  That may be
          silly, but it should not crash any part of MemoryOracle if it
          happens.
        - A more realistic example is a circular bug / feature in a linked
          list.  That happens all the time and may or may not be what the user
          is trying to do.  Thus it is important to note this kind of thing.
    """

    _MEMORIES = "memories"
    _WEIGHT = "edge weights"

    def __init__(self, network):
        self.network = network
        self.count = 0
        self.memories = network.new_vertex_property("python::object")
        self._edge_weights = self.network.new_edge_property("double")
        self.network.vertex_properties.label = self.network.new_vertex_property("string")
        self._community = self.network.new_vertex_property("long long")
        self._values = dict()
        # self.extracted = dict()
        self._handler = {
            SpeciesIndex.array: self._search_array,
            SpeciesIndex.struct: self._search_struct,
            SpeciesIndex.pointer: self._search_pointer
        }

    def discover_vertex(self, vertex):
        mem = self.memories[vertex]
        self.network.vertex_properties.label[vertex] = mem.value
        # print("labeled ", vertex, " with ", mem.value)

    def examine_vertex(self, vertex):
        mem = self.memories[vertex]
        if mem.type_code in self._handler:
            self._handler[mem.type_code](vertex)

    def finish_vertex(self, vertex):
        self.grey_nodes[vertex] = True
        # print(vertex, " marked as grey")


class x86_64(object):

    stack_pointer = "rsp"

    @staticmethod
    def get_arg(num):
        return int(gdb.selected_frame().read_register(['rdi', 'rsi'][num]))

    @staticmethod
    def get_ret():
        return int(gdb.selected_frame().read_register('rax'))

    @staticmethod
    def get_stack_pointer(frame=None):
        if frame is not None:
            return frame.read_register(x86_64.stack_pointer)
        else:
            return gdb.selected_frame().read_register(x86_64.stack_pointer)


class DynamicTracker(object):

    def __init__(self):
        self.allocated = dict()

    def allocate(self, key, size):
        if key not in self.allocated:
            self.allocated[key] = size
        else:
            raise ValueError("address already allocated")

    def is_allocated(self, key):
        return key in self.allocated

    def deallocate(self, key):
        del self.allocated[key]

    def list_addrs(self):
        return self.allocated.keys()


class TrackingBreak(gdb.Breakpoint):

    # _tracker = DynamicTracker()

    def __init__(self,
                 condition,
                 internal=True,
                 temporary=False):
        super(TrackingBreak, self).__init__(condition,
                                            internal=internal,
                                            temporary=temporary)
        self.silent = True

    def stop(self):
        # print("Tracking break stop")
        self.trigger()
        # size = x86_64.get_arg(0)
        # NewFinishBreak(size)
        return False

    @classmethod
    def track(cls, addr, size):
        cls.tracker.allocate(addr, size)

    def trigger(self):
        raise NotImplementedError("You must implement a trigger!")


class TrackingFinishBreak(gdb.FinishBreakpoint):

    def __init__(self, info, superior):
        super(TrackingFinishBreak, self).__init__(internal=True)
        self.info = info
        self.silent = True
        self.superior = superior

    def stop(self):
        self.trigger()
        # addr = x86_64.get_ret()
        # TrackingFinishBreak._SUPERIOR.track(addr, self.size)
        return False

    def trigger(self):
        raise NotImplementedError("You must implement a trigger!")


class DynamicMemoryTrackingBreak(TrackingBreak):

    tracker = DynamicTracker()


class NewTrackingBreak(DynamicMemoryTrackingBreak):

    def __init__(self):
        super(NewTrackingBreak, self).__init__("operator new[]")

    def trigger(self):
        size = x86_64.get_arg(0)
        NewTrackingFinishBreak(size)


class NewTrackingFinishBreak(TrackingFinishBreak):

    def __init__(self, info):
        super(NewTrackingFinishBreak, self).__init__(info, NewTrackingBreak)

    def trigger(self):
        addr = x86_64.get_ret()
        self.superior.track(addr, self.info)


class FunctionBreak(gdb.Breakpoint):

    _searcher = None

    def __init__(self, function):
        self.function = function
        super(FunctionBreak, self).__init__(self.function.name, internal=True)
        self.silent = True
        print("Search break configured for ", self.function.name)

    def stop(self):
        print("stopping to search within function ", self.function.name)
        FunctionBreak._searcher.search_new_frame(gdb.selected_frame())
        return False


class FunctionFinish(gdb.FinishBreakpoint):

    def __init__(self, functionName, frame):
        super(FunctionFinish, self).__init__(frame=frame, internal=True)
        self.silent = True
        self.functionName = functionName

    def stop(self):
        print(self.functionName, " returned with ", str(self.return_value))
        return False


class LocationQueue(object):

    _CACHE_LINE = 1024

    def __init__(self):
        self._queue = sortedcontainers.SortedDict()
        self._keys = self._queue.keys()

    def __iter__(self):
        return self

    def __next__(self):
        return self.dequeue()

    def dequeue(self):
        if not self._keys:
            raise StopIteration()
        else:
            return self._queue.popitem(last=False)[1]

    @classmethod
    def _compute_key(cls, obj, frame=None):
        return _extract_address(obj, frame=frame)

    def enqueue(self, obj, mem, vertex, frame):
        key = self._compute_key(obj, frame=frame)
        val = (obj, mem, vertex, frame)
        if key in self._queue:
            self._queue[key].append(val)
        else:
            self._queue[key] = [val]

    def not_empty(self):
        return not not self._keys


class MemoryGraph(object):

    def __init__(self):
        self._network = graph_tool.Graph(directed=True)
        self._network.vertex_properties.memories = \
            self._network.new_vertex_property("python::object")
        self._network.vertex_properties.label = \
            self._network.new_vertex_property("string")
        self._discovered_types = dict()
        self._queue = LocationQueue()
        self._handler = {
            SpeciesIndex.array: self._search_array,
            SpeciesIndex.struct: self._search_struct,
            SpeciesIndex.pointer: self._search_pointer,
            SpeciesIndex.frame: self._search_frame,
            SpeciesIndex.function: self._search_frame,
            SpeciesIndex.typedef: self._search_typedef,
        }
        self._exploredMemories = set()

    def _enqueue(self, obj, parentVertex=None, frame=None):
        mem = Memory(obj, frame=frame)
        if mem.is_optimized_out:
            return None
        if mem in self._exploredMemories:
            return None
        vertex = self._network.add_vertex()
        if parentVertex is not None:
            self._network.add_edge(parentVertex, vertex)
        self._network.vertex_properties.memories[vertex] = mem
        self._network.vertex_properties.label[vertex] = str(mem.name) + ":" + mem.value
        self._queue.enqueue(obj, mem, vertex, frame)
        return (parentVertex, vertex)

    def _prime_search(self):
        self._search_frame_chain_current()

    def search(self):
        self._prime_search()
        while self._queue.not_empty():
            tasks = self._queue.dequeue()
            for obj, mem, vertex, frame in tasks:
                if mem in self._exploredMemories:
                    continue
                self._search_adjacent(obj, mem, vertex, enclosingFrame=frame)
                self._exploredMemories.add(mem)

    def _search_adjacent(self, obj, mem, vertex, enclosingFrame=None):
        if mem.type_code in self._handler:
            self._handler[mem.type_code](obj, vertex, enclosingFrame=enclosingFrame)

    def _search_frame_chain_up(self, initialFrame):
        frame = initialFrame
        olderFrame = frame.older()
        while olderFrame:
            frame = olderFrame
            olderFrame = olderFrame.older()
        res = self._enqueue(frame)
        if res is not None:
            parent, child = res
            frame = frame.newer()
            if frame:
                self._search_frame_chain_down(frame, vertex=child)

    def _search_typedef(self, typedef, vertex, enclosingFrame=None):
        tname = typedef.type.name
        if tname in self._discovered_types:
            return
        self._discovered_types[tname] = typedef.type
        val = _extract_value(typedef, frame=enclosingFrame)
        # trueType = typedef.type.strip_typedefs()
        castVal = val.cast(typedef.type.target())
        self._enqueue(castVal, parentVertex=vertex, frame=enclosingFrame)

    def _search_frame_chain_down(self, initialFrame, vertex=None):
        res = self._enqueue(initialFrame, parentVertex=vertex)
        if res is None:
            return
        parent, child = res
        frame = initialFrame.newer()
        while frame:
            res = self._enqueue(frame, parentVertex=child)
            if res is None:
                return
            parent, child = res
            frame = frame.newer()

    def _search_frame_chain_current(self):
        self._search_frame_chain_up(gdb.newest_frame())

    def _search_array(self, array, vertex, enclosingFrame=None):
        start, end = array.type.range()
        arrayRange = range(int(start), int(end) + 1)
        for i in arrayRange:
            self._enqueue(array[i], parentVertex=vertex, frame=enclosingFrame)

    def _search_struct(self, struct, vertex, enclosingFrame=None):
        val = _extract_value(struct, frame=enclosingFrame)
        for field in val.type.fields():
            self._enqueue(val[field], parentVertex=vertex, frame=enclosingFrame)

    def _search_frame(self, frame, vertex, enclosingFrame=None):
        sal = frame.find_sal()
        try:
            block = gdb.block_for_pc(sal.pc)
        except RuntimeError as e:
            return
        for symbol in block:
            self._enqueue(symbol, parentVertex=vertex, frame=frame)

    def _search_pointer(self, pointer, vertex, enclosingFrame=None):
        val = _extract_value(pointer, frame=enclosingFrame)
        try:
            string = val.string()
            for i in range(len(string)):
                self._enqueue(val[i], parentVertex=vertex, frame=enclosingFrame)
            return
        except gdb.error:
            print("cant interpret ", val.referenced_value().type.name , "* as string")

        target = int(val)
        if NewTrackingBreak.tracker.is_allocated(target):
            bytesAllocated = NewTrackingBreak.tracker.allocated[target]
            targetSize = \
                val.dereference().type.strip_typedefs().sizeof
            for i in range(bytesAllocated // targetSize):
                self._enqueue(val[i], parentVertex=vertex, frame=None)
        else:
            if target != 0:
                # I am not totally sure how to handle the frame param here
                self._enqueue(val.dereference(), parentVertex=vertex, frame=None)
            else:
                pass

    def save(self, fileName="memorygraph.dot"):
        self._network.save(fileName)


gdb.execute("target remote | vgdb")
nb = NewTrackingBreak()
# nab = NewArrayBreak()
# gdb.execute("b main")
gdb.execute("b fib")
for i in range(2**5 - 1):
    gdb.execute("c")
graph = MemoryGraph()
# FunctionBreak._searcher = searcher
graph.search()
graph.save()
gdb.execute("clear")
gdb.execute("continue")
gdb.execute("c")
gdb.execute("q")
