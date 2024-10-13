
from src.linker.linker import PathItem
from src.linker.linkable_entity.linkable_entity_blob import LinkableEntityBlob
from src.linker.linkable_entity.linkable_entity_line import LinkableEntityLine
from src.path_elaboration.elaborator_blob import elaborate_blob
from src.path_elaboration.elaborator_line import elaborate_line
import heapq


def elaborate_border(num_rows, num_cols, entry_point, exit_point):
    
    # Check input
    entry_r, entry_c = entry_point
    exit_r, exit_c = exit_point
    if (entry_r != 0 and entry_r != num_rows) and (entry_c != 0 and entry_c != num_cols):
        raise Exception("Entry point not on edge")
    if (exit_r != 0 and exit_r != num_rows) and (exit_c != 0 and exit_c != num_cols):
        raise Exception("Exit point not on edge")
    
    # If they are on the same edge, no intermediate poisnts are necessary
    if entry_r == exit_r or entry_c == exit_c:
        return []
    
    open_list = []
    heapq.heappush(open_list, (0, (entry_point, [])))
    
    visited = set()
    
    while len(open_list) > 0:
        
        cost, (position, path) = heapq.heappop(open_list)
        
        if position in visited:
            continue
        
        if position == exit_point:
            return path[:-1]
        
        visited.add(position)
        
        pos_r, pos_c = position
        
        for child_r, child_c in ((0,0), (0,num_cols), (num_rows,0), (num_rows,num_cols), exit_point):
            if pos_r != child_r and pos_c != child_c:
                continue
            step_cost = abs(child_r - pos_r) + abs(child_c - pos_c)
            child_pos = (child_r, child_c)
            new_path = path + [child_pos]
            heapq.heappush(open_list, (cost+step_cost, (child_pos, new_path)))
    
    raise Exception("Failed to elaborate border. Table dims {}x{}. Entry {}, Exit {}".format(num_rows, num_cols, entry_point, exit_point))
        
        



def elaborate_path(layers, path_items: PathItem):
    
    num_rows = len(layers[0][0].get_entity_grid_mask())
    num_cols = len(layers[0][0].get_entity_grid_mask()[0])
    
    elaborated_path = []
    
    for i, path_item in enumerate(path_items):
        # Add the link between the entities
        elaborate_path.extend(path_item.entity_linkage_points)
        
        # Add the entity
        next_entity_ref = path_item.next_entity_ref
        enitty_entry_point = path_item.entity_linkage_points[-1]
        entity_exit_point = path_items[i+1].entity_linkage_points[0] if i + 1 < len(path_items) else None
        
        # Border
        if next_entity_ref.entity_idx is None:
            elaborated_path.extend(elaborate_border(num_rows, num_cols, enitty_entry_point, entity_exit_point))
            continue
        
        entity = layers[next_entity_ref.layer_idx][next_entity_ref.entity_idx]
        if type(entity) == LinkableEntityBlob:
            elaborated_path.extend(elaborate_blob(enitty_entry_point, entity_exit_point))
        elif type(entity) == LinkableEntityLine:
            elaborated_path.extend(elaborate_line(enitty_entry_point, entity_exit_point))
        else:
            raise Exception("Unknown entity type")