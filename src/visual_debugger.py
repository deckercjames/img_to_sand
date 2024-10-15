
from PIL import Image, ImageDraw


def export_path_to_image(path, num_rows, num_cols, output_file_path):
    
    img = Image.new("RGB", (num_cols+1, num_rows+1))
    
    path = [(c,r) for r,c in path]
    
    img1 = ImageDraw.Draw(img)   
    img1.line(path, fill ="red", width = 0)
    
    img.save(output_file_path)
