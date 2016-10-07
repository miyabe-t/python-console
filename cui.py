#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shlex
from modules.ShellModules import ShellModules
from modules._getch import _Getch

VERSION='0.1'
global_help = '''
Help string here.
'''

class ShellInputter:
    def __init__(self):
        self.size = [0, 0]
        self.history = ['']
        self.prompt = '>>> '
        self.getch = _Getch()

    def setConsoleSize(self, rows, columns):
        self.size[0] = rows
        self.size[1] = columns

    def setPrompt(self, prmpt):
        self.prompt = prmpt

    def input(self):
        import sys
        cmd = ''
        cur = len(self.history)
        print(self.prompt),
        while True:
            ch = self.getch()
            if ch == chr(0x03):
                cmd = ''
                break
            elif ch == chr(0x08) or ch == chr(127):
                cmd = cmd[:-1]
            elif ch == chr(0x10) or ch == '\x1b[A': # Ctrl+p / Arrow UP
                cur = cur-1 if cur > 0 else cur
                cmd = self.history[cur]
            elif ch == chr(0x0e) or ch == '\x1b[B': # Ctrl+n / Arrow down
                cur = cur+1 if cur < len(self.history)-1 else len(self.history)-1
                cmd = self.history[cur]
            elif ch == chr(0x0d):
                break
            else:
                cmd += ch
            print('\r' + ' '*(self.size[1] - 1) ),
            print('\r' + self.prompt + cmd),
        print('')
        self.history.append(cmd.strip())
        cmd = shlex.split(cmd)
        return cmd

class ShellEvaluator:
    def __init__(self, modules):
        self.cmds = []
        self.prefix = 'cbk_'
        self.suffix = '_aliases'
        self.core = modules

        # search functions start with `self.prefix` and convert them
        # into a dictionary which contains a commands list a and callback method
        # via `self.regist()`. Aliases are also defined using nameing rule.
        func_names = [ func for func in dir(self.core) if 'cbk_' in func ]
        for func_name in func_names:
            func = getattr(self.core, func_name)
            cmd = [ func_name, func_name.replace( self.prefix, '' ) ]
            if hasattr(self.core, cmd[1] + self.suffix):
                for item in getattr(self.core, cmd[1]+self.suffix):
                    cmd.append(item)
            self.regist( cmd , func)

    def regist(self, commands, callback):
        '''
        Parameters
        -----------
        commands : list of string
            a command you want to use with aliases of that command included in one list
        callback : function
            this fucntion will be called for `commands`
        '''
        self.cmds.append( { 'name':commands, 'callback':callback } )

    def help(self):
        global global_help
        print(global_help)

    def evaluate(self, args):
        if len(args) == 0 : return
        for cmd in self.cmds:
            if args[0] in cmd['name'] :
                return cmd['callback'](args[1:])
        else :
            print('No such a command : {0}'.format(args[0]))

class ShellOutputter:
    def __init__(self):
        self.size = [0, 0]

    def setConsoleSize(self, rows, columns):
        self.size[0] = rows
        self.size[1] = columns

    def output(self):
        pass

class ShellSkelton:
    def __init__(self, modules=ShellModules() ):
        self.inputter = ShellInputter()
        self.evaluator = ShellEvaluator(modules)
        self.outputter = ShellOutputter()
        self.checkSize()
        global VERSION
        print("This is SkeltonShell ver.{0}".format(VERSION))

    def checkSize(self):
        self.rows, self.columns = os.popen('stty size', 'r').read().split()
        self.rows, self.columns = int(self.rows), int(self.columns)
        self.inputter.setConsoleSize( self.rows, self.columns )
        self.outputter.setConsoleSize( self.rows, self.columns )

    # この関数はoverrideして自由に書き換えるようにする。
    def main(self):
        while True:
            cmd = self.inputter.input()
            ret = self.evaluator.evaluate(cmd)
            if ret == -1: break
            self.outputter.output()
            
if __name__ == '__main__':
    shell = ShellSkelton()
    shell.main()
