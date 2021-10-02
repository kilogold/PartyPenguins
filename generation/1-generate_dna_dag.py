import os.path, os, random

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
            if child is not None:
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
        for dir in attr:
            if not dir in trace:
                genes.append("None")
            else:
                selection = random.choice(os.listdir(asset_dir + dir))
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
            dna_catalog.append(dna)


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

if __name__ == '__main__':

    attr = ["background", "race", "mouth", "mask", "hairhat", "glasses"]
    g_dna_width = len(attr)

    asset_dir = "D:\\Projects\\BadgerDAO\\PartyPenguins\\generation\\assets\\"
    
    d_root = \
    Node("background", 0, [
        Node("race", 20, [
            Node("mask", 40, None),
            Node("mouth", 30, None),
            Node("glasses", 30, [
                Node("mouth", 30, None),
                None
                ]), 
            Node("hairhat", 30, [
                Node("mask", 40, None),
                Node("mouth", 30, None),
                Node("glasses", 30, None),
                None
                ]) 
            ])
        ])

    dna_catalog = list()

    bfs_traverse_recursive(d_root)
    print(*dna_catalog, sep = "\n")

    # Generate CSV manually
    with open("dna_dag.csv", 'w') as out_file:
        out_file.write("serial,{},dna\n".format(",".join(attr)))

        for (i, entry) in enumerate(dna_catalog):
            line = "{},".format(i)
            line += entry.replace('--', ',')
            line += ",{}\n".format(entry)
            out_file.write(line)