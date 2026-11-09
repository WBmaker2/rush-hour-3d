"""Rush Hour 3D - Blender build script (Level 01, 6x6, 참고: jvibeschool.org/3D/RushHour).
Blender > Scripting > Open this file > Run Script, or run via Blender MCP execute_blender_code."""
import bpy, math
from collections import deque

# --- 1. Clear (factory reset is avoided so Blender MCP stays connected) ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):
    bpy.data.materials.remove(m, do_unlink=True)

# --- 2. Level data: (name, row, col, length, orientation 'H'/'V', color_key) ---
LEVEL = [
    ("P", 2, 0, 2, "H", "target"),
    ("A", 2, 4, 2, "V", "blue"),
    ("B", 4, 2, 3, "H", "green"),
    ("C", 1, 2, 2, "V", "red"),
    ("D", 0, 4, 2, "H", "purple"),
    ("E", 1, 5, 2, "V", "truck"),
    ("F", 3, 5, 3, "V", "orange"),
]

# --- 3. BFS solver to verify solvable + find minimum moves ---
def solve(level):
    n = 6
    def occ(state):
        g = [["."] * n for _ in range(n)]
        for (name, r, c, L, o, _), (nr, nc) in zip(level, state):
            for k in range(L):
                rr, cc = (nr, nc + k) if o == "H" else (nr + k, nc)
                g[rr][cc] = name
        return g
    start = tuple((r, c) for _, r, c, _, _, _ in level)
    goal_target = state_end = None
    q = deque([start]); seen = {start}; parent = {start: None}; move_of = {}
    while q:
        s = q.popleft()
        g = occ(s)
        tr, tc = s[0]
        if tc + 2 >= n and all(g[tr][cc] == "." for cc in range(tc + 2, n)):
            goal_target = s
            break
        for i, (name, r, c, L, o, _) in enumerate(level):
            cr, cc = s[i]
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if o == "H" and dr != 0: continue
                if o == "V" and dc != 0: continue
                nr, nc = cr + dr, cc + dc
                cells = [(nr, nc + k) if o == "H" else (nr + k, nc) for k in range(L)]
                if any(not (0 <= rr < n and 0 <= cc2 < n) for rr, cc2 in cells): continue
                if any(g[rr][cc2] not in (".", name) for rr, cc2 in cells): continue
                ns = list(s); ns[i] = (nr, nc); ns = tuple(ns)
                if ns not in seen:
                    seen.add(ns); parent[ns] = s; move_of[ns] = (i, nr, nc); q.append(ns)
    if goal_target is None:
        print("SOLVER: no solution found"); return None
    path = []
    s = goal_target
    while parent[s] is not None:
        path.append(move_of[s]); s = parent[s]
    path.reverse()
    print(f"SOLVER: minimum moves = {len(path)}")
    return path

SOLUTION = solve(LEVEL)

# --- 4. World, materials, lights, camera ---
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("RushWorld"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.93, 0.96, 1.0, 1.0); bg.inputs[1].default_value = 1.0

