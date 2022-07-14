import numpy as np

def transform_boxes(box):
    '''
    Args: 
        box: 3D box with center [cx, cy, cz, l, w, h, yaw]
    Return: 
        box3d [8, 3]
            1 -------- 0
           /|         /|
          2 -------- 3 .
          | |        | |
          . 5 -------- 4
          |/         |/
          6 -------- 7
    '''
    
    cx, cy, cz, l, w, h = box[:6]
    x0 = cx + l/2
    y0 = cy - w/2
    z0 = cz + h/2
    
    x1 = cx + l/2
    y1 = cy + w/2
    z1 = cz + h/2
    
    x2 = cx - l/2
    y2 = cy + w/2
    z2 = cz + h/2
    
    x3 = cx - l/2
    y3 = cy - w/2
    z3 = cz + h/2
    
    x4 = cx + l/2
    y4 = cy - w/2
    z4 = cz - h/2
    
    x5 = cx + l/2
    y5 = cy + w/2
    z5 = cz - h/2
    
    x6 = cx - l/2
    y6 = cy + w/2
    z6 = cz - h/2
    
    x7 = cx - l/2
    y7 = cy - w/2
    z7 = cz - h/2
    
    corner3d = np.array([[x0, y0, z0],
                         [x1, y1, z1],
                         [x2, y2, z2],
                         [x3, y3, z3],
                         [x4, y4, z4],
                         [x5, y5, z5],
                         [x6, y6, z6],
                         [x7, y7, z7]], dtype=np.float32)
    return corner3d
    
def box3d_to_2d(box3d, axis_align_matrix, cam_pose, color_intrinsic, format='corners'):
    assert format in {'corners', 'center'}
    if format == 'center':
        box3d = transform_boxes(box3d)
    axis_align_matrix_inv = np.linalg.inv(axis_align_matrix)
    box3d = np.dot(axis_align_matrix_inv, 
                    np.concatenate([box3d, np.ones([box3d.shape[0], 1])], axis=1).T).T
    cam_pose_inv = np.linalg.inv(cam_pose)
    box3d = np.dot(cam_pose_inv, box3d.T).T
    box3d[:,0] /= box3d[:,2]
    box3d[:,1] /= box3d[:,2]
    box3d[:,2] = 1

    corners2d = np.dot(color_intrinsic, box3d.T).T[:, :2]
    return corners2d