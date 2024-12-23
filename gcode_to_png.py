
import sys
import re
from argparse import ArgumentParser
from PIL import Image, ImageDraw

def export_path_to_image(tool_path, num_rows, num_cols, output_file_path):
    
    img = Image.new("RGB", (num_cols+1, num_rows+1))
    
    img_draw = ImageDraw.Draw(img)   
    img_draw.line(tool_path, fill="#baa800", width = 0)
    
    try:
        img.save(output_file_path)
    except OSError as err:
        print("Failed to write visualizer output '{}'. {}".format(output_file_path, err))


def import_gcode(input_path):
    
    try:
        with open(input_path) as fp:
            lines = fp.readlines()
    except OSError as err:
        print("Failed to read input file {}: {}".format(input_path, err))
        
    g01_regex = re.compile(r'^G0*1$')
        
    tool_path = []
    for line in lines:
        
        # discard trailing comment
        command = line.split(";")[0].strip()
        
        if command == "":
            continue
        
        arguments = command.split()
        
        if not g01_regex.match(arguments[0]):
            print("Encounterd non-G01 command, skipping: {}".format(line))
            continue
        
        for arg in arguments[1:]:
            if arg[0] == 'X':
                x = int(float(arg[1:]))
            elif arg[0] == 'Y':
                y = int(float(arg[1:]))
            else:
                print("Encountered unknown arg: {}".format(arg))
            
        tool_path.append((x,y))
    
    return tool_path


def main(input_args):
    parser = ArgumentParser(prog='gcode_to_png')
    parser.add_argument('gcode_input', type=str, help='Input path to a gcode file')
    parser.add_argument('-o', '--output', type=str, default="output.png", help='Output path for png')
    parser.add_argument('table_width', type=int, help='The table width in millimeters')
    parser.add_argument('table_height', type=int, help='The table height in millimeters')
    args = parser.parse_args(input_args)
    
    tool_path = import_gcode(args.gcode_input)
    
    export_path_to_image(tool_path, args.table_height, args.table_width, args.output)
    

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))