import bpy
import bpycv
import cv2
from pathlib import Path
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import json

''' Debugging'''
import pdb

HEIGHT = 1280
WIDTH = 720
ROTATION_INCREMENT = 400
SAVE_PATH = r"D:\\Blender\\Mayuresh\\Rotation\\"
D_MODELS_PATH = r"D:\\Blender\\Mayuresh\\3D_MODELS\\"
file_information = {}


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def camera_view_bounds_2d(scene, cam_ob, me_ob):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            # if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return (
        round(min_x * dim_x),            # X
        round(dim_y - max_y * dim_y),    # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    )
    
    
'''Change Texture of images'''
def apply_Image_texture(root_path):
    
    print("applying Texture ------>")
    """
    This function imports the image and superimposes it onto the active abject.
    :param root_path:
    :return:
    """
    try:
        if(bpy.context.object.active_material):
            mat = bpy.context.object.active_material
            nodes = mat.node_tree.nodes 
            nodes.clear()
            create_nodes(mat,nodes,root_path)

        else:
            active_obj = bpy.context.active_object
            new_mat = bpy.data.materials.new("my_material")
            active_obj.data.materials.append(new_mat)

            new_mat.use_nodes = True
            nodes = new_mat.node_tree.nodes
            nodes.clear()
            create_nodes(new_mat,nodes,root_path)

    except Exception as e:
        print(e)
        print(bpy.context.active_object)
        pdb.set_trace()
        
    
def create_nodes(new_mat ,nodes,root_path):
    """
    Creates new  Principled Bsdf shader node,
    texture node and output node and links them
    :param new_mat:
    :param nodes:
    :param root_path:
    :return:
    """

    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = 0,0
    node_tex = nodes.new('ShaderNodeTexImage')
    
    node_tex.image = bpy.data.images.load(root_path)
    print(root_path)
    node_tex.location = -400,0
    node_output = nodes.new(type='ShaderNodeOutputMaterial')   
    node_output.location = 400,0
    links = new_mat.node_tree.links
    link = links.new(node_tex.outputs["Color"], node_principled.inputs["Base Color"])
    link = links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])

def set_active_object(obj):
    bpy.context.view_layer.objects.active = obj
    
'''Move camera rotate and save rendered images'''
def generate_obj_list(l):
    for ob in bpy.data.objects:
         if(ob.name != 'CameraLock' and ob.name != 'Camera' and ob.name != 'Light' and ob.name != 'Cube'):
            l.append(current_scene.objects[ob.name])
            print("Adding Objects from scene = ", ob.name)
        
def load_model_file(path):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f) and f.endswith('.obj'):
            print('----------'+filename+'-----------------')
            print(f)
            print('---------------------------')
            bpy.ops.import_scene.obj(filepath = f)
            file_information[filename] = path
            
     
def load_obj_file(path):
    dirs = []
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if not os.path.isfile(f):
            dirs.append(f)
    print(dirs)
    for i in range(len(dirs)):
        load_model_file(dirs[i])
        
        
def print_list(l):
    for x in range(len(l)):
        print("List Content : ", l[x])

def hide_objects_from_render(obj, hide):
    if hide:
        obj.hide_render = True
    else:
        obj.hide_render = False
        
def hide_objects_from_viewport(obj, hide):
    if hide:
        obj.hide_viewport = True
    else:
        obj.hide_viewport = False
    
def reset_rotation(obj):
    obj.rotation_euler[0] = math.radians(0)
    obj.rotation_euler[1] = math.radians(0)
    obj.rotation_euler[2] = math.radians(0)

def add_key_frames(i, obj):
    obj.keyframe_insert(data_path="location", frame=i)

def rotate_camera(obj, deg, axis):
    obj.rotation_euler[axis] = math.radians(deg)
    print("Euler Rot ", obj.rotation_euler[axis])

def set_resolution(obj):
    obj.resolution_x = HEIGHT
    obj.resolution_y = WIDTH
    
def create_json():
    fp=open('D:\\Blender\\Mayuresh\\data.json','w')
    fp.close()
    
def write_to_json(path , point):
    fp = open('D:\\Blender\\Mayuresh\\data.json','a+')
    json.dump({path: point},fp)
    fp.close()
    
    
#Rotate along Z Axis
def rotate_along_Z(obj):
    
        camera_object = bpy.data.objects['Camera']
        for deg in range(0, 360,ROTATION_INCREMENT):
            print("Current Rotation",deg)
            current_scene.render.filepath = str(output_path/"Z"/obj.name)+"_"+str(deg)
            rotate_camera(camera_lock, deg,2)
            print("Rendering to ", current_scene.render.filepath)
            
            point = camera_view_bounds_2d(current_scene, camera_object, obj)
            print("point : " , point)
            
            
            write_to_json( current_scene.render.filepath , point )
            print('Writing to json completed')
            bpy.ops.render.render(write_still=True)
            render_instace_seg(current_scene.render.filepath)
            
    
       
        
