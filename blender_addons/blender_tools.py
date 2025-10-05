bl_info = {
    "name": "Blender Tools",
    "blender": (4, 5, 0),
    "category": "Object",
    "author": "KaniniKamal",
    "version": (1, 0),
    "description": "Intro programming + visualization exercises for Blender"
}

import bpy
import math


# --------------------------------------------------
# Utility Helper
# --------------------------------------------------
class BlenderHelper:
    @staticmethod
    def clear_scene():
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

    @staticmethod
    def make_cube(size=1, location=(0,0,0)):
        bpy.ops.mesh.primitive_cube_add(size=size, location=location)
        return bpy.context.active_object

    @staticmethod
    def make_sphere(radius=1, location=(0,0,0)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
        return bpy.context.active_object


# --------------------------------------------------
# Exercises
# --------------------------------------------------

class SpiralGenerator:
    def run(self):
        BlenderHelper.clear_scene()
        for i in range(50):
            angle = i * 0.2 * math.pi
            x = 0.1 * i * math.cos(angle)
            y = 0.1 * i * math.sin(angle)
            z = i * 0.1
            BlenderHelper.make_cube(size=0.5, location=(x,y,z))


class ParametricSurface:
    def run(self, size=20):
        BlenderHelper.clear_scene()
        verts, faces = [], []

        for x in range(size):
            for y in range(size):
                z = math.sin(x * 0.3) * math.cos(y * 0.3)
                verts.append((x, y, z))

        for x in range(size-1):
            for y in range(size-1):
                i = x * size + y
                faces.append([i, i+1, i+size+1, i+size])

        mesh = bpy.data.meshes.new("SineMesh")
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        obj = bpy.data.objects.new("SineSurface", mesh)
        bpy.context.collection.objects.link(obj)


class BouncingBall:
    def run(self):
        BlenderHelper.clear_scene()
        ball = BlenderHelper.make_sphere(radius=1, location=(0,0,5))
        frames = [1, 20, 40, 60]
        positions = [(0,0,5), (0,0,1), (0,0,5), (0,0,1)]

        for f, pos in zip(frames, positions):
            ball.location = pos
            ball.keyframe_insert(data_path="location", frame=f)

        for fcurve in ball.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BEZIER'


class Graph3D:
    def run(self, func=lambda x: math.sin(x), x_min=-10, x_max=10, step=0.2):
        BlenderHelper.clear_scene()
        points = []
        for i in range(int((x_max-x_min)/step)+1):
            x = x_min + i * step
            y = func(x)
            z = 0
            points.append((x, y, z))

        curve_data = bpy.data.curves.new("GraphCurve", type='CURVE')
        curve_data.dimensions = '3D'
        polyline = curve_data.splines.new('POLY')
        polyline.points.add(len(points)-1)

        for i, coord in enumerate(points):
            x, y, z = coord
            polyline.points[i].co = (x, y, z, 1)

        curve_obj = bpy.data.objects.new("FunctionGraph", curve_data)
        bpy.context.collection.objects.link(curve_obj)


# --------------------------------------------------
# Operators
# --------------------------------------------------

class OBJECT_OT_spiral(bpy.types.Operator):
    bl_idname = "object.spiral_generator"
    bl_label = "Generate Spiral"

    def execute(self, context):
        SpiralGenerator().run()
        return {'FINISHED'}


class OBJECT_OT_surface(bpy.types.Operator):
    bl_idname = "object.surface_generator"
    bl_label = "Generate Parametric Surface"

    def execute(self, context):
        ParametricSurface().run()
        return {'FINISHED'}


class OBJECT_OT_bounce(bpy.types.Operator):
    bl_idname = "object.bouncing_ball"
    bl_label = "Animate Bouncing Ball"

    def execute(self, context):
        BouncingBall().run()
        return {'FINISHED'}


class OBJECT_OT_graph(bpy.types.Operator):
    bl_idname = "object.graph_generator"
    bl_label = "Generate Sine Graph"

    def execute(self, context):
        Graph3D().run()
        return {'FINISHED'}


# --------------------------------------------------
# UI Panel
# --------------------------------------------------

class VIEW3D_PT_hello_blender(bpy.types.Panel):
    bl_label = "Hello Blender Tools"
    bl_idname = "VIEW3D_PT_hello_blender"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Hello Blender"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Visualization Exercises:")
        layout.operator("object.spiral_generator")
        layout.operator("object.surface_generator")
        layout.operator("object.bouncing_ball")
        layout.operator("object.graph_generator")


# --------------------------------------------------
# Register
# --------------------------------------------------

classes = [
    OBJECT_OT_spiral,
    OBJECT_OT_surface,
    OBJECT_OT_bounce,
    OBJECT_OT_graph,
    VIEW3D_PT_hello_blender
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
