import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def x1_inside(v_x,t):
  return v_x*t

def y1_inside(v_0x,radi,e,bfi,t1):
  y= 0.5*radi*e*(t1**2)
  if radi*(x1_inside(v_0x,t1)*bfi)**2>= V:
    return D/2
  else:
    return y

# outside Electric_field
def y2_outside(radi,t2,x1,bfield,t1_fi,e):
  if radi*(x1*bfield)**2>=V:
    return 0
  else:
    vy_final_inside= radi*e*t1_fi
    return vy_final_inside*t2
  
def x2_outside(v_x,t2):
  return v_x*t2


def path_function(voltage,distance,x_1,x_2,b):
    ELECTRON_CHARGE= 1.6e-19
    ELECTRON_MASS = 9.1e-31
    # Calculate other factors
    ratio =ELECTRON_CHARGE/ELECTRON_MASS
    E_field=voltage/distance
    acceleration1=ratio*E_field
    vx= E_field/b
    t1_final=x_1/vx
    t2_final=x_2/vx
    #calculate y1, y2
    y1=y1_inside(vx,ratio,E_field,b,t1_final)
    y2=y2_outside(ratio,t2_final,x_1,b,t1_final,E_field)

    x_array=[]
    y_array=[]
    time_step1=t1_final/1000
    time_step2=t2_final/1000
    for i in range (0,2000):
      if (i<1000):
        time=i*time_step1
        if (ratio*(x1_inside(vx,time)*b)**2>=V):
          break
        else:
          x_array.append(x1_inside(vx,time))
          y_array.append(y1_inside(vx,ratio,E_field,b,time))
      else:
        time=(i-1000)*time_step2
        if(y2==0):
          break
        else:
          x_array.append(x1+x2_outside(time))
          y_array.append(y1+y2_outside(time))
    df = pd.DataFrame({'x': x_array, 'y': y_array})

    #path
    plt.plot(x_array,y_array,"r")

    #note
    plt.text(-0.1,(distance/2)*1.3,'E={} V/m,$x_1$={}m,\n$x_2$={}m,$v_0={}m/s$'.format(E_field,x1,x2,vx),fontsize = 12,
             bbox = dict(facecolor = 'lightblue', alpha = 0.5))
    plt.title("Simulation")
    plt.axis("off")

    #facilities
    plt.hlines(y=D/2, xmin=0, xmax=x1, linewidth=4, color='black')
    plt.hlines(y=-D/2, xmin=0, xmax=x1, linewidth=4, color='black')

    plt.vlines(x=x1+x2, ymin=-D/2, ymax=1.5*(y1_inside(vx,ratio,E_field,b,t1_final)+y2_outside(ratio,t2_final,x_1,b,t1_final,E_field)), linewidth=3, color='black')
    plt.hlines(y=0, xmin=0, xmax=x1+x2, linestyles='dotted',color='black')

    #distance note
    # x1
    plt.plot((0,x1),(-1.3*D/2,-1.3*D/2), 'gray',) # arrow line
    plt.plot((0,0),(-1.3*D/2,-1.3*D/2), 'gray', marker='<',) # lower arrowhead
    plt.plot((x1,x1),(-1.3*D/2,-1.3*D/2), 'gray', marker='>',) # upper arrowhead
    plt.text(x1/2.5,-1.5*D/2,"x1={}".format(x1))

    #x2
    plt.plot((x1,x2+x1),(-1.3*D/2,-1.3*D/2), 'gray',) # arrow line
    plt.plot((x1,x1),(-1.3*D/2,-1.3*D/2), 'gray', marker='<',) # lower arrowhead
    plt.plot((x2+x1,x2+x1),(-1.3*D/2,-1.3*D/2), 'gray', marker='>',) # upper arrowhead
    plt.text(x1+x2/2.5,-1.5*D/2,"x2={}".format(x2))

    #D
    plt.plot((-0.1,-0.1),(-D/2,D/2), 'gray',) # arrow line
    plt.plot((-0.1,-0.1),(-D/2,-D/2), 'gray', marker='v',) # lower arrowhead
    plt.plot((-0.1,-0.1),(D/2,D/2), 'gray', marker='^',) # upper arrowhead
    plt.text(-0.15,-D/10,"D={}".format(D),rotation=90)

    # v_0
    plt.show()
    #circle1 = plt.Circle((-0.05, 0), D/10, color='r')
    #plt.show()
    return df


# Tunable input
V=0.43 # Hieu dien the giua 2 dau ban tu (voltage) # 2-20
D= 0.05 # Khoang cach giua 2 ban tu (meter) # 0.01-0.1
x1=0.2 # chieu dai ban tu (meter) #
x2= 0.2 # khoang cach den man chan (meter) #
B_field=0.001 # magnetic field (tesla)

m= path_function(V,D,x1,x2,B_field)
plt.show()
print(m)