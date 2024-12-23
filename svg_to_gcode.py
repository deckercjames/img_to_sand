
import sys
from typing import List, Tuple
import xml.etree.ElementTree as ET
from argparse import ArgumentParser

def pop_left_point(beizer: str) -> Tuple[str, Tuple[int, int]]:
    
    i: int = 0
    
    while i < len(beizer) and not any([beizer[i] == c for c in ['C', 'L', ' ']]):
        i += 1
        pass
    
    print("poped: {}".format(beizer[:i]))
    
    coords = beizer[:i].split(',')
    x = float(coords[0])
    y = float(coords[1])
    
    if i < len(beizer) and beizer[i] == ' ':
        i += 1
    
    return  beizer[i:], (x,y)

def expand_beizer(p0, p1, p2, p3, steps=1000) -> List[Tuple[int, int]]:
    
    tool_path = []
    
    p0x, p0y = p0
    p1x, p1y = p1
    p2x, p2y = p2
    p3x, p3y = p3
    
    t = 0
    
    while t < 1:
        a = (1 - t) ** 3
        b = 3 * ((1 - t) ** 2) * t
        c = 3 * (1 - t) * (t ** 2)
        d = t ** 3
        
        x = (a * p0x) + (b * p1x) + (c * p2x) + (d * p3x)
        y = (a * p0y) + (b * p1y) + (c * p2y) + (d * p3y)
        
        tool_path.append((x, y))
        
        t += (1 / steps)
    
    return tool_path
    
def svg_beizer_to_tool_path(beizer: str) -> List[Tuple[int, int]]:
    tool_path = []
    
    if beizer[0] != 'M':
        print("Error.  Is this a beizer")
        return
    beizer = beizer[1:]
    
    beizer, initial_point = pop_left_point(beizer)
    tool_path.append(initial_point)
    
    while len(beizer) > 0:
        
        line_type = beizer[0]
        beizer = beizer[1:]
        
        if line_type == 'L':
            beizer, next_point = pop_left_point(beizer)
            tool_path.append(next_point)
        elif line_type == 'C':
            p0 = tool_path[-1]
            beizer, p1 = pop_left_point(beizer)
            beizer, p2 = pop_left_point(beizer)
            beizer, p3 = pop_left_point(beizer)
            curve_segment_tool_path = expand_beizer(p0, p1, p2, p3)
            tool_path.extend(curve_segment_tool_path)
        else:
            print("Error: got unknown segment id '{}'".format(line_type))
    
    return tool_path

def load_beizer(file_path: str) -> str:
    # create element tree object 
    tree = ET.parse(file_path) 
  
    # get root element 
    root = tree.getroot()
    
    for item in root.findall(".//{*}path"):
        
        print(item)
        
        return item.attrib['d']


def write_tool_path_to_file(tool_path, output_filepath: str):
    
    try:
        with open(output_filepath, 'w') as fp:
            for x, y in tool_path:
                fp.write("G01 X{} Y{}\n".format(x, y))
    except OSError as err:
        print("Failed to write to file '{}': {}".format(output_filepath, err))


def  main(input_args):
    parser = ArgumentParser(prog='svg_to_gcode')
    parser.add_argument('svg_input', type=str, help='Input path to an SVG file')
    parser.add_argument('gcode_output', type=str, help='Output path to an SVG file')
    args = parser.parse_args(input_args)
    
    beizer = load_beizer(args.svg_input)
    
    tool_path = svg_beizer_to_tool_path(beizer)
    
    write_tool_path_to_file(tool_path, args.gcode_output)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))