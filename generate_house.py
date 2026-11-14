"""
Generator for PUBG-style Tactical Squad Building Model in STL format (house.stl).
Features:
- Completely flush, wide-open ground entrance (14m wide) for effortless walk-in/run-in
- Hollow 2-story interior with tactical rooms and cover
- Left-wall interior concrete staircase to 2nd Floor
- 2nd Floor sniper window nest with chest-height cover sill
- 2nd Floor tactical exterior cantilever balcony with metal railings
- Interior staircase continuing from 2nd floor up to the flat rooftop
- Walkable flat tactical rooftop with perimeter cover parapets and sniper embrasures
- Rooftop stairwell doghouse with open walk-out doorway
- Rooftop cylindrical water tower, industrial HVAC chiller units, and radio antenna
"""
import struct
import numpy as np

class STLBuilder:
    def __init__(self):
        self.triangles = []

    def add_triangle(self, v1, v2, v3, normal=None):
        v1 = np.array(v1, dtype=np.float32)
        v2 = np.array(v2, dtype=np.float32)
        v3 = np.array(v3, dtype=np.float32)
        
        if normal is None:
            e1 = v2 - v1
            e2 = v3 - v1
            n = np.cross(e1, e2)
            norm = np.linalg.norm(n)
            if norm > 1e-9:
                normal = n / norm
            else:
                normal = np.array([0.0, 0.0, 1.0], dtype=np.float32)
        else:
            normal = np.array(normal, dtype=np.float32)
            norm = np.linalg.norm(normal)
            if norm > 1e-9:
                normal = normal / norm
            else:
                normal = np.array([0.0, 0.0, 1.0], dtype=np.float32)
                
        self.triangles.append((normal, v1, v2, v3))

    def add_quad(self, v0, v1, v2, v3, normal=None):
        """Adds a quad v0->v1->v2->v3 (CCW when viewed from exterior)."""
        self.add_triangle(v0, v1, v2, normal)
        self.add_triangle(v0, v2, v3, normal)

    def add_box(self, x0, x1, y0, y1, z0, z1):
        """Adds an axis-aligned solid box [x0,x1] x [y0,y1] x [z0,z1]."""
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        z0, z1 = min(z0, z1), max(z0, z1)

        # Front (-Y)
        self.add_quad((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), (0, -1, 0))
        # Back (+Y)
        self.add_quad((x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (0, 1, 0))
        # Left (-X)
        self.add_quad((x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (-1, 0, 0))
        # Right (+X)
        self.add_quad((x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1), (1, 0, 0))
        # Top (+Z)
        self.add_quad((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1), (0, 0, 1))
        # Bottom (-Z)
        self.add_quad((x0, y1, z0), (x1, y1, z0), (x1, y0, z0), (x0, y0, z0), (0, 0, -1))

    def add_cylinder(self, cx, cy, z0, z1, radius, n_segs=16):
        """Adds a vertical cylinder with caps."""
        angles = np.linspace(0, 2*np.pi, n_segs, endpoint=False)
        cos_a = np.cos(angles)
        sin_a = np.sin(angles)
        
        bc = (cx, cy, z0)
        tc = (cx, cy, z1)
        
        for i in range(n_segs):
            j = (i + 1) % n_segs
            b_i = (cx + radius * cos_a[i], cy + radius * sin_a[i], z0)
            b_j = (cx + radius * cos_a[j], cy + radius * sin_a[j], z0)
            t_i = (cx + radius * cos_a[i], cy + radius * sin_a[i], z1)
            t_j = (cx + radius * cos_a[j], cy + radius * sin_a[j], z1)
            
            self.add_triangle(bc, b_j, b_i, (0, 0, -1))
            self.add_triangle(tc, t_i, t_j, (0, 0, 1))
            self.add_quad(b_i, b_j, t_j, t_i)

    def export_stl(self, filename, header_str=b"PUBG Tactical Squad Building - Antigravity"):
        header = header_str[:80].ljust(80, b'\x00')
        count = len(self.triangles)
        with open(filename, 'wb') as f:
            f.write(header)
            f.write(struct.pack('<I', count))
            for normal, v1, v2, v3 in self.triangles:
                data = struct.pack('<3f3f3f3fH',
                                   normal[0], normal[1], normal[2],
                                   v1[0], v1[1], v1[2],
                                   v2[0], v2[1], v2[2],
                                   v3[0], v3[1], v3[2],
                                   0)
                f.write(data)
        print(f"Exported {count} triangles to '{filename}'.")


def build_house():
    stl = STLBuilder()

    # ==========================================
    # 1. GROUND LEVEL FLUSH ENTRANCES & FLOOR SLAB
    # ==========================================
    # Exterior surrounding base pad (flush ground level Z in [0.0, 0.4])
    stl.add_box(-26.0, 26.0, -24.0, 24.0, 0.0, 0.4)
    # Ground Floor Interior Walkable Floor Slab (flush height 0.4m)
    stl.add_box(-17.2, 17.2, -15.2, 15.2, 0.0, 0.4)
    # Extra wide front and back entrance aprons (smooth ground glide)
    stl.add_box(-12.0, 12.0, -25.0, -15.0, 0.0, 0.4)
    stl.add_box(-12.0, 12.0, 15.0, 25.0, 0.0, 0.4)

    # Perimeter base plinth band
    stl.add_box(-18.4, 18.4, -16.4, 16.4, 0.0, 1.2)

    # ==========================================
    # 2. GROUND FLOOR WALLS & GRAND ENTRANCES (100% WALK-IN)
    # ==========================================
    # FRONT WALL (Y: [-16.0, -15.2], Z: [0.4, 14.0])
    # Massive 14m wide open entrance: X in [-7.0, 7.0]
    stl.add_box(-18.0, -7.0, -16.0, -15.2, 0.4, 14.0)
    stl.add_box(7.0, 18.0, -16.0, -15.2, 0.4, 14.0)
    stl.add_box(-7.0, 7.0, -16.0, -15.2, 12.0, 14.0) # Header beam
    # Heavy concrete entrance pillars
    stl.add_box(-7.8, -6.8, -16.6, -15.0, 0.4, 14.2)
    stl.add_box(6.8, 7.8, -16.6, -15.0, 0.4, 14.2)
    # Entrance canopy overhang
    stl.add_box(-8.5, 8.5, -18.2, -15.2, 11.6, 12.2)

    # BACK WALL (Y: [15.2, 16.0], Z: [0.4, 14.0])
    # 14m wide open back entrance: X in [-7.0, 7.0]
    stl.add_box(-18.0, -7.0, 15.2, 16.0, 0.4, 14.0)
    stl.add_box(7.0, 18.0, 15.2, 16.0, 0.4, 14.0)
    stl.add_box(-7.0, 7.0, 15.2, 16.0, 12.0, 14.0) # Header beam
    stl.add_box(-7.8, -6.8, 15.0, 16.6, 0.4, 14.2)
    stl.add_box(6.8, 7.8, 15.0, 16.6, 0.4, 14.2)
    stl.add_box(-8.5, 8.5, 15.2, 18.2, 11.6, 12.2)

    # SIDE WALLS (Ground Floor)
    # Left Wall (X: [-18.0, -17.2])
    stl.add_box(-18.0, -17.2, -16.0, 16.0, 0.4, 14.0)
    # Right Wall (X: [17.2, 18.0])
    stl.add_box(17.2, 18.0, -16.0, 16.0, 0.4, 14.0)

    # Ground floor tactical partition wall on right side
    stl.add_box(4.0, 17.2, -0.4, 0.4, 0.4, 14.0)

    # Horizontal architectural belt course separating Floor 1 & Floor 2
    stl.add_box(-18.5, 18.5, -16.5, 16.5, 13.5, 14.3)

    # ==========================================
    # 3. INTERIOR STAIRCASE OPENING (GROUND TO 1ST FLOOR)
    # ==========================================
    # Situated along Left Wall: X in [-17.2, -10.0], Y in [-10.0, 6.0]
    # The stairwell shaft is kept 100% open in the STL (no solid concrete steps
    # to avoid Z-fighting with Three.js high-detail illuminated timber stairs,
    # and no solid guardrail wall at X = -10.0 to ensure full panoramic visibility
    # from the 1st floor hall through modern open see-through balustrades).

    # ==========================================
    # 4. FIRST / SECOND FLOOR WALKABLE SLAB & BALCONY
    # ==========================================
    # 1st Floor interior slab (Z: [13.6, 14.2]):
    # Main continuous slab covering center and right side
    stl.add_box(-10.0, 17.2, -15.2, 15.2, 13.6, 14.2)
    # Spacious rear landing behind the top of the stairs: X in [-17.2, -10.0], Y in [6.0, 15.2] (Three.js Z: [-15.2, -6.0], meeting step 16 seamlessly)
    stl.add_box(-17.2, -10.0, 6.0, 15.2, 13.6, 14.2)

    # TACTICAL EXTERIOR BALCONY (Front Right, classic PUBG squad house feature!)
    # Balcony cantilever slab: X in [3.0, 16.0], Y in [-21.0, -15.2], Z in [13.6, 14.2]
    stl.add_box(3.0, 16.0, -21.0, -15.2, 13.6, 14.2)
    # Balcony support brackets underneath
    for bx in [4.0, 9.5, 15.0]:
        stl.add_box(bx - 0.4, bx + 0.4, -20.5, -15.2, 10.5, 13.6)
    # Balcony perimeter parapet & railing (Z: [14.2, 16.8])
    stl.add_box(3.0, 16.0, -21.0, -20.4, 14.2, 16.8) # Front rail
    stl.add_box(3.0, 3.6, -20.4, -15.2, 14.2, 16.8)  # Left rail
    stl.add_box(15.4, 16.0, -20.4, -15.2, 14.2, 16.8) # Right rail

    # ==========================================
    # 5. SECOND FLOOR WALLS & TACTICAL SNIPER WINDOW
    # ==========================================
    # FRONT WALL (Y: [-16.0, -15.2], Z: [14.2, 26.0])
    # Left front wall section
    stl.add_box(-18.0, -3.2, -16.0, -15.2, 14.2, 26.0)

    # PRIMARY TACTICAL SNIPER WINDOW (Center: X in [-3.2, 3.2])
    # Lower chest-high cover sill: Z in [14.2, 16.5]
    stl.add_box(-3.2, 3.2, -16.0, -15.2, 14.2, 16.5)
    # Lintel above sniper window: Z in [23.5, 26.0]
    stl.add_box(-3.2, 3.2, -16.0, -15.2, 23.5, 26.0)
    # Concrete trim moulding framing the sniper window
    stl.add_box(-3.5, -3.1, -16.3, -15.0, 16.2, 23.8) # Left trim
    stl.add_box(3.1, 3.5, -16.3, -15.0, 16.2, 23.8)  # Right trim
    stl.add_box(-3.5, 3.5, -16.4, -15.0, 16.1, 16.6)  # Sill ledge
    stl.add_box(-3.5, 3.5, -16.4, -15.0, 23.4, 23.9)  # Top trim

    # Wall section between center window and balcony door: X in [3.2, 7.0]
    stl.add_box(3.2, 7.0, -16.0, -15.2, 14.2, 26.0)

    # Walkout Balcony Doorway: X in [7.0, 11.5], open from Z = 14.2 to 22.0
    stl.add_box(7.0, 11.5, -16.0, -15.2, 22.0, 26.0) # Header above door

    # Right front wall section: X in [11.5, 18.0]
    stl.add_box(11.5, 18.0, -16.0, -15.2, 14.2, 26.0)

    # BACK WALL (Y: [15.2, 16.0], Z: [14.2, 26.0])
    # Solid wall with 2 rear sniper windows
    stl.add_box(-18.0, -13.0, 15.2, 16.0, 14.2, 26.0)
    # Left rear window opening: X in [-13.0, -8.0], Z in [17.5, 22.5]
    stl.add_box(-13.0, -8.0, 15.2, 16.0, 14.2, 17.5)
    stl.add_box(-13.0, -8.0, 15.2, 16.0, 22.5, 26.0)
    # Center-right wall
    stl.add_box(-8.0, 8.0, 15.2, 16.0, 14.2, 26.0)
    # Right rear window opening: X in [8.0, 13.0], Z in [17.5, 22.5]
    stl.add_box(8.0, 13.0, 15.2, 16.0, 14.2, 17.5)
    stl.add_box(8.0, 13.0, 15.2, 16.0, 22.5, 26.0)
    stl.add_box(13.0, 18.0, 15.2, 16.0, 14.2, 26.0)

    # SIDE WALLS (2nd Floor)
    stl.add_box(-18.0, -17.2, -16.0, 16.0, 14.2, 26.0) # Left wall
    stl.add_box(17.2, 18.0, -16.0, 16.0, 14.2, 26.0)  # Right wall

    # Belt course below roof parapet
    stl.add_box(-18.5, 18.5, -16.5, 16.5, 25.4, 26.2)

    # ==========================================
    # 6. REAR CORNER VERTICAL ACCESS LADDER TO ROOFTOP
    # ==========================================
    # Vertical steel ladder in rear doghouse corner (X: [-16.2, -15.4], Y: [13.2, 14.0])
    # from 1st floor landing (Z = 14.2) up to rooftop doghouse (Z = 26.4)
    stl.add_box(-16.2, -15.4, 13.2, 14.0, 14.2, 26.4)

    # ==========================================
    # 7. TACTICAL FLAT ROOFTOP WITH PARAPETS & PROPS
    # ==========================================
    # Flat Walkable Rooftop Slab (Z: [25.8, 26.4])
    # Full coverage slab with hatch at rear doghouse
    stl.add_box(-18.0, 18.0, -16.0, 16.0, 25.8, 26.4)

    # Rooftop Stairwell Bulkhead / Doghouse (Z: [26.4, 30.2])
    # Enclosing X in [-18.0, -10.5], Y in [2.0, 16.0]
    stl.add_box(-18.0, -17.2, 2.0, 16.0, 26.4, 30.2) # Left wall
    stl.add_box(-18.0, -10.5, 15.2, 16.0, 26.4, 30.2) # Back wall
    stl.add_box(-18.0, -10.5, 2.0, 2.8, 26.4, 30.2)   # Front wall
    # Inner wall facing roof with open doorway: X in [-11.3, -10.5]
    # Doorway: Y in [4.0, 9.0], open from Z = 26.4 to 29.5
    stl.add_box(-11.3, -10.5, 2.0, 4.0, 26.4, 30.2)
    stl.add_box(-11.3, -10.5, 9.0, 16.0, 26.4, 30.2)
    stl.add_box(-11.3, -10.5, 4.0, 9.0, 29.5, 30.2) # Door header
    # Doghouse roof slab
    stl.add_box(-18.2, -10.3, 1.8, 16.2, 30.0, 30.6)

    # PERIMETER PARAPET WALLS WITH SNIPER COVER (Z: [26.4, 28.8])
    # Front parapet (Y: [-16.0, -15.2])
    # Broken into tactical embrasures/crenels (crenelated parapet for peeking!)
    for px in [-17.5, -10.5, -3.5, 3.5, 10.5]:
        stl.add_box(px, px + 5.0, -16.0, -15.2, 26.4, 28.8)
    # Solid low base parapet everywhere along front edge
    stl.add_box(-18.0, 18.0, -16.0, -15.2, 26.4, 27.2)

    # Back parapet (Y: [15.2, 16.0])
    for px in [-10.5, -3.5, 3.5, 10.5]:
        stl.add_box(px, px + 5.0, 15.2, 16.0, 26.4, 28.8)
    stl.add_box(-18.0, 18.0, 15.2, 16.0, 26.4, 27.2)

    # Right parapet (X: [17.2, 18.0])
    for py in [-14.0, -7.0, 0.0, 7.0]:
        stl.add_box(17.2, 18.0, py, py + 5.0, 26.4, 28.8)
    stl.add_box(17.2, 18.0, -16.0, 16.0, 26.4, 27.2)

    # Left parapet (X: [-18.0, -17.2]) - south section in front of doghouse
    stl.add_box(-18.0, -17.2, -16.0, 2.0, 26.4, 28.8)

    # Parapet coping / cap rails
    stl.add_box(-18.2, 18.2, -16.2, -15.0, 28.6, 29.0)
    stl.add_box(-18.2, 18.2, 15.0, 16.2, 28.6, 29.0)
    stl.add_box(17.0, 18.2, -16.2, 16.2, 28.6, 29.0)

    # ==========================================
    # 8. ICONIC PUBG ROOFTOP PROPS (Water Tower & HVAC)
    # ==========================================
    # Cylindrical Water Storage Tank on Sturdy Trestle Stand
    for lx in [8.0, 13.0]:
        for ly in [5.0, 10.0]:
            stl.add_box(lx - 0.25, lx + 0.25, ly - 0.25, ly + 0.25, 26.4, 31.0)
    stl.add_box(7.5, 13.5, 4.5, 10.5, 30.8, 31.3)
    stl.add_cylinder(10.5, 7.5, 31.3, 36.5, 2.5, n_segs=16)
    stl.add_cylinder(10.5, 7.5, 36.5, 37.8, 1.4, n_segs=12)

    # Dual Industrial HVAC Air Ventilation Units
    stl.add_box(2.0, 6.5, -8.0, -3.0, 26.4, 28.8)
    stl.add_box(2.2, 6.3, -7.8, -3.2, 28.8, 29.2)
    stl.add_cylinder(4.25, -5.5, 29.2, 29.8, 1.2, n_segs=12)

    # Communications / Radio Antenna Mast
    stl.add_box(-11.2, -10.6, 3.0, 3.6, 30.0, 42.0)
    stl.add_box(-12.5, -9.3, 3.1, 3.5, 38.0, 38.4)
    stl.add_box(-12.0, -9.8, 3.1, 3.5, 40.5, 40.9)

    return stl


if __name__ == '__main__':
    import base64
    print("Generating PUBG-style Tactical Squad Building with flush entrance...")
    builder = build_house()
    builder.export_stl('house.stl')
    with open('house.stl', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    with open('house_model_data.js', 'w', encoding='utf-8') as f:
        f.write(f'const HOUSE_STL_BASE64 = "{b64}";\n')
    print("Updated house_model_data.js successfully.")