#Rotate Along X Axis
#def rotate_along_X(obj):
#    for deg in range(0, 45,ROTATION_INCREMENT):
#        print("Current Rotation",deg)
#        current_scene.render.filepath = str(output_path/"X"/obj.name)+"_"+str(deg)
#        rotate_camera(camera_lock, deg, 1)
#        print("Rendering to ", current_scene.render.filepath)
#        bpy.ops.render.render(write_still=True)
#        render_instace_seg(current_scene.render.filepath)

#Rotate Along Y Axis
#def rotate_along_Y(obj):
#    for deg in range(0, 360,ROTATION_INCREMENT):
#        print("Current Rotation",deg)
#        current_scene.render.filepath = str(output_path/"Y"/obj.name)+"_"+str(deg)
#        rotate_camera(camera_lock, deg, 0)
#        print("Rendering to ", current_scene.render.filepath)
#        bpy.ops.render.render(write_still=True)
#        render_instace_seg(current_scene.render.filepath)
        

def scale_obj_into_cube(obj):
    print("object dimension :", obj.dimensions)
    maxDimension = 1.5 * max(obj.dimensions)
    print("Dimension :",maxDimension)
    obj.dimensions = obj.dimensions/maxDimension

def hide_all_objs(l, h):
    for x in range(len(l)):
        if(l[x] != camera_lock):
            hide_objects_from_viewport(l[x], h)
            hide_objects_from_render(l[x], h)
            print("Hiding from view port - ", l[x])
            print("Hide Status = ", h)

def add_inst_id_per_mesh():
    counter = 1
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj["inst_id"] = counter
            print("Obj_Name:  ",obj.name)
            counter=counter+1
            
def render_instace_seg(file):
    add_inst_id_per_mesh()
    result = bpycv.render_data()
    cv2.imwrite(file + "_inst_.png", np.uint16(result["inst"]))
    cv2.imwrite(file + "_visual_.png", result.vis())
    plt.plot(result["inst"])
    plt.savefig(file+"_inst_visual.png")
    

    


#Object List
obj_list = []
print("Started Execution")
#Load all models
load_obj_file(D_MODELS_PATH)

#print file paths and texture models
print("file information :",file_information)

#Debug MSG to check of all obj's loaded
print_list(obj_list)

#Set up current scene var
current_scene = bpy.context.scene
camera_lock = current_scene.objects['CameraLock']
fp = current_scene.render.filepath
current_scene.render.image_settings.file_format = 'PNG'
current_scene.render.image_settings.color_mode = 'RGBA'

#Set Render Resolution
set_resolution(current_scene.render)

#Set Save Directory
output_path = Path(SAVE_PATH)

#Add camera lock as first in list
obj_list.append(camera_lock)

#Create list of all objects in scene other than Camera, Cube, Light and CameraLock.
generate_obj_list(obj_list)

#Render on transparent
current_scene.render.film_transparent = True

#Reset Rotation of OBJ
for x in range(len(obj_list)):
    if(obj_list[x] != camera_lock):
        reset_rotation(obj_list[x])


#Hide all Objects before render start
hide_all_objs(obj_list, True)  


create_json()
#Render Obj's other than camera lock one by one
for x in range(len(obj_list)):
   
        if(obj_list[x] != camera_lock):
            print("Object rendered = ",obj_list[x])
            
            #enable obj for rendering and view port
            hide_objects_from_viewport(obj_list[x], False)
            hide_objects_from_render(obj_list[x], False)
            
            #fit the object within camera lock box
            scale_obj_into_cube(obj_list[x])
            #Set Active Obj so that texture can be applied on it
            set_active_object(obj_list[x])
            
            
            #Get the path and render jpg
            for key in file_information:
                image = file_information[obj_list[x].name.split(".")[0]+'.obj']
                print('*************************')
                print(image)
                print('*************************')
                #Iterate our images in local folder
                for texture_file in os.listdir(image):
                    if texture_file.endswith('.jpg'):
                        jpg = image + '/' +texture_file
                        apply_Image_texture(jpg)
                        print('********aaaaaaaa********')
                        print(jpg)
                        print(bpy.context.scene.objects)
                        print('********aaaaaaaa********')
                #Reset Camera Lock
        #        reset_rotation(camera_lock)
                #Rotate camera along X Axis
        #        rotate_along_X(obj_list[x])
                
                #Reset Camera Lock
                reset_rotation(camera_lock)
                #Rotate camera along Z Axis
                rotate_along_Z(obj_list[x])

                #Reset Camera Lock
        #        reset_rotation(camera_lock)
                #Rotate camera along Y Axis
        #        rotate_along_Y(obj_list[x])
                
                #Reset Camera Lock
                reset_rotation(camera_lock)
                hide_all_objs(obj_list, True)
                
                
hide_all_objs(obj_list, False)