def mat(name, rgb, rough=0.35, metal=0.1):
    m = bpy.data.materials.new(name); m.use_nodes = True
    bsdf = next(x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough; bsdf.inputs["Metallic"].default_value = metal
    return m

M = {
    "board": mat("BoardWhite", (0.96, 0.97, 0.99), 0.6, 0.0),
    "board_alt": mat("BoardAlt", (0.82, 0.87, 0.94), 0.6, 0.0),
    "wall": mat("WallNavy", (0.12, 0.24, 0.42), 0.5, 0.05),
    "wall_accent": mat("WallAccent", (0.15, 0.55, 0.95), 0.4, 0.05),
    "ground": mat("Ground", (0.75, 0.82, 0.90), 0.9, 0.0),
    "target": mat("PoliceYellow", (1.0, 0.78, 0.08), 0.28, 0.05),
    "target_cabin": mat("PoliceCabin", (0.08, 0.12, 0.22), 0.25, 0.1),
    "stripe": mat("PoliceStripe", (0.08, 0.12, 0.22), 0.4, 0.0),
    "tire": mat("Tire", (0.05, 0.05, 0.06), 0.9, 0.0),
    "glass": mat("Glass", (0.45, 0.75, 0.95), 0.1, 0.3),
    "red": mat("CarRed", (0.95, 0.22, 0.18), 0.3, 0.05),
    "blue": mat("CarBlue", (0.15, 0.42, 0.95), 0.3, 0.05),
    "green": mat("CarGreen", (0.15, 0.72, 0.35), 0.3, 0.05),
    "orange": mat("CarOrange", (0.98, 0.55, 0.12), 0.3, 0.05),
    "purple": mat("CarPurple", (0.55, 0.32, 0.95), 0.3, 0.05),
    "teal": mat("CarTeal", (0.05, 0.75, 0.78), 0.3, 0.05),
    "pink": mat("CarPink", (0.98, 0.45, 0.68), 0.3, 0.05),
    "truck": mat("TruckGray", (0.45, 0.52, 0.60), 0.45, 0.1),
}

sun_data = bpy.data.lights.new("Sun", "SUN"); sun_data.energy = 5.0
sun_obj = bpy.data.objects.new("Sun", sun_data)
bpy.context.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(50), 0, math.radians(35))

cam_data = bpy.data.cameras.new("CamIso")
cam_obj = bpy.data.objects.new("Camera_Isometric", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (9.5, -10.5, 9.5); cam_obj.rotation_euler = (math.radians(52), 0, math.radians(42))
bpy.context.scene.camera = cam_obj; cam_data.lens = 42; cam_data.clip_end = 100

# --- 5. Board: ground, base, 6x6 tiles, walls with exit gap on right row 2 ---
CELL = 1.0
def add_cube(name, loc, scale, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    return o

add_cube("Ground", (0, 0, -0.6), (16, 16, 0.2), M["ground"])
add_cube("BoardBase", (0, 0, -0.12), (6.6, 6.6, 0.22), M["wall"])
for r in range(6):
    for c in range(6):
        x = c - 2.5; y = 2.5 - r
        add_cube(f"Tile_{r}_{c}", (x, y, 0), (0.9, 0.9, 0.08),
                 M["board"] if (r + c) % 2 == 0 else M["board_alt"])
# walls (exit gap on +X at row 2, world y=0.5)
add_cube("Wall_N", (0, 3.55, 0.25), (7.2, 0.3, 0.5), M["wall"])
add_cube("Wall_S", (0, -3.55, 0.25), (7.2, 0.3, 0.5), M["wall"])
add_cube("Wall_W", (-3.55, 0, 0.25), (0.3, 7.2, 0.5), M["wall"])
add_cube("Wall_E_top", (3.55, 2.27, 0.25), (0.3, 2.6, 0.5), M["wall_accent"])
add_cube("Wall_E_bot", (3.55, -1.77, 0.25), (0.3, 3.6, 0.5), M["wall_accent"])
# exit road strip
add_cube("ExitRoad", (4.6, 0.5, 0.02), (2.0, 0.9, 0.06), M["target"])

def grid_to_world(r, c, L=1, o="H"):
    x = (c + (L - 1) / 2) - 2.5 if o == "H" else (c - 2.5)
    y = (2.5 - r) if o == "H" else (2.5 - (r + (L - 1) / 2))
    return (x, y, 0.42)

# --- 6. Vehicles: low-poly body + cabin + wheels, grouped per vehicle ---
vehicles = {}
for name, r, c, L, o, color_key in LEVEL:
    wx, wy, wz = grid_to_world(r, c, L, o)
    coll = bpy.data.collections.new(f"Vehicle_{name}")
    bpy.context.scene.collection.children.link(coll)
    is_truck = (L == 3)
    body_len = L - 0.12
    body_mat = M[color_key]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz))
    body = bpy.context.active_object; body.name = f"Body_{name}"
    body.scale = (body_len / 2, 0.38, 0.22) if o == "H" else (0.38, body_len / 2, 0.22)
    body.scale = (body.scale[0] * 2, body.scale[1] * 2, body.scale[2] * 2)
    body.data.materials.append(body_mat)
    for coll_list in (body.users_collection,): pass
    # cabin
    bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz + 0.28))
    cab = bpy.context.active_object; cab.name = f"Cabin_{name}"
    cab.scale = ((body_len * 0.45), 0.34, 0.2) if o == "H" else (0.34, (body_len * 0.45), 0.2)
    cab.data.materials.append(M["target_cabin"] if name == "P" else M["glass"])
    # wheels
    wpos = [(-body_len/2 + 0.22, -0.40), (body_len/2 - 0.22, -0.40), (-body_len/2 + 0.22, 0.40), (body_len/2 - 0.22, 0.40)]
    wheels = []
    for dx, dy in wpos:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.09,
              location=(wx + (dx if o == "H" else dy), wy + (dy if o == "H" else dx), wz - 0.18))
        w = bpy.context.active_object; w.name = f"Wheel_{name}"
        w.rotation_euler = (math.radians(90), 0, 0) if o == "H" else (0, math.radians(90), 0)
        w.data.materials.append(M["tire"]); wheels.append(w)
    # police stripe
    if name == "P":
        bpy.ops.mesh.primitive_cube_add(size=1, location=(wx, wy, wz + 0.02))
        s = bpy.context.active_object; s.name = "PoliceStripe"
        s.scale = (body_len * 0.9, 0.42, 0.06)
        s.data.materials.append(M["stripe"])
    # parent everything to body for easy sliding animation
    for child in list(coll.objects) + [cab] + wheels:
        pass
    w_offsets = []
    for w in wheels:
        loc = w.location
        w_offsets.append((loc[0] - wx, loc[1] - wy, loc[2] - wz))
    vehicles[name] = {"body": body, "cab": cab, "wheels": wheels, "w_offsets": w_offsets,
                      "orient": o, "length": L, "row": r, "col": c}

