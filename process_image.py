
import sys

from src.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.consolidate_tree import consolidate_blob_trees
from src.tree import unwrap_tree_post_order_traversal
from src.linker.layer_stratagem import get_all_layer_stratagem
from src.linker.linker import LinkerProblem

def process_image(image_path):
    
    # TODO open image
    
    # TODO cluster like colors
    pixel_grid = None
    
    # Extract blobs
    blob_trees = get_blob_tree_nodes_from_pixel_grid(pixel_grid)
    
    # Consolidate blob trees
    consolidated_blob_tree = consolidate_blob_trees(blob_trees)
    
    # Unwrap consolidated blob tree
    blob_layers = unwrap_tree_post_order_traversal(consolidated_blob_tree)
    
    # Expand blobs to topography
    # TODO
    
    # TODO Search path
    
    layers = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=10, num_blob_buffer_itterations=5)
    
    problem = LinkerProblem(
        layers
    )
    
    # TODO Smooth path
    
    # TODO Remove cosecutive colinear instructions
    
    # TODO Write output
    

def main():
    pass

if __name__ == "__main__":
    sys.exit(main())