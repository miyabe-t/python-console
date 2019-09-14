# skltnsh (SkeltonShell)

## Introduction

`SkeltonShell` is the library for someone who wants to create command line
interface (CLI) using python. This library provides you easy-to-use bash-like
command line interface.


Comprehensive Guideline:

- make the core module
- pass a instance of the class to `SkeltonShell`.

The core module is the module containing
- definitions of commands
- definitions of functions to control core logics

## How to create the core module

It's just a module, a class.
You can create the core module as you like. But you need to follow some rules
since `SkeltonShell` analyzes your core module in order to generate commands.

After creation, you need to create an instance of the core module and
create an instance of `SkeltonShell` with instances of the core module.
Then, call `main()` of `SkeltonShell`. This will start CLI session.

Example:

```python
mc = MyCommands()
ex = SkeltonShell(modules=mc)
ex.main()
```

The entire sample of the core module is depicted in the end of this document.
It would be great to take a glance at that to get a big-picture.

### Create commands

In order to create commands, you need to create functions with specific prefix, `cbk_` .
For example, if you create a function like this:

```python
def cbk_test(self, args):
  print('Do special things')
```

This function will be interpreted as a command `test` .
If users type `test` in our shell, then `cbk_test` will be called.

Note that callback functions should take two arguments.
The first one is `self`, and second one is a list of arguments for the command.

Sometimes we need targets and options for commands. This feature is useful
in such a case.

For example, if users type this:

```
>>> add light_task John
```

then the second argument of `cbk_add` function will be `['light_task', 'John']` .

### Create aliases

In order to declare aliases for your commands, you need to define arrays
containing aliases for the command.

Let's see the example:

```python
self.test_aliases = [ 't', 'te' ]
```

By defining `test_aliases` above, you can define aliases, `t` and `te`,
for the command called `test` . So users can use `test` command by just typing
`t` or `te` .

## Code Example

``` python
from skltnsh import SkeltonShell

class MyCommands:
    """Manage a list through command line"""
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
    ex = SkeltonShell(modules=MyCommands())
    ex.main()
```

Then you can use commands : `add`, `del`, `show` (also as `sh`, `s`).
