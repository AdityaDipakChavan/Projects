import win32com.client
import math


from time import sleep
from ctypes import *
from ctypes.wintypes import *

handle = win32com.client.Dispatch("openglrobot.RobotWindowApi")
handle.init()
handle.createRobotWindow()

# filename='C:/daten/cpp/Qt/QtOpenGLRobot2/QtOpenGLRobot/data/robots/KR16_23Opsira2BBBLeuchte1.xml'
filename = 'C:/daten/cpp/opsira/robot/robot_src/robotBase/env/config/KR4_R600_Stud1.xml'
modelPath = 'C:/daten/cpp/opsira/robot/robot_cad'
gr = math.pi / 180.0
handle.initMainDialog()
handle.openMainDialog()
handle.print("Hallo von Python")

handle.setCADModelDefaultPath(modelPath)
handle.readProjectDataXML(filename)
handle.print('fertig lesen')
handle.openCadWindow()
handle.setCadWindowPosition(100, 100)
handle.setCadWindowSize(800, 600)
handle.addCadBox('box1', 100, 200, 20)
handle.setCadTranslation('box1', 300, 0, 300)
handle.setCadRotationKuka('box1', 0.0, 90 * gr, 20 * gr)

handle.addCadCylinder('cylinder', 20.0, 400.4, 20)
handle.setCadTranslation('cylinder', 600, 0, 300)

handle.setTool('gripper', 34.51, 0, 108.28, 0 * gr, 28.67 * gr, 0 * gr)
handle.setBase('base', 200, 0, 200, 0 * gr, 0 * gr, 0 * gr)

# bool moveRobotLinear(double x, double y, double z, double A, double B, double C);
#    bool setTraceDiffuseColor(double r, double g, double b, double alpha);
#    bool setCadWindowViewpoint(double x, double y, double z, double A, double B, double C);
#    bool moveCameraFlangeViewpoint(double x, double y, double z, double A, double B, double C);
#    bool setCadWindowViewpointByName(QString name);
#    bool setCadWindowViewpointCenter(double x, double y, double z);


handle.moveAxis(-30 * gr, -50 * gr, 40 * gr, 0 * gr, 45 * gr, 0 * gr)
handle.setTraceTcp(True)
handle.moveRobotLinear(335.69, -115.6, 192.29, -150 * gr, 26.33 * gr, 180 * gr)
handle.moveRobotPtp(239.72, -215.6, 192.29, gr * -150, gr * 26.33, gr * 180)
handle.setTraceTcp(False)

# Simulate gripping
handle.addChildrenTree('gr1', 'cylinder')
handle.setCadTranslation('cylinder', 0, 0, 0)
handle.moveAxis(-30 * gr, -50 * gr, 40 * gr, 0 * gr, 45 * gr, 0 * gr)

# Simulate release to add object to robot base
handle.addChildrenTree('KR7', 'gr1')
handle.setCadTranslation('cylinder', 220, 440, 200)
handle.moveAxis(30 * gr, -50 * gr, 40 * gr, 0 * gr, 45 * gr, 0 * gr)

handle.forceUpdateCad()

handle.addChildrenTree('gr1', 'cylinder')
handle.moveAxis(-30 * gr, -50 * gr, 40 * gr, 0 * gr, 45 * gr, 0 * gr)

import time

print("something")
time.sleep(5.5)  # pause 5.5 seconds
print("something")
handle.print('ende warten')

input("Press Enter end...")

handle.closeCentralDialog()
handle.destroyRobotWindow()

del handle
