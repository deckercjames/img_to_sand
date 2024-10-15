
import sys
from argparse import ArgumentParser

from src.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.consolidate_tree import consolidate_blob_trees
from src.tree import unwrap_tree_post_order_traversal
from src.linker.layer_stratagem import get_all_layer_stratagem
from src.linker.linker import LinkerProblem
from src.image_loader import load_image
from src.image_loader import enumerate_pixels
from src.linker.linker import get_linked_path
from src.path_elaboration.elaborator import elaborate_path
from src.visual_debugger import export_path_to_image

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def process_image(image_path):
    
    # Load imagee
    raw_pixels = load_image(image_path)
    logging.info("Image loaded.")
    
    num_rows = len(raw_pixels)
    num_cols = len(raw_pixels[0])
    
    # Cluster like colors
    pixel_grid = enumerate_pixels(raw_pixels)
    logging.info("Enumerated pixels.")
    
    # Extract blobs
    blob_trees = get_blob_tree_nodes_from_pixel_grid(pixel_grid)
    logging.info("Extracted blobs.")
    
    # Consolidate blob trees
    consolidated_blob_tree = consolidate_blob_trees(blob_trees, num_rows, num_cols)
    logging.info("Consolidated blob trees.")
    
    # Unwrap consolidated blob tree
    blob_layers = unwrap_tree_post_order_traversal(consolidated_blob_tree)
    logging.info("Unwrapped blob tree.")
    
    # Expand blobs to topography
    layers = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=0, num_blob_buffer_itterations=0, gateway_point_spacing=1)
    logging.info("Compiled layers.")
    
    # Link Entities
    logging.info("Linking entities...")
    linked_path = get_linked_path(layers)
    logging.info("Entities linked.")
    
    # Elaborate Path
    elaborated_path = elaborate_path(layers, linked_path)
    logging.info("Path elaborated.")
    
    # Write debug image
    export_path_to_image(elaborated_path, num_rows, num_cols, "test_output.png")
    
    # TODO Smooth path
    
    # TODO Remove cosecutive colinear instructions
    
    # TODO Write output
    

def main(input_args):
    parser = ArgumentParser(prog='myprogram')
    parser.add_argument('image', type=str, help='The path of the image to load')
    args = parser.parse_args(input_args)
    
    try:
        process_image(args.image)
    except KeyboardInterrupt:
        print("")
        logging.info("Keyboard Interupt Received")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))