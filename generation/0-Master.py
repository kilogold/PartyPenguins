import importlib.machinery
import importlib.util

# Import mymodule
loader = importlib.machinery.SourceFileLoader( '1-generate_dna_dag', '1-generate_dna_dag.py' )
spec = importlib.util.spec_from_loader( '1-generate_dna_dag', loader )
mymodule = importlib.util.module_from_spec( spec )
loader.exec_module( mymodule )


import importlib  
Test = importlib.import_module("1-generate_dna_dag.py", None)
foobar = importlib.import_module("2-generate_penguin_meta.py")
foobar = importlib.import_module("3-generate_penguin.py")

