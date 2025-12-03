import open3d as o3d
import numpy as np
from PIL import Image

DOWNSAMPLE_FACTOR = 4   # constant factor to downsize image
MAX_POINTS = 50000  # constant number of max pixels/points to traverse from the image

def create_color_palette_with_octree(image_path, max_depth):
    """Takes an image path and max tree depth to create an octree and use it to develop
    a color palette based on the averages of the pixel colors within the image."""

    img = Image.open(image_path).convert('RGB') # load image and convert to rgb

    if DOWNSAMPLE_FACTOR > 1:   # downsize the image to decrease runtime
        new_size = (img.width // DOWNSAMPLE_FACTOR, img.height // DOWNSAMPLE_FACTOR)
        img = img.resize(new_size, Image.LANCZOS)

    img_np = np.array(img) / 255.0 # normalize for open3d color representation
    points = img_np.reshape(-1, 3)  # reshape pixels into an nx3 array --- n points & 3 color channels

    if len(points) > MAX_POINTS:    # downsizeimage to decrease runtime
        indices = np.random.choice(len(points), MAX_POINTS, replace = False)
        points = points[indices]

    pcd = o3d.geometry.PointCloud() # create a point cloud
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(points) # use colors as points for octree

    octree = o3d.geometry.Octree(max_depth=max_depth)   # build an octree object
    octree.convert_from_point_cloud(pcd, size_expand=0.01)  # convert from pointcloud

    palette_colors = []
    visited_nodes = set()   # creates placeholder to store visited nodes in following loop
    
    for point in points:  # loops through sampled points
        leaf_node, node_info = octree.locate_leaf_node(point)   # finds a leaf node
        node_id = id(leaf_node)  # use object id to track uniqueness
        
        if node_id not in visited_nodes:    # the point here represents the color
            palette_colors.append(tuple(point * 255))  # convert back to 0-255
            visited_nodes.add(node_id)

    unique_colors = list(dict.fromkeys(palette_colors)) # remove duplicates while preserving order

    return unique_colors



if __name__ == '__main__':
    palette = create_color_palette_with_octree("applecat.JPG", max_depth=5)
    print(f"Generated palette with {len(palette)} colors:")
    color_list = []
    for color in palette:
        if color not in color_list:
            rgb_tuple = tuple(map(int, color))  # gets rgb tuple of color
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)    # tansforms into hex code
            print(f"RGB: {hex_color}")
            color_list.append(color)

