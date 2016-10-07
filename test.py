class cmds:
    def __init__(self):
        self.list = []

    def regist(self, cmd, cbk):
        self.list.append( { 'cmd': cmd, 'cbk':cbk} )

    def do(self, cmd):
        tar = 0
        for cms in self.list:
            for item in cms['cmd']:
                if item == cmd : tar = cms
        if tar == 0: return
        cms['cbk']()

class core:
    def __init__(self):
        pass

    def test(self):
        print('find')

    def commet(self):
        print('commet')


co = core()
cm = cmds()
cm.regist( ['test', 't'], co.test )
cm.do('t')
