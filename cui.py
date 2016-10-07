#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shlex
from modules.ShellModules import ShellModules
from modules._getch import _Getch

VERSION='0.1'

class ShellInputter:
    def __init__(self):
        self.size = [0, 0]
        self.history = ['']
        self.hist_cur = len(self.history)
        self.binds = []
        self.prompt = '>>> '
        self.getch = _Getch()
        # regist key bindings to itself
        self.regist(chr(0x03), self.clear)
        self.regist(chr(0x08), self.backspace)
        self.regist(chr(0x7f), self.backspace)
        self.regist(chr(0x10), self.historyUp)
        self.regist('\x1b[A', self.historyUp)
        self.regist(chr(0x0e), self.historyDown)
        self.regist('\x1b[B', self.historyDown)
        self.regist(chr(0x0d), self.newline)

    def setConsoleSize(self, rows, columns):
        self.size[0] = rows
        self.size[1] = columns

    def setPrompt(self, prmpt):
        self.prompt = prmpt

    def input(self):
        import sys
        cmd = ''
        term = False
        cur = len(self.history)
        print(self.prompt),
        while True:
            ch = self.getch()
            matched = False
            for bind in self.binds:
                if ch == bind['key'] :
                    cmd, term = bind['callback'](cmd)
                    matched = True
            if not matched:
                cmd += ch
            if term : break
            print('\r' + ' '*(self.size[1] - 1) ),
            print('\r' + self.prompt + cmd),
        print('')
        self.history.append(cmd.strip())
        self.hist_cur = len(self.history)
        cmd = shlex.split(cmd)
        return cmd

    def clear(self, cmd):
        return '', True
    def backspace(self, cmd):
        return cmd[:-1], False
    def newline(self, cmd):
        return cmd, True
    def historyUp(self, cmd):
        self.hist_cur = self.hist_cur-1 if self.hist_cur > 0 else self.hist_cur
        return self.history[self.hist_cur], False
    def historyDown(self, cmd):
        self.hist_cur = self.hist_cur+1 if self.hist_cur < len(self.history)-1 else len(self.history)-1
        return self.history[self.hist_cur], False
    def regist(self, key, callback):
        self.binds.append({ 'key':key, 'callback':callback } )

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

    def main(self):
        '''This function is the main loop of interactive shell.
        You can override this function to change global behavior
        of the interactive shell, such as change the mode of shell or so on.
        '''
        while True:
            cmd = self.inputter.input()
            ret = self.evaluator.evaluate(cmd)
            if ret == -1: break
            self.outputter.output()
            
if __name__ == '__main__':
    shell = ShellSkelton()
    shell.main()
