class ShellModules:
    def __init__(self):
        self.test_aliases = ['t']
        self.quit_aliases = ['q', 'exit']

    def cbk_test(self, args):
        print('This is the funtion named "cbk_test"')
        print('Here goes your arguments list : '),
        print(args)

    def cbk_quit(self, args):
        return -1
