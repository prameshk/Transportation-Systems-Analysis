# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:59:51 2020

@author: Pramesh Kumar
"""
import networkx as nx

nodes = [1, 2, 3, 4, 5] # List of the nodes

links = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)] # List of links

g = nx.DiGraph()

# Adding nodes and links to the graph
g.add_nodes_from(nodes)
g.add_edges_from(links)


# Drawing a network
import matplotlib.pyplot as plt
position = nx.random_layout(g)
nx.draw(g, with_labels =True, pos = position)


# Shortest path problem
costs = {(1, 2): 4, (1, 3):4, (2, 3): 2, (2, 4):2, (2, 5): 6, (3, 4): 1, (3, 5): 1, (4, 5): 2}

for (a, b) in links:
    g[a][b]['cost'] = costs[a, b]
    
p = nx.shortest_path(g, source= 1, target = 5, weight = 'cost')   
print('shortest path from 1 to 5 is:', p)

l = nx.shortest_path_length(g, source= 1, target = 5, weight = 'cost') 
print('The cost of the shortest path from node 1 to node 5 is:', l)

sp = nx.shortest_path(g, source = 1, weight = 'cost')

for n in nodes:
    print('Shortest path from node 1 to ', n, ' is:', sp[n])
    
# Minimum cost flow problem
g.nodes[1]['demand'] = -20
g.nodes[4]['demand'] = 5
g.nodes[5]['demand'] = 15

capacity = {(1, 2): 15, (1, 3): 8, (2, 3) : float("inf"), (2, 4):4, (2, 5):10, (3, 4):15, (3, 5):4, (4, 5): float("inf")}

for (a, b) in links:
    g[a][b]['capacity'] = capacity[a, b]
    
flow = nx.min_cost_flow(g, demand = 'demand', capacity = 'capacity', weight = 'cost')

for (a, b) in links:
    print('The flow on edge' , (a, b), 'is: ', flow[a][b])
    
# Solving the maximum flow problem
maxFlow = nx.maximum_flow(g, 1, 5, capacity = 'capacity')

print('Printing max flow results')
print('The maximum flow that we can send from node 1 to 5 is: ', maxFlow[0])


for (a, b) in links:
    print('The flow on edge' , (a, b), 'is: ', maxFlow[1][a][b])   
    
# matching problem
print('matches are ', nx.max_weight_matching(g, weight = 'cost', maxcardinality =False))


# How to use Gurobi for solving the max flow problem

from gurobipy import *

m = Model()

# Decisions
v = m.addVar(vtype = GRB.CONTINUOUS)
x = m.addVars(links, vtype = GRB.INTEGER)

links = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)] # List of links

forwardStar = {1:[2, 3], 2:[3, 4], 3:[4], 4:[5], 5:[]}
backwardStar = {1:[], 2:[1], 3:[1, 2], 4:[2, 3], 5:[2, 4]}

# Constraints
origin = 1
dest = 5

m.addConstr(sum([x[origin, k] for k in forwardStar[origin]]) == v)
m.addConstr(sum([x[k, dest] for k in backwardStar[dest]]) == v)

for n in nodes:
    if n not in [origin, dest]:
        m.addConstr(sum([x[n, k] for k in forwardStar[n]]) == sum([x[k, n] for k in backwardStar[n]]))
        
for a in links:
    m.addConstr(x[a] <= capacity[a])
    
obj = v
m.setObjective(obj, sense = GRB.MAXIMIZE)
m.optimize()


print(m.status)    





    
    
    


