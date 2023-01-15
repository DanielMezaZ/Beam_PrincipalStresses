# -*- coding: utf-8 -,0*-
"""
Created on Thu Jan  5 22:35:09 2023

@author: Daniel Meza
"""

# To generate path of lines following the principal stresses \
    # and export as gcode (sort of)
# Writes in the output.txt file, which then has to be manually copied intt
# Beam_template.gcode
# This could be automated, but I was using Windows and don't like batch

import numpy as np
from matplotlib import pyplot as plt

# Arrays with coordinates to print
xCoords=np.array([])
yCoords=np.array([])

# Define functions for stress components
# Actually they coud be writen inside of evalAngle, but I wanted to \
    # make the values accesible from outside of that function
    
def sigma11(x,y,xDist,yDist):
    return (x**2-(xDist/2)**2)*y+2*(yDist/2)**2*y/5-2*y**3/3
def sigma22(x,y,xDist,yDist):
    return (y**3/3-(yDist/2)**2*y-2*(yDist/2)**3/3)
def sigma12(x,y,xDist,yDist):
    return (x*((yDist/2)**2-y**2))

def evalAngle(coords,typ):
    # Find direction of principal stresses array
    # Typ describes the line type
    # 0 for horizontal lines -> can only move right
    # 1 for vertical lines -> can only move down
    s11=sigma11(coords[0],coords[1],xDist,yDist)
    s22=sigma22(coords[0],coords[1],xDist,yDist)
    s12=sigma12(coords[0],coords[1],xDist,yDist)

    # Get angle
    theta=0.5*np.arctan(2*s12/(s11-s22))
    # Constraint motion. Needed to ensure that the line does not get stuck
    
    # Example: At point A the angle is 0. After one step, at point B, the angle \
        # is 180. After one more step, we go back to point A and the process \
        # continues until the program ends
    
    # Vertical lines use the second main direction (90 DEG rotation)
    # Principal stresses are perpendicular to each other
    # Maybe here there's the constraint making the lines meet perpendicularly
    theta=theta+np.pi/2*typ*np.ones(theta.size)
    
    for i in range(theta.size):
        # -Vertical lines to move down only
        if typ==1 and theta[i]>0:
            theta[i]=theta[i]-np.pi
        # -Horizontal lines to move right only
        if typ==0 and (theta[i]>np.pi/2 or theta[i]<-np.pi/2):
            theta[i]=theta[i]-np.pi       
    return theta

[xDist,yDist,zDist]=(50,25,1)     # Define bar dimensions in mm
[xNo,yNo,step]=(8,5,1.0)          # Define number of horizontal, vertical lines and step size
# Note: after each iteration, the point moves one step of constant length in the principal direction

# Set limits for the plot
plt.xlim([-xDist/2*1.1,xDist/2*1.1])
plt.ylim([-yDist/2*1.1,yDist/2*1.1])

# Create points for the borders
# Width of line in mm
w=0.4
# Offset: overlap of borders with the inner space in mm
offset=-0.4
# When a new line is created, instead of appending coordinates, the string \
    # "New line" is appended for later (measures to prevent stringing in print)
    
# The points of the borders are plotted with red
for i in range(4): # Range represents the number of lines in the border
    # Bounds 1
    xCoords=np.append(xCoords,"New line")
    yCoords=np.append(yCoords,"New line")
    y=np.linspace(-(yDist/2+offset),(yDist/2+offset),round((yDist+2*offset)/step)+1)
    x=np.linspace(-(xDist/2+offset),(xDist/2+offset),round((xDist+2*offset)/step)+1)
    # Top
    plt.scatter(x, np.ones(x.size)*(yDist/2+offset), c="red")
    yCoords=np.append(yCoords,np.ones(y.size)*(yDist/2+offset))
    xCoords=np.append(xCoords,x)
    # Right
    plt.scatter(np.ones(y.size)*(xDist/2+offset),-y, c="red")
    xCoords=np.append(xCoords,np.ones(x.size)*(xDist/2+offset))
    yCoords=np.append(yCoords,-y)
    # Bottom
    plt.scatter(-x,-np.ones(x.size)*(yDist/2+offset), c="red")
    yCoords=np.append(yCoords,np.ones(y.size)*-(yDist/2+offset))
    xCoords=np.append(xCoords,-x)
    # Left
    plt.scatter(np.ones(y.size)*-(xDist/2+offset),y, c="red")
    xCoords=np.append(xCoords,np.ones(x.size)*-(xDist/2+offset))
    yCoords=np.append(yCoords,y)
    offset=offset+w
            
