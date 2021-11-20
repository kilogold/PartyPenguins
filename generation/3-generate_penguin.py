from PIL import Image, ImageSequence
import csv
import time
import os
from multiprocessing import Pool

override = True
asset_folder = "assets"
dna_file = "dna_dag.csv"
output_folder = "output"

def open_all_assets(traits):
    all_assets = list()
    for trait in traits:
        
        path = f'{asset_folder}/{trait}.png'
        if not os.path.exists(path):
            path = f'{asset_folder}/{trait}.gif'
        
        all_assets.append(Image.open(path))
    
    return all_assets


def combine_with_gif_background(all_assets, output_filepath):
    
    def blend(background, foreground):
        center_point_background = (background.width/2, background.height/2)
        centered_foreground_coords = (
            int(center_point_background[0] - foreground.width/2), 
            int(center_point_background[1] - foreground.height/2)
            )

        ret = background.convert("RGBA")
        ret.paste(foreground, box=centered_foreground_coords, mask=foreground)
        return ret


    background_image = all_assets[0]
    foreground_image = all_assets[1]
    
    if len(all_assets) >= 2: #only loop if list is longer than starting index.
        for img in all_assets[2:]:
            foreground_image.paste(img, (0, 0), img)

    # Overlay the foreground on each frame of the background
    frames = []
    for frame in ImageSequence.Iterator(background_image):
        fr = blend(frame, foreground_image)
        frames.append(fr)

    frames[0].save(output_filepath, save_all=True, append_images=frames[1:], 
    optimize=False, duration=40, loop=0)

def combine_with_png_background(all_assets, output_filepath):
    base_image = all_assets[0]
    
    for img in all_assets[1:]:
        base_image.paste(img, (0, 0), img)

    base_image.save(output_filepath)

def combine_layers(all_assets, path):
    if path.endswith("PNG"):
        return combine_with_png_background(all_assets, path)  
    if path.endswith("GIF"):
        return combine_with_gif_background(all_assets, path)
    
    Exception("Unsupported background format.")

def generate_img(params):
    try:
        serial_no, traits = params
        if not override and f'{serial_no}.png' in existing_images:
            print(f"Skipping image #{serial_no}")
            return

        for trt in list(traits): #HACK: Copy to remove during iteration.
            if trt.endswith("None"):
                traits.remove(trt)
            
        all_assets = open_all_assets(traits)
        
        combine_layers(all_assets, f'{output_folder}/{serial_no}.{all_assets[0].format}')

        print(f"Generated image #{serial_no}")
    except Exception as ex:
        print(f"Failed for {serial_no}, with exception: {ex}")


dnas = []
with open(dna_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        dnas.append(row)

columns = list(dnas[0].keys())
all_params = []

rootdir = os.getcwd()
existing_images = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if output_folder in subdir and file.endswith(".png"):
            existing_images.append(file)

for dna in dnas:
    traits = [f'{key}/{dna[key]}' for key in columns if key not in set(['serial', 'dna']) and dna[key]!= 'NONE']

    trait_vals = [t.split('/')[-1] for t in traits]
    all_params.append([dna['serial'], traits])

if __name__ == "__main__":
    pool = Pool()
    tic = time.perf_counter()
    pool.map(generate_img, all_params)
    pool.close()
    toc = time.perf_counter()
    print(f"Total time taken to process {len(dnas)} dnas is {toc - tic:0.4f} seconds")
