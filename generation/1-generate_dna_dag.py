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
                selection = self.__select_filepath(trace,dir)
                if "race_suda" in trace and dir == "background":
                    print(selection)
                genes.append(os.path.splitext(selection)[0])

        return genes

    
    def __determine_race(self, trace):
        return trace[1].removeprefix("race_") #HACK: Assuming this index is always the race.


    def __select_filepath(self, trace, dir): #TODO: Make more generic for Node class        
        # if "race_suda" in trace and dir == "hairhat": 
        #     dir = "hairhat_suda"

        # if dir == "fur_face" or dir == "fur_side" or dir == "fur_top":
        #     race_name = self.__determine_race(trace)
        #     dir = f"{dir}_{race_name}"
        
        return random.choice(os.listdir(asset_dir + dir))

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

    attr = [
    "background", 
    "race_american", "race_european", "race_pliotaxidea", "race_honey", "race_suda", 
    "fur_face_american", "fur_side_american", "fur_top_american", 
    "fur_face_european", "fur_side_european", "fur_top_european", 
    "fur_face_pliotaxidea", "fur_side_pliotaxidea", "fur_top_pliotaxidea", 
    "fur_face_honey", "fur_side_honey", "fur_top_honey", 
    "fur_face_suda", "fur_side_suda", "fur_top_suda", 
    "mouth", 
    "mask", 
    "hairhat", "hairhat_suda",
    "glasses"]

    g_dna_width = len(attr)

    asset_dir = "D:\\Projects\\BadgerDAO\\PartyPenguins\\generation\\assets\\"
    

    def get_predefined_node(race):
        race_name = race.removeprefix("race_")
        return  Node(race, 4, [
                    Node(f"fur_face_{race_name}", 0, [
                        Node(f"fur_side_{race_name}", 0, [
                            Node(f"fur_top_{race_name}", 0, [
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
                    ])
                ]) 


    d_root = \
    Node("background", 0, [
        get_predefined_node("race_american"), 
        get_predefined_node("race_european"), 
        get_predefined_node("race_pliotaxidea"), 
        get_predefined_node("race_honey"),
        Node("race_suda", 4, [
            Node(f"fur_face_suda", 0, [
                Node(f"fur_side_suda", 0, [
                    Node(f"fur_top_suda", 0, [
                        Node("mask", 40, None),
                        Node("mouth", 30, None),
                        Node("glasses", 30, [
                            Node("mouth", 30, None),
                            None
                        ]), 
                        Node("hairhat_suda", 30, [
                            Node("mask", 40, None),
                            Node("mouth", 30, None),
                            Node("glasses", 30, None),
                            None
                        ])
                    ])
                ])
            ])
        ]) 
    ])

    dna_catalog = list()

    bfs_traverse_recursive(d_root)
    
    # Uncomment to output result on console.
    #print(*dna_catalog, sep = "\n")

    # Generate CSV manually
    with open("dna_dag.csv", 'w') as out_file:
        out_file.write("serial,{},dna\n".format(",".join(attr)))

        for (i, entry) in enumerate(dna_catalog):
            line = "{},".format(i)
            line += entry.replace('--', ',')
            line += ",{}\n".format(entry)
            out_file.write(line)