# Vertical lines
# Starting from top with power distribution across 0
dist=np.linspace(-0.8, 0.8, num=xNo)        # Tune changing the bounds of the sample
x=np.abs(dist)**1.2*xDist/2*np.sign(dist)   # Tune power for distribution density. Hint >1
for xVar in x:
    yVar=yDist/2
    x_i=np.array([xVar,yVar])  # Starting point
    xCoords=np.append(xCoords,"New line")
    yCoords=np.append(yCoords,"New line")
    # Initial point with black
    plt.scatter(x_i[0],x_i[1],c="black")
    # Append coordinates
    xCoords=np.append(xCoords,x_i[0])
    yCoords=np.append(yCoords,x_i[1])
    # Repeat until a point is outside the domain of the beam
    cond=False # control variable
    while cond==False:
        theta = evalAngle(x_i, 1)       # Get principal direction
        # Move one step in the principal direction 
        x_i[0]=x_i[0]+step*np.cos(theta)
        x_i[1]=x_i[1]+step*np.sin(theta)
        # If a coordinate is outside the domain, place it within the domain \
            # and finalize the loop
        if np.abs(x_i[0])>xDist/2:
            x_i[0]=xDist/2*np.sign(x_i[0])
            cond=True
        if np.abs(x_i[1])>yDist/2:
            x_i[1]=yDist/2*np.sign(x_i[1])
            cond=True
            
        if cond==False:
            # Plot horizontal points with green
            plt.scatter(x_i[0],x_i[1],c="green")
        else:
            # Plot end points with black
            plt.scatter(x_i[0],x_i[1],c="black")
        # Append coordinates
        xCoords=np.append(xCoords,x_i[0])
        yCoords=np.append(yCoords,x_i[1])

# Horizontal lines
# Starting from left with power distribution across -yDist/2
dist=np.linspace(0.15, 0.85, num=yNo)     # Tune changing the bounds of the sample
y=np.abs(dist)**0.85*yDist*np.sign(dist)-yDist/2+yDist/yNo/2 # Tune power for distribution density. Hint < 1
for yVar in y:
    xVar=-xDist/2
    x_i=np.array([xVar,yVar])  # Starting point
    xCoords=np.append(xCoords,"New line")
    yCoords=np.append(yCoords,"New line")
    plt.scatter(x_i[0],x_i[1],c="black")
    xCoords=np.append(xCoords,x_i[0])
    yCoords=np.append(yCoords,x_i[1])
    cond=False
    while cond==False:
        theta = evalAngle(x_i, 0)       # Get principal direction
        # Move one step in the principal direction 
        x_i[0]=x_i[0]+step*np.cos(theta)
        x_i[1]=x_i[1]+step*np.sin(theta)
        if np.abs(x_i[0])>xDist/2:
            x_i[0]=xDist/2*np.sign(x_i[0])
            cond=True
        if np.abs(x_i[1])>yDist/2:
            x_i[1]=yDist/2*np.sign(x_i[1])
            cond=True
        if cond==False:
            # Plot points with blue
            plt.scatter(x_i[0],x_i[1],c="blue")
        else:        
            # Plot endpoints with black
            plt.scatter(x_i[0],x_i[1],c="black")
        # Append coordinates to array
        xCoords=np.append(xCoords,x_i[0])
        yCoords=np.append(yCoords,x_i[1])

plt.title(f"Printing Points_xDist{xDist}_yDist{yDist}_xNo{xNo}_yNo{yNo}_step{step}")
plt.tight_layout()
plt.savefig(f"printingCoordsScatter_xDist{xDist}_yDist{yDist}_xNo{xNo}_yNo{yNo}_step{step}.png", dpi=300)

print ("Done building coordinates")


# print ("Exporting to gcode")

# # Note: Need an output.txt file in the working directory
# f=open("output.txt","w")
# E = 19.124          # Initial extrusion point, based on beam_template.gcode
# x_0=120             # Center of printing bed in x
# y_0=120             # Center of printing bed in y
# z_0=-0.1            # Starting z coordinate, goes to 0.3 after the first iteration
# x=95                # Initial x coordinate, based on beam_template.gcode
# y=95                # Initial y coordinate, based on beam_template.gcode
# E_val=round(0.071177*step,5)    # Extrusion distance in the stepper motor for one step
# newLinePrev=False   # Control variable to detect new lines and prevent stringing
# f.write(";START\n") # Write comment as reference
# for j in range(35): # Loop being repeated for each layer, total of 35 here
#     f.write(f";LAYER {j}\n") # Comment of a new layer being added
#     z_0=round(z_0+0.4,3)    # Update z coordinate
#     f.write(f"G0 F7200 Z{z_0}\n")   # Move in z direction
#     for i in range(xCoords.size):
#         # If new line, update control variable and carry out routine to prevent stringing
#         if xCoords[i]=="New line":
#             newLinePrev=True
#             f.write(f"G1 F1000 E{E-2}\n")   # Retract filament 2 mm
#             f.write("G4 P500\n")            # Wait 500 ms
#             f.write(f"G0 F4200 Z{z_0+1}\n") # Move 1 mm in z
#             f.write(f"G0 F4200 X{x} Y{y-10}\n") # Go outside of the beam domain
#         else:
#             x=round(float(xCoords[i]),3)+x_0    # Update x coordinate using offset
#             y=round(float(yCoords[i]),3)+y_0    # Update y coordinate using offset
#             # Standard procedure, move to new coordinate and extrude filament
#             if newLinePrev==False:
#                 E=E+E_val
#                 f.write(f"G1 F1000 X{x} Y{y} E{E}\n")
#             else:
#             # If starting a new line, special procedure to prevent stringing
#                 f.write(f"G0 F4200 X{x} Y{y}\n")    # Go to coordinate
#                 f.write(f"G1 F1000 E{E}\n")         # Move back filament retraction
#                 f.write(f"G0 F4200 Z{z_0}\n")       # Move back in z-direction
#                 f.write("G4 P500\n")                # Wait 500 ms
#             newLinePrev=False                       # Reset control variable
# f.write(";END\n") # Write comment as reference
# f.close()
# print("Finished exporting")