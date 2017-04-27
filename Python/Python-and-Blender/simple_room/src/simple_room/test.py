bl_info = {
    "name": "Spindle",
    "author": "Blender",
    "version": (0, 1),
    "blender": (2, 78),
    "location": "View3D > Add > Mesh",
    "description": "Add Sindle Object.",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extension:2.5/Py/"\
        "Scripts/Add_Mesh/",
    "tracker_url": "",
    "category": "Add Mesh"
}

import bpy
from mathutils import *
from math import *
from bpy.props import *

def align_matrix(context):
    loc = Matrix.Translation(context.scene.cursor_location)

    obj_align = context.user_preferences.edit.object_align

    if(context.space_data.type == 'VIEW_3D' and obj_align == 'VIEW'):
        rot = context.space_data.region_3d.view_matrix.rotation.part().invert().resize4x4()
    else:
        rot = Matrix()

    align_matrix = loc * rot

    return align_matrix

def create_mesh_object(context, verts, edges, faces, name, edit, align_matrix):
    scene = context.scene
    obj_act = scene.objects.active

    if edit and not obj_act:
        return None

    mesh = bpy.data.meshes.new(name)

    mesh.from_pydata(verts, edges, faces)

    mesh.update()

    bpy.ops.object.select_all(action='DESELECT')

    if edit:
        ob_new = obj_act
        ob_new.select = True

        if obj_act.mode == 'OBJECT':
            old_mesh = ob_new.data
            ob_new.data = None

            old_mesh.user_clear()

            if (old_mesh.users == 0):
                bpy.data.meshes.remove(old_mesh)

            ob_new.data = mesh

    else:
        ob_new = bpy.data.objects.new(name, mesh)

        scene.objects.link(ob_new)
        ob_new.select = True

        ob_new.matrix_world = align_matrix

    if obj_act and obj_act.mode == 'EDIT':
        if not edit:
            bpy.ops.object.mode_set(mode='OBJECT')

            obj_act.select = True

            scene.update()

            bpy.ops.object.join()

            bpy.ops.object.mode_set(mode='EDIT')

            ob_new = obj_act
    else:
        scene.objects.active = ob_new

    return ob_new

def createFaces(vertIdx1, vertIdx2, closed=False, flipped=False):
    faces = []
    if not vertIdx1 or not vertIdx2:
        return None

    if len(vertIdx1) < 2 and len(vertIdx2) < 2:
        return None

    fan = False
    if (len(vertIdx1) != len(vertIdx2)):
        if (len(vertIdx1) == 1 and len(vertIdx2) > 1):
            fan = True
        else:
            return None

    total = len(vertIdx2)

    if closed:
        if flipped:
            face = [
                    vertIdx1[0],
                    vertIdx2[0],
                    vertIdx2[total - 1]]
            if not fan:
                face.append(vertIdx1[total - 1])
            faces.append(face)

        else:
            face = [vertIdx2[0], vertIdx1[0]]
            if not fan:
                face.append(vertIdx1[total - 1])
            face.append(vertIdx2[total - 1])
            faces.append(face)


    for num in range(total - 1):
        if flipped:
            if fan:
                face = [vertIdx2[num], vertIdx1[0], vertIdx2[num + 1]]
            else:
                face = [vertIdx2[num], vertIdx1[num], vertIdx1[num + 1],
                    vertIdx2[num + 1]]
            faces.append(face)
        else:
            if fan:
                face = [vertIdx1[0], vertIdx2[num], vertIdx2[num + 1]]
            else:
                face = [vertIdx1[num], vertIdx2[num], vertIdx2[num + 1],
                    vertIdx1[num + 1]]
            faces.append(face)

    return faces

def add_spindle(segments, radius, height, cap_height):
    verts = []
    faces = []

    tot_verts = segments * 2 + 2

    half_height = height / 2.0

    # Upper tip
    idx_upper_tip = len(verts)
    verts.append(Vector((0.0, 0.0, half_height + cap_height)))

    # Lower tip
    idx_lower_tip = len(verts)
    verts.append(Vector((0.0, 0.0, -half_height - cap_height)))

    upper_edgeloop = []
    lower_edgeloop = []

    for index in range(segments):
        mtx = Matrix.Rotation(2.0 * pi * float(index) / segments, 3, 'Z')

        idx_up = len(verts)

        upper_edgeloop.append(idx_up)

        if height > 0:
            idx_low = len(verts)
            lower_edgeloop.append(idx_low)
            verts.append(Vector((radius, 0.0, -half_height)) * mtx)

    tip_up_faces = createFaces([idx_upper_tip], lower_edgeloop, closed=True,
            flipped=True)

    faces.extend(tip_up_faces)

    if height > 0:
        cyl_faces = createFaces(lower_edgeloop, upper_edgeloop, closed=True)
        faces.extend(cyl_faces)

    else:
        tip_low_faces = createFaces([idx_lower_tip], upper_edgeloop,
            closed=True)
        faces.extend(tip_low_faces)

    return verts, faces

class AddSpindle(bpy.types.Operator):
    bl_idname = "mesh.primitive_spindle_add"
    bl_label = "Add Spindle"
    bl_description = "Create a spindle mesh."
    bl_options = {'REGISTER', 'UNDO'}

    edit = BoolProperty(name="",
            description="",
            default=False,
            options={'HIDDEN'})
    segments = IntProperty(name="Segments",
            description="Number of segments of the spindle",
            min=3,
            max=512,
            default=32)
    radius = FloatProperty(name="Radius",
            description="Radius of the spindle",
            min=0.0,
            max=100.0,
            default=1.0)
    height = FloatProperty(name="Height",
            description="Height of spindle",
            min=0.0,
            max=100.0,
            default=1.0)
    cap_height = FloatProperty(name="Cap Height",
            description="Cap height of spindle",
            min=9999.0,
            max=9999.0,
            default=0.5)
    align_matrix = Matrix()

    def execute(self, context):
        verts, faces = add_spindle(
            self.segments,
            self.radius,
            self.height,
            self.cap_height)

        obj = create_mesh_object(context, verts, [], faces, "Spindle",
            self.edit, self.align_matrix)

        return {'FINISHED'}

    def invoke(self, context, event):
        self.align_matrix = align_matrix(context)
        self.execute(context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(AddSpindle.bl_idname, text="Spindle", icon='PLUGIN')

def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_mesh_remove(menu_func)

if __name__ == "__main__":
    print (bpy.data.objects[:])
    register()
