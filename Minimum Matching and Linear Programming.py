#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pandas import DataFrame
import networkx as nx
from gurobipy import *

#load data from dataset,filter the data based on passenger number
def Get_dist(f):
    data = pd.read_csv(f, header = 0)
    DataFrame = pd.DataFrame(data)
    DataFrame['passenger_count'] = DataFrame['passenger_count'].apply(pd.to_numeric)
    data_filtered = DataFrame.query(data, 'passenger_count<=2')
    dist = data_filtered.iloc[:, [5, 6, 9, 10]]
    return dist

# Define manhattan distance
def compute_distance(x1, y1, x2, y2):
    return (abs(x1 - x2) + abs(y1 - y2))


# Algorithm1: Minimum Matching

# Compute the minimum pooling plan between two passengers. 0:xyxy, 1:xyyx, 2:yxxy, 3:yxyx; 4:no pool
def min_matching(x, y):
    x1y1 = compute_distance(x[0], x[1], y[0], y[1])
    x2y1 = compute_distance(x[2], x[3], y[0], y[1])
    x1y2 = compute_distance(x[0], x[1], y[2], y[3])
    x2y2 = compute_distance(x[2], x[3], y[2], y[3])
    y1y2 = compute_distance(y[0], y[1], y[2], y[3])
    x1x2 = compute_distance(x[0], x[1], x[2], x[3])
    dist = {}
    # If pooling distance if larger than 1.25times of individual trip, then passenger will not be pooled
    if (x1y1 + x2y1) > 1.25 * (x1x2) or (x2y1 + x2y2) > 1.25 * (y1y2):
        dist[0] = 1000
    else:
        dist[0] = x1y1 + x2y1 + x2y2
    if (x1y1 + y1y2 + x2y2) > 1.25 * (x1x2):
        dist[1] = 1000
    else:
        dist[1] = x1y1 + y1y2 + x2y2
    if (y1y2 + x1x2 + x2y2) > 1.25 * (y1y2):
        dist[2] = 1000
    else:
        dist[2] = x1y1 + x1x2 + x2y2
    if (x1y1 + x1y2) > 1.25 * (y1y2) or (x1y2 + x2y2) > 1.25 * (x1x2):
        dist[3] = 1000
    else:
        dist[3] = x1y1 + x2y1 + x2y2
    dist[4] = x1x2 + y1y2 + 10
    return min(dist.items(), key=lambda x: x[1])


def ipedge(x, y):
    weight = min_matching(x, y)
    route = weight[0]
    if route == 4:
        return 0
    else:
        return 1


# Calculate the minimum pooling among all the data points
def min_matching_graph(dist):
    G = nx.DiGraph()
    pos = {}
    n = dist.shape[0]
    for i in range(n):
        G.add_node(i, x=dist[i][0], y=dist[i][1])
        pos[i] = (dist[i][0], dist[i][1])
    for i in range(n):
        for j in range(i):
            G.add_edge(i, j, weight=ipedge(dist[i], dist[j]))
            G.add_edge(j, i, weight=ipedge(dist[i], dist[j]))
    labels = nx.get_edge_attributes(G, 'weight')
    print(labels)
    return list(G.nodes()), labels


# Calculate average pooling distance and output the optimum plan
def pool(route, dist):
    n = dist.shape[0]
    m = int(n / 2)
    pool_dist = np.full((m), fill_value=np.nan)
    pool_route = np.full((m), fill_value=np.nan)
    i = 0
    while i in range(n - 1):
        j = int(i / 2)
        pool_dist[j] = min_matching(dist[route[i]], dist[route[i + 1]])[1]
        pool_route[j] = min_matching(dist[route[i]], dist[route[i + 1]])[0]
        i = i + 2
    return pool_dist, pool_route, sum(pool_dist)



# Algorithm2: integer programming
def twoCycle(vertices, edges):
    '''
    Returns a dictionary of 2 cycles. Keys: (u,v), Value: weight of cycle
    Note that u < v to not double count cycles.
    '''
    twoCycles = {}
    for edge in edges:
        u = edge[0]
        v = edge[1]
        if (u < v and (v,u) in edges):
            twoCycles[(u,v)] = edges[(u,v)] + edges[(v,u)]
    return twoCycles

def threeCycle(vertices, edges):
    '''
    Returns a dictionary of 3 cycles. Keys: (u,w,v), Value: weight of cycle
    Note that w is always the lowest numbered vertex to not double
    (or triple) count cycles.
    '''
    threeCycles = {}
    for edge in edges:
        u = edge[0]
        v = edge[1]
        for w in vertices:
            if (w >= u or w >= v ):
                break
            if ( (u,w) in edges and (w,v) in edges ):
                threeCycles[(u,w,v)] = edges[(u,v)] + edges[(u,w)] + edges[(w,v)]
    return threeCycles


dist = Get_dist(b)
vertices,edges= min_matching_graph(dist)
twoCycles = twoCycle(vertices, edges)
threeCycles = threeCycle(vertices, edges)



# Gurobi
m = Model()

c = {}

for cycle in twoCycles:
    c[cycle] = m.addVar(vtype=GRB.BINARY, name="c_%s" % str(cycle))

for cycle in threeCycles:
    c[cycle] = m.addVar(vtype=GRB.BINARY, name="c_%s" % str(cycle))

m.update()

for v in vertices:
  constraint = []
  for cycle in c:
      if (v in cycle):
          constraint.append(c[cycle])
  if constraint:
      m.addConstr( quicksum( constraint[i] for i in range(len(constraint)) ) <= 1 , name="v%d" % v)

m.setObjective( quicksum( c[cycle] * twoCycles[cycle] for cycle in twoCycles ) +
                quicksum( c[cycle] * threeCycles[cycle] for cycle in threeCycles ),
                GRB.MAXIMIZE )

m.optimize()

obj = m.getObjective()
print(obj)


