
from PIL import Image, ImageDraw


def export_path_to_image(path, num_rows, num_cols, output_file_path):
    
    img = Image.new("RGB", (num_cols+1, num_rows+1))
    
    # Transpose all path points
    path = [(c,r) for r,c in path]
    
    img_draw = ImageDraw.Draw(img)   
    img_draw.line(path, fill="yellow", width = 0)
    
    img.save(output_file_path)
