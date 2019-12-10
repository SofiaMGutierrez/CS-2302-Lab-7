#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:33:13 2019

@author: sofiagutierrez
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import graph_AL as AL_graph
import graph_AM as AM_graph

class Edge:
    def __init__(self, source, dest, weight=1):
        self.source = source
        self.dest = dest
        self.weight = weight
        
class Graph:
    # Constructor
    def __init__(self,  vertices, weighted=False, directed = False):
        self.vertices = vertices
        self.el = []
        self.weighted = weighted
        self.directed = directed
        self.representation = 'EL'
        
    def insert_edge(self,source,dest,weight=1):
        self.el.append(Edge(source, dest, weight))
    
    def delete_edge(self,source,dest):
        for edge in self.el:
            if source == edge.source:
                if dest == edge.dest:
                    self.el.remove(edge)
                
    def display(self):
        print("[", end="")
        for edge in self.el:
            print("[" + str(edge.source), str(edge.dest), str(edge.weight) + "]", end=" ")

    def draw(self):
        self.as_AL().draw()
            
    def as_EL(self):
        return self
    
    def as_AM(self):
        # import AM from graph_AM.py
        from graph_AM import Graph
        AM = Graph(self.vertices, self.weighted, self.directed)
        for edge in self.el:
            AM.insert_edge(edge.source, edge.dest, edge.weight)
        return AM
    
    def as_AL(self):
        # import AL from graph_Al.py
        from graph_AL import Graph
        AL = Graph(self.vertices, self.weighted, self.directed)
        for edge in self.el:
            AL.insert_edge(edge.source, edge.dest, edge.weight)
        return AL

    def DFS(self, start, end):
        stack = [start]
        discoveredSet = [start]
        path = [-1] * 16
        while stack:
            v = stack.pop()
            for e in self.el:
                if e.source == v and e.dest not in discoveredSet:
                    stack.append(e.dest)
                    discoveredSet.append(e.dest)
                    path[e.dest] = e.source
        return path
    
    def BFS(self, start, end):
        queue = [start]
        discoveredSet = [start]
        path = [-1] * 16
        while queue:
            v = queue.pop(0)
            for e in self.el:
                if e.source == v and e.dest not in discoveredSet:
                    queue.append(e.dest)
                    discoveredSet.append(e.dest)
                    path[e.dest] = e.source
        return path

    def printPath(self, path, dest):
        if path[dest] != -1:
            self.printPath(path, path[dest])
            print(dest, end=' ')
        else:
            print(dest, end=' ')
            return -1
    
    def printDFS(self, start, end):
        path = self.DFS(start, end)
        self.printPath(path, end)
        print()
    
    def printBFS(self, start, end):
        path = self.BFS(start, end)
        self.printPath(path, end)
        print()