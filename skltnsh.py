#!/usr/bin/env python
# -*- coding: utf-8 -*-

# enable python3's print function in Python2.x
from __future__ import print_function
import os
import shlex
from modules._getch import _Getch


VERSION = '0.1'


class ShellInputter:
    def __init__(self):
        self.cmd = ''
        self.size = [0, 0]
        self.history = ['']
        self.hist_cur = len(self.history)
        self.cursor = 0
        self.cursor_dif = 0
        self.insert = False
        self.binds = []
        self.prompt = '>>> '
        self.getch = _Getch()

        # register special keys
        self.register(chr(0x01), self.moveToHead)      # C-a
        self.register(chr(0x03), self.clear)           # C-c
        self.register(chr(0x05), self.moveToTail)      # C-e
        self.register(chr(0x15), self.deleteAll)       # C-u
        self.register(chr(0x17), self.deleteWord)      # C-w
        self.register(chr(0x08), self.deleteChar)      # C-h
        self.register(chr(0x7f), self.deleteChar)      # backspace
        self.register('\x1b[3', self.deleteFolChar)    # delete key
        self.register(chr(0x10), self.historyUp)       # C-p
        self.register('\x1b[A', self.historyUp)        # up arrow
        self.register(chr(0x0e), self.historyDown)     # C-n
        self.register('\x1b[B', self.historyDown)      # down arrow
        self.register('\x1b[C', self.moveForward)      # right arrow
        self.register('\x1b[D', self.moveBackward)     # left arrow
        self.register(chr(0x0a), self.newline)         # C-j
        self.register(chr(0x0d), self.newline)         # Enter

    def setConsoleSize(self, rows, columns):
        self.size[0] = rows
        self.size[1] = columns

    def setPrompt(self, prmpt):
        self.prompt = prmpt

    def input(self):
        self.cmd = ''
        term = False
        print(self.prompt, end='', flush=True)
        while True:
            ch = self.getch()
            # if key-bind matching occured or not
            matched = False
            # default cursor movement is +1
            self.cursor_dif = 1

            for bind in self.binds:
                if ch == bind['key']:
                    term = bind['callback']()
                    matched = True
            if term:
                break

            self.updateCursor()

            if not matched:
                head = self.cursor - 1 if (self.cursor > 0) else 0
                self.cmd = self.cmd[:head] + ch + self.cmd[head:]

            self.updateCurLine()
        print('')
        self.history.append(self.cmd.strip())
        self.hist_cur = len(self.history)
        self.cursor = 0
        splitted_cmd = shlex.split(self.cmd)
        return splitted_cmd

    def updateCursor(self):
        self.cursor += self.cursor_dif
        if self.cursor < 0:
            self.cursor = 0
        if self.cursor > len(self.cmd) + 1:
            self.cursor = len(self.cmd) + 1

    def updateCurLine(self):
        print('\r' + ' '*(self.size[1] - 1), end='')
        print('\r' + self.prompt + self.cmd, end='', flush=True)
        print('\r' + self.prompt + self.cmd[:self.cursor], end='', flush=True)
        return

    def clear(self):
        self.cmd = ''
        return True

    def deleteAll(self):
        self.cmd = ''
        return False

    def deleteChar(self):
        self.cursor_dif = -1
        self.cmd = self.cmd[:self.cursor-1] + self.cmd[self.cursor:]
        return False

    def deleteFolChar(self):
        self.cursor_dif = -1
        self.cmd = self.cmd[:self.cursor] + self.cmd[self.cursor+1:]
        return False

    def deleteWord(self):
        cutoff_point = self.cmd.rstrip().rfind(' ', 0, self.cursor)

        if cutoff_point == -1:
            # Could not find a space.
            # This means a user is now on a first word
            # In this case we have nothing to do since we will do +1 after
            pass

        # some +1 used in order to deal with a target white space
        self.cmd = self.cmd[:cutoff_point+1] + self.cmd[self.cursor:]
        self.cursor_dif = cutoff_point - self.cursor + 1
        return False

    def newline(self):
        return True

    def historyUp(self):
        if self.hist_cur > 0:
            self.hist_cur = self.hist_cur-1
        self.cmd = self.history[self.hist_cur]
        self.cursor_dif = 0
        return False

    def historyDown(self):
        if self.hist_cur < len(self.history)-1:
            self.hist_cur = self.hist_cur+1
        else:
            len(self.history)-1
        self.cmd = self.history[self.hist_cur]
        self.cursor_dif = 0
        return False

    def moveForward(self):
        self.cursor_dif = 1
        return False

    def moveBackward(self):
        self.cursor_dif = -1
        return False

    def moveToHead(self):
        self.cursor_dif = (-1) * self.cursor
        return False

    def moveToTail(self):
        self.cursor_dif = len(self.cmd) - self.cursor + 1
        return False

    def register(self, key, callback):
        self.binds.append({'key': key, 'callback': callback})


class ShellEvaluator:
    def __init__(self, modules):
        self.cmds = []
        self.prefix = 'cbk_'
        self.suffix = '_aliases'
        self.core = modules

        # search functions start with `self.prefix` and convert them into a
        # dictionary which contains a commands list a and callback method via
        # `self.register()`. Aliases are also defined using nameing rule.
        func_names = [func for func in dir(self.core) if 'cbk_' in func]
        for func_name in func_names:
            func = getattr(self.core, func_name)
            cmd = [func_name, func_name.replace(self.prefix, '')]
            if hasattr(self.core, cmd[1] + self.suffix):
                for item in getattr(self.core, cmd[1]+self.suffix):
                    cmd.append(item)
            self.register(cmd, func)

    def register(self, commands, callback):
        '''
        Args:
        commands (list(str)):
            a command you want to use with aliases of that command included in
            one list
        callback (function):
            this fucntion will be called for `commands`
        '''
        self.cmds.append({'name': commands, 'callback': callback})

    def help(self):
        global global_help
        print(global_help)

    def evaluate(self, args):
        if len(args) == 0:
            return
        for cmd in self.cmds:
            if args[0] in cmd['name']:
                return cmd['callback'](args[1:])
        else:
            print('No such a command : {0}'.format(args[0]))



class ShellOutputter:
    def __init__(self):
        self.size = [0, 0]

    def setConsoleSize(self, rows, columns):
        self.size[0] = rows
        self.size[1] = columns

    def output(self):
        pass


class SkeltonShell:
    def __init__(self, modules):
        self.inputter = ShellInputter()
        self.evaluator = ShellEvaluator(modules)
        self.outputter = ShellOutputter()
        self.checkSize()
        global VERSION
        print("This is SkeltonShell ver.{0}".format(VERSION))

    def checkSize(self):
        self.rows, self.columns = os.popen('stty size', 'r').read().split()
        self.rows, self.columns = int(self.rows), int(self.columns)
        self.inputter.setConsoleSize(self.rows, self.columns)
        self.outputter.setConsoleSize(self.rows, self.columns)

    def main(self):
        '''This function is the main loop of interactive shell.
        You can override this function to change global behavior
        of the interactive shell, such as change the mode of shell or so on.
        '''
        while True:
            cmd = self.inputter.input()
            ret = self.evaluator.evaluate(cmd)
            if ret == -1:
                break
            self.outputter.output()


if __name__ == '__main__':
    print('Running this file directly has no meaning...')
