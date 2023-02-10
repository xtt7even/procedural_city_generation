from direct.showbase.ShowBase import ShowBase

import Connector

class Generator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #Connector.generateCity()
        Connector.finalize()

        base.disableMouse()
        base.camera.setPos(0,0,500)
        base.camera.lookAt(0,0,0)

        base.taskMgr.add(self.testTask,'testTask')

    def testTask(self,task):
        return task.cont

generator = Generator()
generator.run()
