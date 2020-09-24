# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 13:09:16 2020

@author: Pramesh Kumar
"""
import gurobipy as gp
from gurobipy import GRB

model = gp.read('model.lp')


model.Params.outputFlag = 0
model.Params.DualReductions  = 0

model.optimize()

if model.status == GRB.OPTIMAL:
    print('model is optimal')
elif model.status ==GRB.INFEASIBLE:
    print('model is infeasible')
elif model.status == GRB.UNBOUNDED:
    print('model is unbounded')
else:
    print('Not sure')
    
    
#model.Params.InfUnbdInfo = 1
    

#model.computeIIS()
#model.write("infeasible_model.lp")
    
 
print('The otimal value of the model is', model.objVal)

for k in model.getVars():
    print(k.varName, ' = ', k.x)
    

    

    

    