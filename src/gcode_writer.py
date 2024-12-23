


def write_path_to_gcode(path, num_rows, output_file):
    
    buf = ""
    
    # write path
    for r,c in path:
        
        buf += "G01 X{} Y{}\n".format(c, (num_rows - r))
    
    try:
        with open(output_file, "w") as output_fp:
            output_fp.write(buf)
    except OSError:
        print("FAILED")