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

