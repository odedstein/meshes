import sys, os
import numpy as np
import gpytoolbox as gpy

table = ""
table += "| Mesh | Image | Vertices | Faces | Components | Boundary | Manifold |\n"
newline = "| --- | --- | --- | --- | --- | --- | --- |\n"
table += newline

objects_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'objects')
objects_url = "https://github.com/odedstein/meshes/tree/master/objects"
objects_raw_url = "https://raw.githubusercontent.com/odedstein/meshes/master/objects"
all_objects = [d for d in os.listdir(objects_dir) if os.path.isdir(os.path.join(objects_dir,d))]
all_objects.sort()

for obj in all_objects:
    # Account for meshes not named like their directories.
    if obj=='human':
        obj_name = 'human_neutral'
    else:
        obj_name = obj
    table += f"| [{obj}]({objects_url}/{obj}) "
    table += f"| ![{obj}]({objects_raw_url}/{obj}/{obj_name}.png) "

    obj_dir = os.path.join(objects_dir, obj)
    mesh = os.path.join(obj_dir, f"{obj_name}.obj")
    V,F = gpy.read_mesh(mesh)
    table += f"| {V.shape[0]} "
    table += f"| {F.shape[0]} "

    C,CF = gpy.connected_components(F, return_face_indices=True)
    n_components = np.max(C)+1
    table += f"| {n_components} "

    boundary = False
    for component in range(n_components):
        FC = F[CF==component,:]
        b = gpy.boundary_loops(FC)
        if len(b)>0:
            boundary = True
            break
    table += f"| {'Yes' if boundary else 'No'} "

    E,nI = gpy.edges(F, return_nonmanifold_indices=True)
    table += f"| {'Yes' if nI.size==0 else 'No'} "

    table += "|\n"

print(table)
