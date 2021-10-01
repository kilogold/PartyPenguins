import csv
dna_file = "dna_dag.csv"

dnas = []
with open(dna_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        dnas.append(row)

columns = list(dnas[0].keys())
all_params = []

for dna in dnas:
    traits = [f'{key}/{dna[key]}' for key in columns if key not in set(['serial', 'dna']) and dna[key]!= 'NONE']

    trait_vals = [t.split('/')[-1] for t in traits]
    all_params.append([dna['serial'], traits])


metadata_template = \
r"""
{{
  "attributes": [
      {}
  ],
  "description": "A proto-BadgerPunk to be tested on OpenSea.",
  "external_url": "https://discord.gg/PRVyFKKStt",
  "image": "http://kraniumtivity.com/Extra/BadgerPunks_Dev/{}.png",
  "name": "{}"
}}
"""

def metadata_trait(trait_type, value, display_type):
    return r"""
    {{
      {}
      "trait_type": "{}",
      "value": "{}"
    }}
    """.format("" if display_type is None else display_type, trait_type, value)

def metadata_generate():
    name = "Proto badger #{}".format(d['serial'])
    attributes_string = str()
    attribute_name = columns[2] #temp var

    metadata_attributes = [
        (attribute_name, d[attribute_name])
    ]

    for t in metadata_attributes:
        appending_trait = metadata_trait(t[0], t[1], None)
        attributes_string = attributes_string.join(appending_trait)

        if t != metadata_attributes[-1] and len(metadata_attributes) > 1:
            attributes_string += ',\n'


    return metadata_template.format(attributes_string, d['serial'] ,name)

def metadata_serialize(metadata, dry_run):
    if dry_run:
        print(metadata)
        return

    filepath = 'output/' + d['serial'] 
    fout = open(filepath, 'w')
    fout.write(metadata)
    fout.close()

if __name__ == "__main__":
    name_template = "Proto badger"

    for d in dnas:
        output = metadata_generate()
        metadata_serialize(output, False)

