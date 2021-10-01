import os.path, os, random
from typing import Collection
from collections import deque
from pathlib import Path

import os, sys
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

class Node:
    def __init__(self, asset_dir, count, children):
        self.asset_dir = asset_dir
        self.count = count
        self.children = children
        self.parent = None
        self.probability_map = None #TODO

        if children is None:
            return

        for child in children:
            child.parent = self

    def get_trace_paths(self):

        trace = list()
        trace.append(self.asset_dir)

        iter_parent = self.parent

        while iter_parent is not None:
            trace.append(iter_parent.asset_dir)
            iter_parent = iter_parent.parent

        trace.reverse()
        return trace

    def get_genes(self, trace):
        if self.probability_map is not None:
            raise Exception("TODO: Missing Feature")
        
        if self.count == 0:
            raise Exception("Overconsuming count")
        
        self.count -= 1

        genes = list()
        for dir in trace:
            selection = random.choice(os.listdir(dir))
            genes.append(os.path.splitext(selection)[0])

        return genes

    def generate_dna(self, genes):
        dna = "--".join(genes)
        return dna

    def process(self):

        if self.count == 0:
            return

        trace = self.get_trace_paths()

        while self.count > 0:    
            genes = self.get_genes(trace)
            dna = self.generate_dna(genes)


d_mask =  Node("D:\\Projects\\BadgerDAO\\PartyPenguins\\generation\\assets\\mask",4, None)
d_mouth = Node("D:\\Projects\\BadgerDAO\\PartyPenguins\\generation\\assets\\mouth",3, None)
d_face = Node("D:\\Projects\\BadgerDAO\\PartyPenguins\\generation\\assets\\race",2, [d_mask,d_mouth])
d_background = Node("D:\\Projects\\BadgerDAO\\PartyPenguins\\generation\\assets\\background", 0, [d_face])

dna_catalog = list()

g_dna_width = 3

def bfs_traverse_recursive(node):

    # Base case:
    if node is None:
        return
    if node.children == None:
        node.process()
        return

    # Recursion:
    for child in node.children:
        bfs_traverse_recursive(child)
    
    # Unwinding Work:
    node.process()

# MAIN
bfs_traverse_recursive(d_background)
print(*dna_catalog, sep = "\n")

# Generate CSV manually