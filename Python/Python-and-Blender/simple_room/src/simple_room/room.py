bl_info = {
    "name": "SimpleRoom",
    "author": "100i",
    "version": (0, 1),
    "blender": (2, 78),
    "location": "View3D > Add > Mesh",
}

import bpy
from mathutils import *
from math import *
from bpy.props import *

def align_matrix(context):
    loc = Matrix.Translation(context.scene.cursor_location)
    obj_align = context.user_preferences.edit.object_align
    if (context.space_data.type == 'VIEW_3D' and obj_align == 'VIEW'):
        rot = context.space_data.region_3d.view_matrix.rotation.part().\
                invert().resize4x4()

def position_camera(
    camera_translate=(0.0, 0.0, 0.0),
    camera_rotation=(0.0, 0.0, 0.0),
    fov=50.0):

    pi = 3.14159265

    scene = bpy.data.scenes["Scene"]

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

    # Set camera FOV in degrees
    scene.camera.data.angle = fov * (pi/180.0)

    scene.camera.rotation_mode = 'XYZ'

    scene.camera.rotation_euler[0] = camera_rotation[0]*(pi/180.0)
    scene.camera.rotation_euler[1] = camera_rotation[1]*(pi/180.0)
    scene.camera.rotation_euler[2] = camera_rotation[2]*(pi/180.0)

    scene.camera.location.x = camera_translate[0]
    scene.camera.location.y = camera_translate[1]
    scene.camera.location.z = camera_translate[2]

def create_mesh_object(context, verts, edges, faces, name, edit, align_matrix):
    scene = context.scene
    scene.render.engine = 'CYCLES'

    obj_act = scene.objects.active

    bpy.ops.object.select_all()
    bpy.ops.object.delete()

    if edit and not obj_act:
        return None

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, edges, faces)
    mesh.update()

    bpy.ops.object.select_all(action='DESELECT')

    position_camera((.70,1.4,.35),(-98,-181,345))
    add_lighting()


def add_wall(
        object_name='Plane',
        object_group='Room', 
        rotation_degree=0,
        axis_of_rotation='X',
        subdivision_level=5):

    # Create the plane
    bpy.ops.mesh.primitive_plane_add(
        radius         = 1,
        enter_editmode = False,
        location       = (0,0,0),
        rotation       = (0,0,0))

    # Reference object
    ob = bpy.context.active_object

    # Name object
    ob.name = object_name

    # Add new a group
    bpy.ops.object.group_add()

    # Set group name
    bpy.data.groups["Group"].name = object_group

    # Material
    mat = bpy.data.materials.get("basic")

    # If the material is not found, create it
    if mat is None:
        mat = bpy.data.materials.new(name="basic")
        mat.use_nodes = True
        node_diffuse = mat.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
        node_diffuse.inputs[0].default_value = (1,1,1,1)
        node_diffuse.inputs[1].default_value = 2.0
        node_diffuse.location = 0,0

        node_output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        node_output.location = 400,0

        mat.node_tree.links.new(node_diffuse.outputs[0], node_output.inputs[0])

    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)

    bpy.ops.object.modifier_add(type='MULTIRES')

    # Use simple subdivision type
    ob.modifiers["Multires"].subdivision_type = 'SIMPLE'

    # Subdivide
    for i in range(0, subdivision_level):
        bpy.ops.object.multires_subdivide(modifier="Multires")

    # Apply modifier
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Multires")

    # Stage Floor
    rot_mat = Matrix.Rotation(radians(rotation_degree), 4, axis_of_rotation)

    # Get quaternions
    orig_loc, orig_rot, orig_scale = ob.matrix_world.decompose()

    orig_loc_mat = Matrix.Translation(orig_loc)
    orig_rot_mat = orig_rot.to_matrix().to_4x4()
    orig_scale_mat =\
        Matrix.Scale(orig_scale[0],4,(1,0,0)) *\
        Matrix.Scale(orig_scale[1],4,(0,1,0)) *\
        Matrix.Scale(orig_scale[2],4,(0,0,1))

    ob.matrix_world = orig_loc_mat * rot_mat * orig_rot_mat * orig_scale_mat

def add_lighting():
    bpy.ops.object.lamp_add(type="HEMI")
    bpy.ops.transform.translate(value=(0,0,1.5))

def add_table():
    bpy.ops.mesh.primitive_cube_add()

    ob = bpy.context.object

    ob.scale = (.290,.15,.1)
    bpy.ops.transform.translate(value=(.5,.39,.1))

def add_room(width, height, length):
    # TODO: remove verts and faces
    verts = []
    faces = []

    add_wall("Wall")
    add_wall("Wall", "Room", 90, 'Y')
    add_wall("Wall", "Room", 90, 'X')

    add_table()

    return verts, faces

class AddRoom(bpy.types.Operator):
    bl_idname = "mesh.primitive_room_add"
    bl_label = "Add Room"
    bl_description = "Create a room."
    bl_options = {'REGISTER', 'UNDO'}

    edit = BoolProperty(name="",
            description="",
            default=False,
            options={'HIDDEN'})

    width = FloatProperty(name="Width",
            description="Width of room",
            min=0.0,
            max=100.0,
            default=5.0)

    height = FloatProperty(name="Height",
            description="Height of room",
            min=0.0,
            max=100.0,
            default=5.0)

    length = FloatProperty(name="Length",
            description="Length of room",
            min=0.0,
            max=100.0,
            default=5.0)

    def execute(self, context):
        verts, faces = add_room(
            self.width,
            self.height,
            self.length)

        obj = create_mesh_object(context, verts, [], faces, 'Room', self.edit,
            self.align_matrix)

        return {'FINISHED'}

    def invoke(self, context, event):
        self.align_matrix = align_matrix(context)
        self.execute(context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(AddRoom.bl_idname, text='SimpleRoom', icon='PLUGIN')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_remove(menu_func)

if __name__ == "__main__":
    register()
