#!/usr/bin/env python
# -*- encoding UTF-8 -*-
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

import gdb





class _Type(object):

    # Global

    """
    # Type detection error code
    """
    error = gdb.TYPE_CODE_ERROR

    """
    # internal debugger function type code.
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


class _Representation(object):

    value = gdb.Value

    frame = gdb.Frame

    symbol = gdb.Symbol

    block = gdb.Block

    type = gdb.Type


_type_description = {
    _Type.error: "pointer",
    _Type.array: "array",
    _Type.struct: "struct",
    _Type.union: "union",
    _Type.enum: "enumeration",
    _Type.function: "function",
    _Type.integer: "integer",
    _Type.float: "float",
    _Type.void: "void",
    _Type.string: "string",
    _Type.error: "type detection error",
    _Type.method: "method",
    _Type.method_pointer: "method pointer",
    _Type.member_pointer: "member pointer",
    _Type.reference: "reference",
    _Type.character: "character",
    _Type.boolean: "boolean",
    _Type.complex: "complex",
    _Type.typedef: "typedef",
    _Type.namespace: "namespace",
    _Type.internal_function: "GDB internal function",
}

_representation_description = {
    _Representation.value: "value",
    _Representation.frame: "frame",
    _Representation.symbol: "symbol",
    _Representation.block: "block",
    _Representation.type: "type",
}


_gdb_types = {
    _Representation.value: _species_code_from_value,
    gdb.Frame: _species_code_from_frame,
    gdb.Symbol: _species_code_from_symbol
}
