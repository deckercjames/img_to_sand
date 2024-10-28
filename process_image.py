
import sys
from argparse import ArgumentParser

from src.image_parsing.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.consolidate_tree import consolidate_blob_trees
from src.tree import unwrap_tree_post_order_traversal
from src.linker.layer_stratagem import get_all_layer_stratagem
from src.image_parsing.image_loader import load_image
from src.image_parsing.image_loader import enumerate_pixels
from src.linker.linker import get_linked_path
from src.path_elaboration.elaborator import elaborate_path
from src.visualizer.visual_debugger import export_path_to_image

import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s | %(levelname)-8s | %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger_root = logging.getLogger()
logger_root.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter())
logger_root.addHandler(stdout_handler)

def process_image(input_image_path, output_visualizer_path):
    
    # Load image
    logging.info("Loading image...")
    raw_pixels = load_image(input_image_path)
    
    num_rows = len(raw_pixels)
    num_cols = len(raw_pixels[0])
    
    # Cluster like colors
    logging.info("Enumerating pixels...")
    pixel_grid = enumerate_pixels(raw_pixels)

    # Extract blobs
    logging.info("Extracting blobs...")
    blob_trees = get_blob_tree_nodes_from_pixel_grid(pixel_grid)
    num_blobs = sum([tree.count_nodes() for tree in blob_trees])
    
    if num_blobs == 0:
        logging.fatal("Found 0 blobs in given image")
        return 1
    
    logging.debug("Found {} blobs".format(num_blobs))
    
    # Consolidate blob trees
    logging.info("Consolidating blob trees...")
    consolidated_blob_tree = consolidate_blob_trees(blob_trees, num_rows, num_cols)
    
    # Unwrap consolidated blob tree
    logging.info("Unwrapping consolidated blob tree..")
    blob_layers = unwrap_tree_post_order_traversal(consolidated_blob_tree)
    
    # Expand blobs to topography
    logging.info("Compiling layers...")
    layers = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=0, num_blob_buffer_itterations=0)
    logging.debug("Got {} linkable entities".format(sum([len(layer) for layer in layers])))
    
    # Link Entities
    logging.info("Linking entities...")
    linked_path = get_linked_path(layers)
    
    # Elaborate Path
    logging.info("Elaborating path...")
    elaborated_path = elaborate_path(layers, linked_path)
    
    # Write debug image
    logging.info("Writing visual path to '{}'".format(output_visualizer_path))
    export_path_to_image(elaborated_path, num_rows, num_cols, output_visualizer_path)
    
    # TODO Smooth path
    
    # TODO Remove cosecutive colinear instructions
    
    # TODO Write output
    

def main(input_args):
    parser = ArgumentParser(prog='myprogram')
    parser.add_argument('image', type=str, help='The path of the image to load')
    args = parser.parse_args(input_args)
    
    try:
        process_image(args.image, "output.png")
    except KeyboardInterrupt:
        print("")
        logging.info("Keyboard Interupt Received.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))