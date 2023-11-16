import sys, os
import numpy as np
import bpy

objects_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'objects')
all_objects = [d for d in os.listdir(objects_dir) if os.path.isdir(os.path.join(objects_dir,d))]

for obj in all_objects:
    obj_dir = os.path.join(objects_dir, obj)
    meshes = [m for m in os.listdir(obj_dir) if os.path.splitext(m)[1]=='.obj']
    for mesh in meshes:
        obj_name = os.path.splitext(mesh)[0]
        mesh_path = os.path.join(obj_dir, f"{obj_name}.obj")

        bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(__file__), 'scene.blend'))
        ref_obj_name = 'obj'
        bpy.ops.object.select_all(action='DESELECT')

        # bpy.ops.import_scene.obj(filepath=mesh_path)
        bpy.ops.wm.obj_import(filepath=mesh_path)
        new_obj_name = os.path.splitext(os.path.basename(mesh_path))[0]
        new_obj = bpy.data.objects[new_obj_name];

        ref_obj = bpy.data.objects[ref_obj_name];
        ref_obj.select_set(True)
        new_obj.select_set(True)
        bpy.context.view_layer.objects.active = ref_obj
        bpy.ops.object.make_links_data(type='MATERIAL')
        bpy.context.view_layer.objects.active = new_obj
        bpy.ops.object.make_links_data(type='OBDATA')
        ref_obj.select_set(False)
        bpy.ops.object.delete()

        ref_obj.select_set(True)
        for f in ref_obj.data.polygons:
            f.use_smooth = True
        ref_obj.data.update()
        bpy.context.view_layer.objects.active = ref_obj
        bpy.ops.object.select_all( action = 'SELECT' )
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        ref_obj.location = 0. * ref_obj.location
        max_dims = max(abs(max(ref_obj.dimensions)), abs(min(ref_obj.dimensions)))
        ref_obj.dimensions = 2.5 * ref_obj.dimensions / max_dims

        bpy.context.scene.render.filepath = os.path.join(obj_dir, f"{obj_name}.png")
        bpy.ops.render.render(write_still=True)
    