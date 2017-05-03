bl_info = {
    "name": "SimplePerson",
    "author": "100i",
    "version": (0, 1),
    "blender": (2, 78),
    "location": "View3D > Add > Mesh",
}

import bpy
from mathutils import *
from math import *
from bpy.props import *

def create_person():
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=23)

class AddPerson(bpy.types.Operator):
    bl_idname = "mesh.primitive_person_add"
    bl_label = "Add Simple Person"
    bl_description = "Create a person."
    bl_options = {'REGISTER', 'UNDO'}

    height = FloatProperty(name="Height",
            description="Height of person",
            min=0.0,
            max=15.0,
            default=6.0)

    def execute(self, context):
        create_person()

        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(AddPerson.bl_idname, text='SimplePerson', icon='PLUGIN')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_remove(menu_func)

if __name__ == '__main__':
    register()
