# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 17:07:09 2022

@author: COM
"""

from abaqus import *
from abaqusConstants import *
import regionToolset
import __main__
import section
import regionToolset
import part
import material
import assembly
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import connectorBehavior
import odbAccess
from operator import add


import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# functions

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def Create_3D_Beam(model,part,length,height,thickness):
    s = mdb.models[model].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-length/2.0, height/2.0), point2=(length/2.0, -height/2.0))
    p = mdb.models[model].Part(name=part, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models[model].parts[part]
    p.BaseSolidExtrude(sketch=s, depth=thickness)
    s.unsetPrimaryObject()
    del mdb.models[model].sketches['__profile__']

#------------------------------------------------------------------------------

def Create_Assembly(model,part,instance,x,y,z):
    a = mdb.models[model].rootAssembly
    p = mdb.models[model].parts[part]
    a.Instance(name=instance, part=p, dependent=ON)
    p = a.instances[instance]
    p.translate(vector=(x,y,z))

#------------------------------------------------------------------------------

def Create_Analysis_Step(model,step_name,pre_step_name,Initial_inc,Max_inc,Min_inc,Inc_Number,NL_ON_OFF):
    a = mdb.models[model].StaticStep(name=step_name, previous=pre_step_name, initialInc=Initial_inc, maxInc=Max_inc, minInc=Min_inc, nlgeom=ON)
    a = mdb.models[model].steps[step_name].setValues(maxNumInc=Inc_Number)

#------------------------------------------------------------------------------

def Create_Gravity_Load(model,load_name,step_name,load):
    mdb.models[model].Gravity(name=load_name, createStepName=step_name, comp2=-load, distributionType=UNIFORM, field='')

#------------------------------------------------------------------------------

def Create_BC(model,set_name,BC_name,step_name,u,v,w,ur,vr,wr):
    a = mdb.models[model].rootAssembly
    region = a.sets[set_name]
    mdb.models[model].DisplacementBC(name=BC_name, createStepName=step_name, region=region, u1=u, u2=v, u3=w, ur1=ur, ur2=vr, ur3=wr, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

#------------------------------------------------------------------------------

def Create_Mesh(model,part,mesh_size):
    p = mdb.models[model].parts[part]
    p.seedPart(size=mesh_size, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()

#------------------------------------------------------------------------------

def Create_Material_and_Assign(model,part,material_name,E,Nu,Rho,section_name,set_name):
    p = mdb.models[model].parts[part]
    mdb.models[model].Material(name=material_name)
    mdb.models[model].materials[material_name].Elastic(table=((E, Nu), ))
    mdb.models[model].materials[material_name].Density(table=((Rho, ), ))
    mdb.models[model].HomogeneousSolidSection(name=section_name, material=material_name, thickness=None)
    p = mdb.models[model].parts[part]
    region = p.sets[set_name]
    p = mdb.models[model].parts[part]
    p.SectionAssignment(region=region, sectionName=section_name, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

#------------------------------------------------------------------------------

def Create_Job(model,job_name,cpu):
    a = mdb.models[model].rootAssembly
    mdb.Job(name=job_name, model=model, description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, multiprocessingMode=DEFAULT, numCpus=cpu, numDomains=cpu, numGPUs=0)

#------------------------------------------------------------------------------


myPart = "Beam_Part"
myString = "Simple_Beam"
mdb.Model(name=myString)
myMaterialName = "Concreate"



myLength = 4000.0
myHeight = 100.0
myThickness = 100.0

myE = 200000
myNu = 0.3
myRho = 7.8E-09



# Create 3D Beam

Create_3D_Beam(myString, myPart, myLength, myHeight, myThickness)

#Create Assembly

Create_Assembly(myString,myPart,"Beam-1",0,0,0)

# Create Analysis_Step

Create_Analysis_Step(myString,"Gravity","Initial",0.1,0.1,1E-05,1000,ON)
Create_Analysis_Step(myString,"Loading","Gravity",0.1,0.1,1E-05,1000,ON)

# Create Gravity Load

Create_Gravity_Load(myString,"Gravity","Gravity",9810)





    