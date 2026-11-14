"""
Pixel-perfect software Z-buffer renderer for STL models.
Renders high quality shaded views of house.stl.
"""
import struct
import numpy as np
from PIL import Image

def render_zbuffer(stl_path, out_path, cam_pos, target, width=800, height=600, scale=10.5):
    with open(stl_path, 'rb') as f:
        f.read(80)
        count = struct.unpack('<I', f.read(4))[0]
        tris = []
        for _ in range(count):
            d = struct.unpack('<3f3f3f3fH', f.read(50))
            n = np.array(d[0:3], dtype=np.float32)
            v1 = np.array(d[3:6], dtype=np.float32)
            v2 = np.array(d[6:9], dtype=np.float32)
            v3 = np.array(d[9:12], dtype=np.float32)
            tris.append((n, v1, v2, v3))

    cam_pos = np.array(cam_pos, dtype=np.float32)
    target = np.array(target, dtype=np.float32)
    world_up = np.array([0.0, 0.0, 1.0], dtype=np.float32)

    fwd = target - cam_pos
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, world_up)
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)

    light = np.array([0.35, -0.65, 0.67], dtype=np.float32)
    light /= np.linalg.norm(light)

    img = np.full((height, width, 3), (228, 236, 244), dtype=np.uint8)
    zbuf = np.full((height, width), 1e9, dtype=np.float32)

    for n, v1, v2, v3 in tris:
        e1 = v2 - v1
        e2 = v3 - v1
        norm = np.cross(e1, e2)
        l_norm = np.linalg.norm(norm)
        if l_norm > 1e-6:
            n = norm / l_norm

        centroid = (v1 + v2 + v3) / 3.0
        to_cam = cam_pos - centroid
        # Backface culling
        if np.dot(n, to_cam) <= 0:
            continue

        # Lighting model
        diff = max(0.0, float(np.dot(n, light)))
        diff2 = max(0.0, float(np.dot(n, np.array([-0.4, 0.4, 0.3])))) * 0.25 # fill
        diff3 = max(0.0, float(np.dot(n, np.array([0.0, 0.0, 1.0])))) * 0.15 # sky
        intensity = 0.32 + 0.52 * diff + diff2 + diff3
        intensity = min(1.0, intensity)

        avg_z = centroid[2]
        avg_x = centroid[0]
        avg_y = centroid[1]

        # Is this rooftop water tank?
        is_water_tank = (7.0 <= avg_x <= 14.0 and 4.0 <= avg_y <= 11.0 and avg_z > 30.5)
        # Is this HVAC / antenna?
        is_metal_prop = (avg_z > 28.0 and not is_water_tank)
        # Is this rooftop floor?
        is_roof_deck = (25.5 <= avg_z <= 26.6 and n[2] > 0.5)
        # Is this balcony?
        is_balcony = (3.0 <= avg_x <= 16.5 and avg_y < -15.0)

        # Interior surface classification
        is_inside_vol = (abs(avg_x) <= 17.25 and abs(avg_y) <= 15.25 and 0.45 <= avg_z <= 26.2)
        is_interior_facing = (
            (avg_x <= -17.0 and n[0] > 0.3) or
            (avg_x >= 17.0 and n[0] < -0.3) or
            (avg_y <= -15.0 and n[1] > 0.3) or
            (avg_y >= 15.0 and n[1] < -0.3) or
            (abs(avg_y) <= 1.0 and 3.8 <= avg_x <= 17.4)
        )
        is_ceiling = (12.0 < avg_z < 26.3 and n[2] < -0.4 and is_inside_vol)
        is_interior_stairs = (-17.5 <= avg_x <= -11.0 and abs(avg_y) < 14.5 and 0.4 < avg_z < 26.0)
        is_interior = is_inside_vol and (is_interior_facing or is_ceiling or is_interior_stairs or (abs(avg_x) < 16.5 and abs(avg_y) < 14.5))

        if avg_z <= 0.45:
            base_col = np.array([125, 150, 115], dtype=np.float32) # surrounding grass / pad
        elif is_water_tank:
            base_col = np.array([72, 132, 148], dtype=np.float32) # industrial water tank
        elif is_metal_prop:
            base_col = np.array([85, 90, 100], dtype=np.float32) # HVAC / antenna metal
        elif is_roof_deck:
            base_col = np.array([130, 132, 138], dtype=np.float32) # rooftop gravel / concrete
        elif is_balcony:
            base_col = np.array([170, 174, 180], dtype=np.float32) # balcony concrete
        elif is_interior:
            if is_ceiling:
                base_col = np.array([55, 38, 26], dtype=np.float32) # dark rustic timber ceiling
            elif is_interior_stairs:
                if n[2] > 0.4:
                    base_col = np.array([135, 90, 50], dtype=np.float32) # polished oak tread
                else:
                    base_col = np.array([58, 62, 68], dtype=np.float32) # gunmetal steel stringer
            elif (avg_z <= 4.8) or (14.0 < avg_z <= 17.5):
                base_col = np.array([75, 45, 28], dtype=np.float32) # rich dark walnut wainscot
            elif (4.8 < avg_z <= 5.1) or (17.5 < avg_z <= 17.8):
                base_col = np.array([45, 26, 16], dtype=np.float32) # carved moulding trim
            elif abs(avg_y) <= 1.0:
                base_col = np.array([65, 80, 98], dtype=np.float32) # tactical slate partition wall
            else:
                base_col = np.array([198, 158, 112], dtype=np.float32) # warm caramel / amber sand plaster
        elif avg_z <= 1.3:
            base_col = np.array([110, 115, 125], dtype=np.float32) # bunker foundation plinth
        elif abs(n[2]) < 0.2 and (13.4 <= avg_z <= 14.4 or 25.3 <= avg_z <= 26.2):
            base_col = np.array([140, 145, 155], dtype=np.float32) # architectural belt courses
        else:
            base_col = np.array([220, 215, 202], dtype=np.float32) # tactical plaster / stucco siding

        col = np.clip(base_col * intensity, 0, 255).astype(np.uint8)

        # Project vertices
        pts2d = []
        zs = []
        for v in [v1, v2, v3]:
            d = v - cam_pos
            xc = np.dot(d, right)
            yc = np.dot(d, up)
            zc = np.dot(d, fwd)
            sx = width / 2.0 + xc * scale
            sy = height / 2.0 - yc * scale
            pts2d.append([sx, sy])
            zs.append(zc)

        pts2d = np.array(pts2d, dtype=np.float32)
        zs = np.array(zs, dtype=np.float32)

        min_x = max(0, int(np.floor(pts2d[:, 0].min())))
        max_x = min(width - 1, int(np.ceil(pts2d[:, 0].max())))
        min_y = max(0, int(np.floor(pts2d[:, 1].min())))
        max_y = min(height - 1, int(np.ceil(pts2d[:, 1].max())))

        if min_x > max_x or min_y > max_y:
            continue

        x0, y0 = pts2d[0]; x1, y1 = pts2d[1]; x2, y2 = pts2d[2]
        det = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
        if abs(det) < 1e-5:
            continue

        xs = np.arange(min_x, max_x + 1, dtype=np.float32)
        ys = np.arange(min_y, max_y + 1, dtype=np.float32)[:, None]

        e0 = (xs - x0) * (y1 - y0) - (ys - y0) * (x1 - x0)
        e1 = (xs - x1) * (y2 - y1) - (ys - y1) * (x2 - x1)
        e2 = (xs - x2) * (y0 - y2) - (ys - y2) * (x0 - x2)

        if det > 0:
            mask = (e0 <= 0) & (e1 <= 0) & (e2 <= 0)
        else:
            mask = (e0 >= 0) & (e1 >= 0) & (e2 >= 0)

        if not np.any(mask):
            continue

        inv_det = 1.0 / det
        w2 = -e0 * inv_det
        w0 = -e1 * inv_det
        w1 = -e2 * inv_det
        z_interp = w0 * zs[0] + w1 * zs[1] + w2 * zs[2]

        z_patch = zbuf[min_y:max_y+1, min_x:max_x+1]
        update = mask & (z_interp < z_patch)
        z_patch[update] = z_interp[update]
        
        img_patch = img[min_y:max_y+1, min_x:max_x+1]
        img_patch[update] = col

    Image.fromarray(img).save(out_path)
    print(f"Rendered {out_path} ({width}x{height})")


if __name__ == '__main__':
    render_zbuffer('house.stl', 'house_front_iso.png', cam_pos=[-55, -75, 45], target=[0, -6, 20])
    render_zbuffer('house.stl', 'house_rear_iso.png', cam_pos=[65, 75, 45], target=[0, 4, 20])
