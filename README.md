# SkeltonShell

## Introduction

`SkeltonShell` is the library for someone who want to create command line interface
with python. Command line interface is very useful for interactive program which 
means that the program which isn't just a sequential script.

All you have to do with this library is to make a module class, which contains
commands and related functions, and pass the instance of the class to `SkeltonShell`.
But the important point of creating a module class is "naming rule".

## Naming rule of SkeltonShell modules

`SkeltonShell` analyze a module class and automatically make commands and callback
functions, so you must  the naming rule of `SkeltonShell` to make a correct program.

### Commands and functions

All the commands are derived from the name of functions of module class. Functions 
start with `cbk_` is recognized as command related functions, then the program
extract string after `cbk_` and regist it as a command. And a command is tied to 
that function. 

For example, if your module class have function named `cbk_test`, the program will
regist the command `test`. If a user types the command `test`, the program will
invoke the function `cbk_test`.

### Aliases of commands

You can add aliases to each command. This is also contrained by naming rule. If you
wish to add aliases, just append list variable named `*_aliases` to module class. `*` 
stands for each command.

For example, `self.test_aliases = ['t']` for an aliase for the `test` command.

## Code Example

	import SkeltonShell

	class MyCommands:
		def __init__(self):
			self.items = []
			self.show_aliases = [ 'sh', 's' ]

		def cbk_add(self, args):
			self.items.append(args[0])

		def cbk_del(self, args):
			self.items.remove(args[0])

		def cbk_show(self, args):
			print(self.items)

	if __name__ == '__main__':
		cmds = MyCommands()
		shell = SkeltonShell(cmds)
		shell.main()

Then you can use commands : add, del, show (also sh, s).
