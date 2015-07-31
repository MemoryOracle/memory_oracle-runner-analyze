#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import re
import memory.interface
import gdb
import graph_tool.all as gt


class Extractor(memory.interface.extractor):

    MAX_SEARCHERS = 4
    _arrowMatch = re.compile(r"([>,:<])")

    # This logic may need to move to a different file.
    # def run(self):
    #
    #     missCount = 0
    #     while True:
    #         try:
    #             x = Oracle.found.popleft()
    #             missCount = 0
    #             self._describe(x)
    #             self._extract_object(x)
    #         except IndexError as e:
    #             if missCount >= 3:
    #                 return
    #             else:
    #                 gdb.write("Queue miss!\n")
    #                 missCount += 1
    #                 time.sleep(0.1)

    def extract_object(self, x):
        # This should be done with a lookup
        code = x["value"].type.strip_typedefs().code
        if code == gdb.TYPE_CODE_ARRAY:
            self.extract_array(x)
        elif code == gdb.TYPE_CODE_STRUCT:
            self.extract_struct(x)
        elif code == gdb.TYPE_CODE_PTR:
            self.extract_pointer(x)

    ## Commented until I am sure I actually want this method.
    # def describe_object(self, x):
    #     try:
    #         if (x["index"][1] != 'None'):
    #             Oracle.network.add_node(x["index"])
    #             Oracle.described.append(x)
    #     except gdb.MemoryError:
    #         gdb.write("debug: encountered invalid memory\n")

    def extract_range(self, x, startRange, endRange):
        for element in range(int(startRange), int(endRange + 1)):
            foundObj = dict()
            foundObj.update(x)
            foundObj["value"] = x["value"][element]
            foundObj["name"] = x["name"] + "[" + str(element) + "]"
            foundObj["parent"] = x["index"]
            foundObj.update(Oracle._extract(foundObj["value"]))
            if element == int(startRange):
                Oracle.network.add_edge(foundObj["parent"], foundObj["index"], label="[]")
            if int(foundObj["address"], 16):
                Oracle.found.append(foundObj)

    def _extract_array(self, x):
        startRange, endRange = x["value"].type.strip_typedefs().range()
        self._extract_range(x, startRange, endRange)

    def _extract_struct(self, x):
        if x["index"][1] in {'None', None, 0x0, "0x0"}:
            return
        itr = x["value"].type.fields()
        fields = [x["index"]]
        for element in itr:
            foundObj = dict()
            foundObj.update(x)
            foundObj["value"] = x["value"][element]
            foundObj["parent"] = x["index"]
            try:
                foundObj.update(Oracle._extract(foundObj["value"]))
            except AlreadyFound:
                return
            if foundObj["address"] not in {'None', 0x0, "0x0", 0}:
                Oracle.found.append(foundObj)

    def _extract_pointer(self, x):
        foundObj = dict()
        foundObj.update(x)
        ## TODO: Make this handle char* correctly
        try:
            foundObj["value"] = x["value"].dereference()
            addr = int(foundObj["value"].address)
            foundObj["parent"] = x["index"]
            if addr not in Oracle.extractd:
                if addr in NewBreak.allocated:
                    typeSize = foundObj["value"].type.sizeof
                    size = NewBreak.allocated[addr]
                    gdb.write("Found " + str(size / typeSize) + "\n")
                    # realType = foundObj["value"].type.array(0, size / typeSize - 1)
                    self._extract_range(x, 0, size / typeSize - 1)
                    Oracle.extractd.add(addr)
                else:
                    foundObj["name"] = "*" + x["name"]
                    foundObj.update(Oracle._extract(foundObj["value"]))
                    if foundObj["address"] != "None":
                        Oracle.network.add_edge(foundObj["parent"], foundObj["index"], label="*")
                        Oracle.found.append(foundObj)
                        Oracle.extractd.add(addr)
            else:
                foundObj.update(Oracle._extract(foundObj["value"]))
                Oracle.network.add_edge(foundObj["parent"], foundObj["index"], label="*")
        except gdb.MemoryError as e:
            gdb.write(str(e))
            return
        except gdb.error as e:
            gdb.write(str(e))
            return
        except AlreadyFound:
            gdb.write("Already found that one!\n")
            return
