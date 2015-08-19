
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

# I likely need to move this to a different interface.
# It is not really the extractor's job to articulate data to the oracle.
# def describe_object(self, x):
#     """
#     Describe object x in the inferior.
#     """
#     raise NotImplementedError("describe_object method not implemented")

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

## Commented until I am sure I actually want this method.
# def describe_object(self, x):
#     try:
#         if (x["index"][1] != 'None'):
#             Oracle.network.add_node(x["index"])
#             Oracle.described.append(x)
#     except gdb.MemoryError:
#         gdb.write("debug: encountered invalid memory\n")

