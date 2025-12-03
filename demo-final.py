import open3d as o3d
import numpy as np
from PIL import Image
DOWNSAMPLE_FACTOR = 4
MAX_POINTS = 50000

def create_color_palette_with_octree(image_path, max_depth):
    img = Image.open(image_path).convert('RGB') # load image and convert to rgb
    img_np = np.array(img) / 255.0 # normalize for open3d color representation

    if DOWNSAMPLE_FACTOR > 1:   # downsize the image to decrease runtime
        new_size = (img.width // DOWNSAMPLE_FACTOR, img.height // DOWNSAMPLE_FACTOR)
        img = img.resize(new_size, Image.LANCZOS)

    points = img_np.reshape(-1, 3)  # reshape pixels into an nx3 array --- n points & 3 color channels

    if len(points) > MAX_POINTS:    # downsizeimage to decrease runtime
        indices = np.random.choice(len(points), MAX_POINTS, replace = False)
        points = points[indices]

    pcd = o3d.geometry.PointCloud() # create a point cloud
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(points) # use colors as points for octree

    octree = o3d.geometry.Octree(max_depth=max_depth)   # build an octree object
    octree.convert_from_point_cloud(pcd, size_expand=0.01)  # convert from pointcloud

    # 4. Traverse the Octree and collect colors
    palette_colors = []
    
    # Define a callback function for traversal
    def collect_colors_callback(node, node_info):
        #if isinstance(node, o3d.geometry.OctreeColorLeafNode):
            # Colors are stored as float [0, 1] in Open3D
        color = np.asarray(node.color) 
        palette_colors.append(tuple(color))
        return False # Continue traversal

    leaf_nodes = []
    for point in pcd.points:
        leaf_node, node_info = octree.locate_leaf_node(point)
        if leaf_node not in leaf_nodes:
            collect_colors_callback(leaf_node, node_info)
            leaf_nodes.append(leaf_node)

    #unique_colors = list(set(palette_colors)) 
    unique_colors = []
    for color in palette_colors:    # remove duplicate colors from the list
        if color not in unique_colors:
            unique_colors.append(color)
    return unique_colors

# Usage example

if __name__ == '__main__':
    palette = create_color_palette_with_octree("applecat.JPG", max_depth=5)
    print(f"Generated palette with {len(palette)} colors:")
    color_list = []
    for color in palette:
        if color not in color_list:
            rgb_tuple = tuple(map(int, color))
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)
            print(f"RGB: {hex_color}")
            color_list.append(color)

