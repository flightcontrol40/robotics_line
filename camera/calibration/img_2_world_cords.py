import json

import cv2
import numpy as np

# 1) Camera intrinsics (from prior calibration)
K = np.array(
    [
        [4950.661092496948, 0.0, 633.6073466485544],
        [0.0, 4864.514616285357, 515.3418045850099],
        [0.0, 0.0, 1.0],
    ],
    dtype=np.float64,
)

dist_coeffs = [
    [
      -1.932871109561859,
      69.05190357769888,
      0.04656007696684483,
      0.03833592116042833,
      -136.49641732540258
    ]
]

data = None
with open("point_data.json", "r") as fd:
    data = json.load(fd)

# img_pts: Nx2 array of (u,v)  
# world_pts: Nx2 array of (x,y) in robot frame at z=z0
img_pts = np.array([
    data["image_cords"]
], dtype=np.float64)

world_pts = np.array([
    data["robot_cords"]
], dtype=np.float64)

#  -- 2. Compute homography from world→image
#    H: maps homogeneous (x,y,1) → λ(u,v,1)
H, status = cv2.findHomography(world_pts, img_pts, method=0)  # 0=regular LLS

#  -- 3. Invert H so we can go image→world
H_inv = np.linalg.inv(H)

def pixel_to_world(u, v, z0):
    """
    Map an image pixel (u,v) to world (x,y,z0) on the table plane.
    """
    uv1 = np.array([u, v, 1.0], dtype=np.float64)
    xyw = H_inv.dot(uv1)
    xyw /= xyw[2]                # de‑homogenize
    x, y = xyw[0], xyw[1]
    return x, y, z0

#  -- 4. Test on a new detection
u_det, v_det = 612, 312
x_pick, y_pick, z_pick = pixel_to_world(u_det, v_det, z0=0.02)
print(f"Pick at robot coords: x={x_pick:.3f}, y={y_pick:.3f}, z={z_pick:.3f}")