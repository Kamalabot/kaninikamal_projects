# Hello Blender — create a cube and animate it moving along X (frame 1 -> 100)
import bpy

# --- Scene / timeline settings ---
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 100

# --- Remove default objects (optional) ---
# Comment out if you don't want deletion
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# --- Create a cube ---
bpy.ops.mesh.primitive_cube_add(size=2, location=(0.0, 0.0, 1.0))
cube = bpy.context.active_object
cube.name = "HelloCube"

# --- Keyframe - start position at frame 1 ---
scene.frame_set(1)
cube.location = (0.0, 0.0, 1.0)
cube.keyframe_insert(data_path="location", frame=1)

# --- Keyframe - end position at frame 100 ---
scene.frame_set(100)
cube.location = (10.0, 0.0, 1.0)
cube.keyframe_insert(data_path="location", frame=100)

# --- Ensure interpolation is linear for smoother consistent movement ---
# This iterates the fcurves for the object's action and sets keyframe interpolation.
if cube.animation_data and cube.animation_data.action:
    for fc in cube.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'

# --- Optional: set the active camera to view the cube if no camera exists ---
if not any(obj.type == 'CAMERA' for obj in scene.objects):
    bpy.ops.object.camera_add(location=(15.0, -15.0, 10.0), rotation=(1.1, 0.0, 0.9))
    cam = bpy.context.active_object
    scene.camera = cam

# --- Return to first frame ---
scene.frame_set(1)

print("Hello Blender: cube created and animated from frame 1 to 100.")