# --- 7. Solution playback animation (keyframe each move) ---
frame = 1
if SOLUTION:
    positions = {name: grid_to_world(r, c, L, o) for name, r, c, L, o, *_ in LEVEL}
    for name in positions:
        v = vehicles[name]
        wx, wy, wz = positions[name]
        v["body"].location = (wx, wy, wz); v["body"].keyframe_insert(data_path="location", frame=frame)
        v["cab"].location = (wx, wy, wz + 0.28); v["cab"].keyframe_insert(data_path="location", frame=frame)
        for w, off in zip(v["wheels"], v["w_offsets"]):
            w.location = (wx + off[0], wy + off[1], wz + off[2]); w.keyframe_insert(data_path="location", frame=frame)
    for idx, nr, nc in SOLUTION:
        name = LEVEL[idx][0]
        positions[name] = grid_to_world(nr, nc, LEVEL[idx][3], LEVEL[idx][4])
        v = vehicles[name]
        wx, wy, wz = positions[name]
        frame += 12
        v["body"].location = (wx, wy, wz); v["body"].keyframe_insert(data_path="location", frame=frame)
        v["cab"].location = (wx, wy, wz + 0.28); v["cab"].keyframe_insert(data_path="location", frame=frame)
        for w, off in zip(v["wheels"], v["w_offsets"]):
            w.location = (wx + off[0], wy + off[1], wz + off[2]); w.keyframe_insert(data_path="location", frame=frame)
    print(f"ANIMATION: {len(SOLUTION)} moves keyframed, end frame {frame}")

# --- 8. Title text + level info ---
def add_text(name, body, loc, size, rot=(0, 0, 0), mat_=None):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"
    ob = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = tuple(math.radians(a) for a in rot)
    if mat_: cu.materials.append(mat_)
    return ob

add_text("Title", "RUSH HOUR 3D", (0, 4.6, 0.2), 0.55, mat_=M["wall_accent"])
add_text("LevelInfo", "LEVEL 01 · 6 x 6 · Police Car -> Exit", (0, 4.0, 0.2), 0.25, mat_=M["wall"])

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = max(120, frame if SOLUTION else 120)
bpy.context.scene.frame_current = 1
print("DONE: Rush Hour 3D scene built. Save as rush-hour-3d.blend")
