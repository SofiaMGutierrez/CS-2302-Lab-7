#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Course: CS 2302
Author: Sofia Gutierrez
Lab #7: The purpose of this lab
is to determine whether a graph
has a Hamiltonian cycle using 3
different algorithms: Randomization,
Backtracking, and Dynamic Programming
Instructor: Olac Fuentes
T.A.: Anindita Nath
"""
import numpy as np
import graph_AL as AL
import graph_EL as EL
import dsf
import random

#Function to find the number in-degrees of the current vertex, v
#The current vertex must have an in-degree of two in order to be
#considered a Hamiltonian cycle
def in_degree(G, v):
	in_degree_count = 0
	for i in range(len(G.al)):
		for edge in G.al[i]:
			if edge.dest == v:
				in_degree_count += 1
	return in_degree_count

#If connected_components returns a 1 this means that all vertices
#within the graph are connected and therefore a valid Hamiltonian Cycle
def connected_components(g):
    vertices = len(g.al)
    components = vertices
    s = dsf.DSF(vertices)
    for v in range(vertices):
        for edge in g.al[v]:
            components -= s.union(v,edge.dest)
    return components

#Function creates a path where each vertex is visited exactly once
def randomized_hamiltonian(V, maximum_trials=10000):
    edge_list = V.as_EL() #converts the adjacency list to an edge list
    
    for i in range(10000):
        edges = random.sample(edge_list.el, len(V.al)) #creates a random list of edges from edge_list
        al = AL.Graph(len(V.al), weighted=V.weighted, directed=V.directed) #creates an adjacency list
        
        for i in range(len(edges)):
            al.insert_edge(edges[i].source, edges[i].dest)
        
        #a valid Hamiltonian Cycle has a connected component of 1
        #meaning all nodes are connected to each other
        if connected_components(al) == 1:
            for i in range(len(al.al)):
                
                if in_degree(al,i) != 2: #every vertex within a Hamiltonian Cycle must have an in-degree of 2
                    return False
            return True

def randomized_check(V, maximum_trials=10000):
    for i in range(10000):
        if randomized_hamiltonian(V, maximum_trials=10000)==True:
            return True
    return False

#compute solution to original problem by combing solutions to subproblems
def backtracking_hamiltonian(V, Eh):
    
    if len(V.el) == V.vertices:
        AL_graph = V.as_AL()
        
        #if connected_components returns a 1 this means that all vertices
        #within the graph are connected and therefore a valid Hamiltonian Cycle
        if connected_components(AL_graph) == 1:
            for i in range(len(AL_graph.al)):
                
                #each vertex must have an in degree of 2
                if in_degree(AL_graph, i) != 2:
                    return None
            return AL_graph
    
    if len(Eh) > 0:
        V.el += [Eh[0]]
        a = backtracking_hamiltonian(V, Eh[1:])
        if a == None:
            V.el.remove(Eh[0])
            return backtracking_hamiltonian(V,Eh[1:])
        return a
    return

def backtracking_check(V):
    Eh = V.as_EL()
    el = EL.Graph(len(V.al), weighted=V.weighted, directed=V.directed)
    h = backtracking_hamiltonian(el, Eh.el)
    if isinstance(h, AL.Graph):
        #ham.display()
        return True
    else:
        return False

def edit_distance(s1, s2):
    v = ['a','e','i','o','u']
    d = np.zeros((len(s1)+1,len(s2)+1),dtype=int)
    d[0,:] = np.arange(len(s2)+1)
    d[:,0] = np.arange(len(s1)+1)
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            if s1[i-1] == s2[j-1]:
                d[i,j] = d[i-1,j-1]
            else:
                if (s1[i-1] in v and s2[j-1] in v):
                    n = [d[i,j-1],d[i-1,j-1],d[i-1,j]]
                    d[i,j] = min(n)+1
                if (s1[i-1] not in v and s2[j-1] not in v):
                    n = [d[i,j-1],d[i-1,j-1],d[i-1,j]]
                    d[i,j] = min(n)+1
                else:
                    n = [d[i,j-1],d[i-1,j]]
                    d[i,j] = min(n)+1
    return d[-1,-1]

if __name__=="__main__":

    #Graph with a Hamiltonian cycle
    g1 = AL.Graph(5)
    g1.insert_edge(0,1)
    g1.insert_edge(1,2)
    g1.insert_edge(2,3)
    g1.insert_edge(3,4)
    g1.insert_edge(4,0)
    g1.draw()
    
    #Graph without a Hamiltonian cycle
    g2 = AL.Graph(5)
    g2.insert_edge(0,2)
    g2.insert_edge(1,2)
    g2.insert_edge(2,3)
    g2.insert_edge(3,2)
    g2.insert_edge(4,2)
    g2.draw()

    if randomized_check(g1) == True:
        print("Hamiltonian cycle with randomization using g1 found")
    else:
        print("Hamiltonian cycle with randomization using g1 not found")

    if randomized_check(g2) == True:
        print("Hamiltonian cycle with randomization using g2 found")
    else:
        print("Hamiltonian cycle with randomization using g2 not found")



    if backtracking_check(g1) == True:
        print("Hamiltonian cycle with backtracking using g1 found")
    else:
        print("Hamiltonian cycle with backtracking using g1 not found")

    if backtracking_check(g2) == True:
        print("Hamiltonian cycle with backtracking using g2 found")
    else:
        print("Hamiltonian cycle with backtracking using g2 not found")

    word1 = str(input("Enter first word: "))
    word2 = str(input("Enter second word: "))
    print()
    print("Edit distance from", word1, "to", word2, ": ", edit_distance(word1, word2))