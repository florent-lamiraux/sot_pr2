# 1. Init robot, ros binding, solver
from dynamic_graph.sot.pr2.pr2_tasks import *
[robot,ros,sot] = initPr2RosSimuProblem()

# 2. Main loop
from dynamic_graph.sot.core.utils.thread_interruptible_loop import loopInThread,loopShortcuts
dt=3e-3
@loopInThread
def inc():
    robot.device.increment(dt)

runner=inc()
[go,stop,next,n]=loopShortcuts(runner)

# 3. Init Tasks
taskRH = Pr2RightHandTask(robot)
taskLH = Pr2LeftHandTask(robot)
taskJL = Pr2JointLimitsTask(robot,dt)
taskContact = Pr2ContactTask(robot)
taskFov = Pr2FoVTask(robot,dt)
taskBase = Pr2BaseTask(robot)

# 4. Formulate problem
from dynamic_graph.sot.core.meta_tasks_kine import gotoNd

# 4.1 Right hand
targetRH = (0.60,0.2,0.8)
gotoNd(taskRH,targetRH,'111',(4.9,0.9,0.01,0.9))

# 4.2 Left hand
targetLH = (0.65,0.6,0.3)
gotoNd(taskLH,targetLH,'111',(4.9,0.9,0.01,0.9))

# 4.3 Look at the right hand target
taskFov.goto3D(targetRH)

# 4.4 Base position
targetBase = (0,0,0,0,0,-0.2)
gotoNd(taskBase,targetBase,'100011',(4.9,0.9,0.01,0.9))


sot=push(sot,taskFov)
sot=push(sot,taskBase)
sot=push(sot,taskRH)
sot=push(sot,taskLH)
sot.addContact(taskContact)
sot=push(sot,taskJL)

print ('Type go to run the solver loop')