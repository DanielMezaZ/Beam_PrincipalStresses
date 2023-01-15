# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 20:28:11 2022

@author: Daniel Meza
"""
# Only to visualize von Mises stresses and principal directions of a beam
import numpy as np
from matplotlib import pyplot as plt

def visualizeBeam(xDist,yDist,zDist,xNo,yNo,zNo,i):
    # Create homogenous samples in the space
    x = np.linspace(-xDist/2, xDist/2, num=xNo)
    y  =np.linspace(-yDist/2, yDist/2, num=yNo)
    z  =np.linspace(-zDist/2, zDist/2, num=zNo) #Never used (yet)
    
    # Build a grid from the sample points
    #[xs,ys,zs] = np.meshgrid(x, y, z)
    [xs,ys] = np.meshgrid(x, y)
    
    # Compute the stress components in the beam
    sigma11=(xs**2-(xDist/2)**2)*ys+2*(yDist/2)**2*ys/5-2*ys**3/3
    sigma22=ys**3/3-(yDist/2)**2*ys-2*(yDist/2)**3/3
    sigma33=0
    sigma12=xs*((yDist/2)**2-ys**2)
    sigma13=0
    sigma23=0
    
    # Compute the von Mises stress in the beam
    sigmaVM=(sigma11-sigma22)**2+(sigma22-sigma33)**2+(sigma33-sigma11)**2
    sigmaVM=sigmaVM+6*(sigma12**2+sigma23**2+sigma13**2)
    sigmaVM=np.sqrt(sigmaVM) 
    
    # Intermediate step: assign values (color in the plot) to the von Mises stress
    values= sigmaVM
    
    # Plot von Mises stress
    axes[i,0].contourf(xs, ys, values,20)
    axes[i,0].set_title(f"VM Stress, {xDist}X{yDist}")
    
    ## 3D - too complicated, maybe another day
    #ax = plt.axes(projection='3d')
    #ax.scatter(xs, zs, ys, c= values, cmap='coolwarm', linewidth=1);
    #ax.quiver(xs, zs, ys, u, v, w, length=0.025)
    #plt.colorbar()
    
    # sigma1=(sigma11+sigma22)/2+np.sqrt(((sigma11-sigma22)/2)**2+sigma12**2)
    # sigma2=(sigma11+sigma22)/2-np.sqrt(((sigma11-sigma22)/2)**2+sigma12**2)
    # theta=0.5*np.arctan(2*sigma12/(sigma11-sigma22))
    # theta=theta +(sigma12-np.abs(sigma12))/(2*sigma12)*np.pi
    # [u,v,w]=(sigma1*np.cos(theta),sigma1*np.sin(theta),1)
    # u=u*np.abs(sigma12)/sigma12
    # axes[0,1].quiver(xs, ys, u, v, color='red', cmap='coolwarm')
    # [u,v,w]=(sigma2*np.cos(theta+np.pi/2),sigma2*np.sin(theta+np.pi/2),1)
    # u=u*np.abs(sigma12)/sigma12
    # axes[0,1].quiver(xs, ys, u, v, color='blue', cmap='coolwarm')
    # #plt.quiver(xs, ys, u, v, color='black')
    # axes[0,1].set_title("Principal stresses, 5X1")
    
    # Compute principal stresses
    sigma1=(sigma11+sigma22)/2+np.sqrt(((sigma11-sigma22)/2)**2+sigma12**2)
    sigma2=(sigma11+sigma22)/2-np.sqrt(((sigma11-sigma22)/2)**2+sigma12**2)
    # Compute principal direction
    theta=0.5*np.arctan(2*sigma12/(sigma11-sigma22))
    
    # Create vector field of principal stress 1
    [u,v,w]=(sigma1*np.cos(theta),sigma1*np.sin(theta),1)
    # Plot principal stress 1 with red
    axes[i,1].quiver(xs, ys, u, v, color='red', cmap='coolwarm')
    
    # Create vector field of principal stress 2
    [u,v,w]=(sigma2*np.cos(theta+np.pi/2),sigma2*np.sin(theta+np.pi/2),1)
    # Plot principal stress 2 with blue
    axes[i,1].quiver(xs, ys, u, v, color='blue', cmap='coolwarm')
    axes[i,1].set_title(f"Principal stresses, {xDist}X{yDist}")

# To simplify, code is repeated here for each beam 

# Insert the dimensions of the beam (x_1,x_2,x_3)
xDist=[5,5,5]
yDist=[5,2.5,1]
zDist=[1,1,1] # not used yet

# Insert the number of poins in each direction (x,y,z)
xNo=[30,30,30]
yNo=[30,30,30]
zNo=[1,1,1]

# Create a plot array
nBeams=np.array(xDist).size
fig, axes = plt.subplots(nrows=nBeams, ncols=2, figsize=(5, 5))

for i in range(nBeams):
    visualizeBeam(xDist[i],yDist[i],zDist[i],xNo[i],yNo[i],zNo[i],i)

fig.tight_layout()
fig.savefig("beam_VonMises-PrincipalStresses.png", dpi=300)

