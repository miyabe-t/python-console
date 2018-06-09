# SkeltonShell

## Introduction

`SkeltonShell` is the library for someone who want to create command line interface
with python.

All you have to do with this library is to make a module class containing
commands and related functions, then pass a instance of that module class to `SkeltonShell`.
A module class must protect the **naming rule** .

## The naming rule of SkeltonShell modules

`SkeltonShell` analyze a name of functions or variables which a module class has,
and automatically generate commands and callback functions.
So you must protect the naming rule of `SkeltonShell` to make a module.

### Naming Rule 1: Commands and functions

```python
def cbk_<commandName>(self):
	# do something
```

Callback functions must have `cbk_` as prefix.
Words after `cbk_` prefix is treated as a command.

All the commands are derived from the name of functions of a module class. Functions
start with `cbk_` is recognized as a command related function (callback function),
then the program extract string after `cbk_` and regist it as a command.
So when you declaer a callback function, you also declear a command name.

For example, if your module class have function named `cbk_test`, the program will
regist the command `test`. If a user types the command `test`, the program will
invoke the function `cbk_test`.

### Naming Rule 2: Aliases of commands

```python
self.<commandName>_aliases = [ <alias0>, <aliase1>, ... ]
```

An array of command named `*_aliases` defines aliases of a given command.

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

Then you can use commands : `add`, `del`, `show` (also as `sh`, `s`).
