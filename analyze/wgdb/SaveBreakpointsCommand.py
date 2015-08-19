#!/usr/bin/env python
# -*- encoding UTF-8 -*-

import gdb

class SaveBreakpointsCommand (gdb.Command):
    """"Save the current breakpoints to a file.

    This command takes a single argument, a file name.

    The breakpoints can be restored using the 'source'
    command."""

    def __init__(self):
        super (SaveBreakpointsCommand, self).__init__("save breakpoints",
                                                      gdb.COMMAND_SUPPORT,
                                                      gdb.COMPLETE_FILENAME)

    def invoke(self, arg, from_tty):
        with open(arg, 'w') as f:
            for bp in gdb.breakpoints():
                instruction = "break " + bp.location
                if bp.thread is not None:
                    instruction += " thread " + bp.thread
                if bp.condition is not None:
                    instruction += " if " + bp.condition
                f.write(instruction)
                if not bp.is_valid() or not bp.enabled:
                    f.write("disable " + bp.number)
                commands = bp.commands
                if commands is not None:
                    f.write("commands")
                    for c in commands:
                        f.write(c)
                    f.write("end")
                f.write("\n")


SaveBreakpointsCommand()
