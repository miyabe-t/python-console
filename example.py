#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example use of SkeltonShell
===========================

This file describes how to use SkeltonShell.
The Class named `ModuleExample` is just example
of a module which is passed to SkelltonShell.

A module must have commands, aliases of commands and
function invoked by commands. You must follow the naming
convention described in README.
"""
from skltnsh import SkeltonShell


class ModuleExample:
    def __init__(self):
        self.test_aliases = ['t']
        self.quit_aliases = ['q', 'exit']

    def cbk_test(self, args):
        print('This is the funtion named "cbk_test"')
        print('Here goes your arguments list : '),
        print(args)

    def cbk_quit(self, args):
        return -1


"""
Entry point of this sample script. Note that SkeltonShell's argument
must be instance of the calss, not class itself. Then just call main()
to begin main loop of the program, interactive shell.
"""
if __name__ == '__main__':
    ex = SkeltonShell(modules=ModuleExample())
    ex.main()
