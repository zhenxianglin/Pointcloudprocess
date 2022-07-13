import pandas as pd
import numpy as np
from pyntcloud import PyntCloud
from .utils import paint_points, cal_corner_after_rotation, eight_points, create_lines

COLOR_LIST = {'red': [255, 0, 0], 'green': [0, 255, 0], 'blue': [0, 0, 255],
         'black':[0, 0, 0], 'white': [255, 255, 255], 'aque':[0, 255, 255],
         'yellow': [255, 255, 0], 'orange': [255, 125, 0], 'grey':[125, 125, 125],
         'gray': [125, 125, 125]
}

class PointCloudScene:
    def __init__(self, points):
        self.points = points
        self.scene = None
        self.boxes = []
 
    def plot(self, initial_point_size=0.02):
        assert self.scene is not None
        self.scene.plot(initial_point_size=initial_point_size, backend="pythreejs", polylines=self.boxes)
    
    def init_scene(self, point_color='green', with_rgb=False):
        assert self.points is not None
        color = COLOR_LIST[point_color]
        if with_rgb:
            pc_plot = self.points[:, :3]
            color = self.points[:, 3:6]
        else:
            pc_plot = self.points[:, :3]
        pc_plot = pd.DataFrame(paint_points(pc_plot, color=color), columns=['x', 'y', 'z', 'red', 'green', 'blue'])
        self.scene = PyntCloud(pc_plot)

    def add_boxes_by_center(self, boxes, color='blue'):
        """
        boxes: List[List] [cx, cy, cz, depth, width, height, rotation]
        """
        pc_corners = []
        for bbox in boxes:
            center = bbox[:3]
            size = bbox[3:6]
            try:
                rotation = bbox[6]
            except:
                rotation = 0
            eight_corners = eight_points(center, size, rotation)
            pc_corners.append(eight_corners)
        for corners in pc_corners:
            if not isinstance(corners, list):
                corners = corners.tolist()
            self.boxes.extend(create_lines(corners=corners, color=color))
    
    def add_boxes_by_corners(self, boxes, color='yellow'):
        for corners in boxes:
            if not isinstance(corners, list):
                corners = corners.tolist()
            self.boxes.extend(create_lines(corners=corners, color=color))
    
    def draw_line(self, pointA, pointB, color='red'):
        """
        pointA: list [x, y, z]
        pointB: list [x, y, z]
        "color": "0xFFFFFF" or "red". Default: red
        """
        if isinstance(pointA, np.ndarray):
            pointA = pointA.tolist()
        if isinstance(pointB, np.ndarray):
            pointB = pointB.tolist()
        self.boxes.extend([{"color": color, "vertices": [pointA, pointB]}])
    
    def draw_axis(self, length=5):
        self.boxes.extend([
            {"color": 'red', "vertices": [[0, 0, 0], [length, 0, 0]]},
            {"color": 'blue', "vertices": [[0, 0, 0], [0, length, 0]]},
            {"color": 'green', "vertices": [[0, 0, 0], [0, 0, length]]}
            ])


def create_scene(points, color='green', with_rgb=False, with_axis=True):
    """
    Args:
        points: np.ndarray [N, 3+C]
        color: points color, default: 'green'
        with_rgb: scene include color. If with_rgb is True, parameter 'color' can be ignored.
        with_axis: create 3D-axis
    Return: PointCloudScene
    """
    if not isinstance(points, np.ndarray):
        raise TypeError("points should be np.ndarray")
    if with_rgb:
        assert points.shape[1] >= 6, f"If RGB points, points dimension should be at least 6 (x, y, z, r, g, b)."
    scene = PointCloudScene(points)
    scene.init_scene(color, with_rgb)
    if with_axis:
        scene.draw_axis()
    return scene

def append_boxes(scene, boxes, format='corners', color='red'):
    """
    Args:
        scene: PointCloudScene
        boxes: List or np.ndarray.
        format: 'corners' or 'center'. If corners, the format of each box is [8, 3] (eight corners). 
                If center, the format is [7, ] (cx, cy, cz, l, w, h, yaw). Default: 'corners'
        color: box color. Default: red
    """
    assert format in {'corners', 'center'}, f"format can only be corners or center"
    assert isinstance(boxes, [list, np.ndarray])
    if format == 'corners':
        scene.add_boxes_by_corners(boxes, color)
    else:
        scene.add_boxes_by_center(boxes, color)
    return scene

def plot(scene, initial_point_size=0.02):
    scene.plot(initial_point_size)

def show_scene(points, color='green', with_rgb=False, with_axis=True, initial_point_size=0.02):
    if not isinstance(points, np.ndarray):
        raise TypeError("points should be np.ndarray")
    if with_rgb:
        assert points.shape[1] >= 6, f"If RGB points, points dimension should be at least 6 (x, y, z, r, g, b)."
    scene = create_scene(points, color, with_rgb, with_axis)
    scene.plot(initial_point_size)

def show_scene_by_boxes(points, boxes, points_color='green', with_rgb=False, box_color='red', format='corners', with_axis=False, initial_point_size=0.02):
    if not isinstance(points, np.ndarray):
        raise TypeError("points should be np.ndarray")
    if with_rgb:
        assert points.shape[1] >= 6, f"If RGB points, points dimension should be at least 6 (x, y, z, r, g, b)."
    scene = create_scene(points, points_color, with_rgb, with_axis)
    scene = append_boxes(scene, boxes, format, box_color)
    scene.plot(initial_point_size)

def draw_line(scene, pointA, pointB, color='red'):
    """
        pointA: list [x, y, z]
        pointB: list [x, y, z]
        "color": "0xFFFFFF" or "red". Default: red
    """
    scene.draw_line(pointA, pointB, color)
    return scene

def draw_axis(scene, length=5):
    scene.draw_axis(length)
    return scene
