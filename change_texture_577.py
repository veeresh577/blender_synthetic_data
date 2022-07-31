import bpy
import os


OBECT_ROOT_PATH = "D:\\Blender\\3D_MODELS\\apple_seperated.obj" 
SAVE_OBJECTS = ""
APPLE_body = "D:\\Blender\\apple\\body\\download(2).jpg"

IMAGE_ROOT_FOLDER = "D:\\Blender\\apple\\body\\"
STEM_IMAGE_PATH = "D:\\Blender\\apple\\stem\\Apple_stem.jpg"

#imported_object = bpy.ops.import_scene.obj(filepath=OBECT_ROOT_PATH)

""" storing the objects in the list"""
object_list = []


"""set active object"""
def set_active_object( object):
    #bpy.data.collections[Collection_name].objects[object_name].select_set(True)
    #bpy.data.objects[object].select_set(True)
    bpy.context.view_layer.objects.active = object 
    bpy.data.objects[object.name].select_set(True)
    #bpy.context.scene.objects.active = object
    
    
"""deselect the active object"""   
def deselect_active_object( object):
    #bpy.data.collections[Collection_name].objects[object_name].select_set(False)
    bpy.data.objects[object.name].select_set(False)
    
    """import the objetc"""
def import_object(path):
    imported_object = bpy.ops.import_scene.obj(filepath=path)
     
    """Delete all objects """
def Delete_all_objects():
    bpy.ops.object.select_all()
    bpy.ops.object.delete()
    
    
 
    
#iterate over objects in collections
#for obj in bpy.data.objects:
#    if obj.name != "Camera":
#        object_list.append(obj)
        

def apply_Image_texture(root_path,obj):
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
            
            active_obj = bpy.context.view_layer.objects.active
            #active_obj = obj
            new_mat = bpy.data.materials.new("my_material")
            active_obj.data.materials.append(new_mat)

            new_mat.use_nodes = True
            nodes = new_mat.node_tree.nodes
            nodes.clear()
            create_nodes(new_mat,nodes,root_path)

    except Exception as e:
        print(e)
        
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
    
    node_tex.location = -400,0
    node_output = nodes.new(type='ShaderNodeOutputMaterial')   
    node_output.location = 400,0
    links = new_mat.node_tree.links
    link = links.new(node_tex.outputs["Color"], node_principled.inputs["Base Color"])
    link = links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
        
    

Stem_object = "stem_Manzana.002"
Body_object = "body_Manzana.001"

"""Iterate our images in local folder"""

"""set stem as active object and apply texture"""
#set_active_object("Collection",Stem_object)
#apply_Image_texture(STEM_IMAGE_PATH)
#deselect_active_object("Collection",Stem_object)

#set_active_object("Collection",Body_object)
#for image in os.listdir(IMAGE_ROOT_FOLDER):
#    image = IMAGE_ROOT_FOLDER + image
#    apply_Image_texture(image)
    

for image in os.listdir(IMAGE_ROOT_FOLDER):
   
    
    import_object(OBECT_ROOT_PATH)
    
    #global object_list
    object_list = [ obj for obj in bpy.data.objects if obj.name != "Camera" ]
            
    image_name = image.split('.')[0]
    print("---------------image_name :",image_name)
    image = IMAGE_ROOT_FOLDER + image

    for obj in object_list:
        
        if "stem" in obj.name:
            set_active_object(obj)
            apply_Image_texture(STEM_IMAGE_PATH,obj)
            deselect_active_object(obj)
           
        
        if "body" in obj.name:
          
                set_active_object(obj)
                apply_Image_texture(image,obj)
                
                #bpy.ops.object.select_all()
                #bpy.ops.object.join(object_list)
                
                #bpy.ops.wm.save_as_mainfile(object_list, filepath= r"D:\Blender\apple\objects\apple_" + image_name +".obj")
    
    ctx = bpy.context.copy()
    ctx['selected_objects'] = object_list
    bpy.ops.object.join(ctx)
    bpy.ops.export_scene.obj(filepath=r"D:\Blender\apple\objects\apple_" + image_name +".obj")
    object_list.clear()        
    Delete_all_objects()
    
    
