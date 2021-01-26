from vpython import* #importing modules
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
G=6.67259 * 10 ** -20 #values for variables
m1=5.974 * 10 ** 24
m2=7.348 * 10 ** 22
re=6378.0
rm=1737.0
r12 = 384400.0
M=m1+m2
pi1=m1/M
pi2=m2/M
u1=G*m1
u2=G*m2
u=u1+u2
w=np.sqrt((u/r12**3))
x1=-pi2*r12
x2=pi1*r12
d=200.0
phi=-np.pi*0.5
v0=10.9148
gamma=20*np.pi/180.0
r0=re+d
x=r0*np.cos(phi)+x1
y=r0*np.sin(phi)
vx=v0*(np.sin(gamma)*np.cos(phi)- np.cos(gamma)*np.sin(phi))
vy=v0* (np.sin(gamma)*np.sin(phi)+np.cos(gamma)*np.cos(phi))
t=0
tf=6.1*24*3600
def f(r,tpoints): #define a function
    fvx=2*w*r[3]+w**2*r[0]-(u1/(np.sqrt((r[0]+pi2*r12)**2+r[1]**2))**3)*(r[0]-x1)-(u2/(np.sqrt((r[0]-pi1*r12)**2+r[1]**2))**3)*(r[0]-x2)
    fvy=-2*w*r[2]+(w**2-(u1/(np.sqrt((r[0]+pi2*r12)**2+r[1]**2))**3)-(u2/(np.sqrt((r[0]-pi1*r12)**2+r[1]**2))**3))*r[1]
    return [r[2],r[3],fvx,fvy]
r=[x,y,vx,vy] #solving ode13

tpoints=np.linspace(t,tf,tf)
sol = odeint(f,r,tpoints)
'''
plt.plot(sol[:,0],sol[:,1])
plt.show()
'''
#make animation
scene=canvas(background=color.black,center=vector(24,3,0),width=700,height=350)
earth=sphere(radius=1,color=color.blue,pos=vector(0,0,0))
moon=sphere(radius=0.4,color=color.white,pos=vector(37.44,0,0))
sat=sphere(radius=0.1,color=color.orange,pos=vector(0,0,0),make_trail=True,trail_type='points',trail_color=color.white)
label(pos=vector(24,14,0), text='Restricted planar three body problem',box=False,color=color.red)
label(pos=vector(0,-2,0), text='earth',box=False)
label(pos=vector(37.44,-2,0), text='moon',box=False)
label(pos=vector(3,9,0), text='spacecraft trajectory',box=False)
time1=label(pos=vector(46,10,0),text="time")
position_x=label(pos=vector(46,8,0),text="X")
position_y=label(pos=vector(46,6,0),text="Y")
velocity=label(pos=vector(46,4,0),text="Velocity")
pointer = arrow(pos=vector(0,7,1),axis=vector(2,-2,-2), shaftwidth=0.3)
time=0
#making widgets
running = True

def Run(b):
    global running
    running = not running
    if running:
          b.text = "Run"
    else: 
          b.text = "Pause"
button(text="Run", pos=vector(5,0,0), bind=Run)
while time<tf:
    rate(10000)
    if not running:
        p=vector((sol[time,0]/10000),(sol[time,1]/10000),0)
        p_x=sol[time,0]
        p_y=sol[time,1]
        v=(sol[time,2]**2+sol[time,3]**2)**(1/2)
        sat.pos=p
        time+=1
        time1.text=("Time:%.1f"%(time/60)+" min")
        position_x.text=("X:%.1f"%p_x)
        position_y.text=("Y:%.1f"%p_y)
        velocity.text=("velocity:%.1f"%v+"km/s")
