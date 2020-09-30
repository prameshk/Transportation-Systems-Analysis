# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:58:56 2020

@author: Pramesh Kumar
"""
import networkx as nx #improting the package as "nx"
from gurobipy import *


nodes = [1, 2, 3, 4, 5, 6, 7] # Make a list of nodes
links = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4), (3, 6), (4, 6), (6, 5), (4, 5), (5, 7), (6, 7)] # Make a list of links


costs = {(1, 2): 6, (1, 3): 7, (2, 3): 2, (2, 4): 3, (3, 4): 2, (2, 5): 4, (3, 6): 5, (4, 5): 3, (4, 6): 2, (6, 5): 2, (5, 7): 7, (6, 7): 4}

outLinks = {1: [(1, 2), (1, 3)], 2: [(2, 5), (2, 4), (2, 3)], 3: [(3, 4), (3, 6)], 4: [(4, 5), (4, 6)], 5:[(5, 7)], 6: [(6, 5), (6, 7)], 7: []}
inLinks = {1:[], 2:[(1, 2)], 3:[(1, 3), (2, 3)], 4:[(2, 4), (3, 4)], 5:[(2, 5), (4, 5), (6, 5)], 6:[(3, 6), (4, 6)], 7:[(5, 7), (6, 7)]}

capacity = {(1, 2): 15, (1, 3): 10, (2, 3): 3, (2, 4): 7, (3, 4):4, (2, 5): 18, (4,5): 2, (4, 6): 2, (3, 6): 5, (6, 7):1, (6, 5): 3, (5, 7):float("inf")}

# Setting up the graph for networkx
g = nx.DiGraph() # Initialize the directed graph
g.add_nodes_from(nodes) # Add nodes to the graph from the list we created
g.add_edges_from(links) # Add links from the list we created    


# Drawing the graph 
import matplotlib.pyplot as plt # import this package to plot the graph
pos = nx.random_layout(g) # To get the coordinates of nodes
nx.draw(g, with_labels=True, pos=pos) # We specify the graph, position, etc.

# Shortest path 
m = Model()
x = m.addVars(links, vtype = GRB.BINARY)
m.addConstr(x[(1, 2)] + x[(1, 3)] == 1)
m.addConstr(x[(5, 7)] + x[(6, 7)] == 1)

for i in nodes:
    if i not in [1, 7]:        
        tmp = sum(x[a] for a in outLinks[i]) - sum(x[a] for a in inLinks[i])
        m.addConstr(tmp ==0)
        
obj = sum([costs[a]*x[a] for a in links])        
m.setObjective(obj, sense = GRB.MINIMIZE)        
m.Params.outputFlag = 0
m.update()
m.optimize()
if m.status == 2:
    print('Shortest path using gurobi: ', [k for k in x if x[k].x != 0])
    print('The cost of the shortest path using gurobi: ', m.objVal)

for (a, b) in links:
    g[a][b]['cost'] = costs[a, b] # Adding costs to the edges
    
p = nx.shortest_path(g, source=1, target = 7, weight = 'cost') # Computes a shortest path in the network 
print('shorest path between using networkx is: ' , p) # prints the path

l = nx.shortest_path_length(g, source=1, target = 7, weight = 'cost') # Computes the cost of the shortest path
print('The cost of the shortest path using gurobi: ', l)
print('########################################################################')


# Min cost flow problem
m = Model()
x = m.addVars(links, vtype = GRB.INTEGER)
m.addConstr(x[(1, 2)] + x[(1, 3)] == 20)
m.addConstr(x[(5, 7)] + x[(6, 7)] == 20)


for i in nodes:
    if i not in [1, 7]:        
        tmp = sum(x[a] for a in outLinks[i]) - sum(x[a] for a in inLinks[i])
        m.addConstr(tmp ==0)
 

        
for a in links:
    m.addConstr(x[a] <= capacity[a])
        
obj = sum([costs[a]*x[a] for a in links])        
m.setObjective(obj, sense = GRB.MINIMIZE)        
m.Params.outputFlag = 0
m.update()
m.optimize()
if m.status == 2:
    print('Flow on various links using gurobi: ', {k:x[k].x for k in x})
    print('Total cost of flow: ', m.objVal)

else:
    m.computeIIS() 
    m.write("infeasible_model.lp")
    
g.nodes[1]['demand'] = -20 # -ve because this is to be sent.
g.nodes[7]['demand'] = 20

# Let's add the capacity attribute
for (a, b) in capacity:
    g[a][b]['capacity'] = capacity[a, b] # Adding costs to the edges

flowDict = nx.min_cost_flow(g, demand='demand', capacity='capacity', weight='cost') 

# To print the flow on edges
print('Flow on various links using networkx is: ', {k:flowDict[k[0]][k[1]] for k in links})
print('########################################################################')




# Max flow problem
m = Model()
x = m.addVars(links, vtype = GRB.INTEGER)
v = m.addVar(vtype = GRB.INTEGER)

m.addConstr(x[(1, 2)] + x[(1, 3)] == v)
m.addConstr(x[(5, 7)] + x[(6, 7)] == v)

for i in nodes:
    if i not in [1, 7]:        
        tmp = sum(x[a] for a in outLinks[i]) - sum(x[a] for a in inLinks[i])
        m.addConstr(tmp ==0)
        
for a in links:
    m.addConstr(x[a] <= capacity[a])
        
      
m.setObjective(v, sense = GRB.MAXIMIZE)        
m.Params.outputFlag = 0
m.update()
m.optimize()
if m.status == 2:
    print('Flow on various links using gurobi: ', {k:x[k].x for k in x if x[k]})
    print('Maximum flow: ', m.objVal)

else:
    m.computeIIS() 
    m.write("infeasible_model.lp")

results = nx.maximum_flow(g, 1, 7, capacity='capacity')
print('maximum flow using networkx:', results[0])
print('The flow on edges are: ', {k:results[1][k[0]][k[1]] for k in links})

# Transportation problem
m = Model()
x = m.addVars(links, vtype = GRB.INTEGER)

m.addConstr(x[(1, 2)] + x[(1, 3)] == 20)
m.addConstr(x[(5, 7)] + x[(6, 7)] == v)

for i in nodes:
    if i not in [1, 7]:        
        tmp = sum(x[a] for a in outLinks[i]) - sum(x[a] for a in inLinks[i])
        m.addConstr(tmp ==0)
        
for a in links:
    m.addConstr(x[a] <= capacity[a])
        
      
m.setObjective(v, sense = GRB.MAXIMIZE)        
m.Params.outputFlag = 0
m.update()
m.optimize()
if m.status == 2:
    print('Flow on various links using gurobi: ', {k:x[k].x for k in x if x[k]})
    print('Maximum flow: ', m.objVal)

else:
    m.computeIIS() 
    m.write("infeasible_model.lp")

