########################################################################
#           Author Vs6993    _Veeresh_SM_                              #
#           date September 2022                                        #
########################################################################


"""
This script generated 3D objects with different texture using the Blender
provided input : 3D Object with segmented parts like body, stem , leaf etc
         input : Texture images for specific objext's body segment
"""

import bpy
import os

SAVE_PATH = r"D:\\Blender\\Generated_3D_MODELS"
Root = r"D:\\Blender\\vegitables_modles"

source = r"source"
texture = r"textures"

body_texture = r"body_texture"
leaf_texture = r"leaf_texture"
stem_texture = r"stem_texture"


""" storing the objects in the list"""
object_list = []
ctx = {}


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
    
    """importing the object"""
def import_object(object_root_path):
    x=[os.path.join(object_root_path,file) for file in os.listdir(object_root_path) if file.endswith('.obj')]
    bpy.ops.import_scene.obj(filepath=x[0])
    print("importing object :", x[0])
     


def join_and_save(folder,body_image,leaf_image ="",stem_image="",):            
        
            for obj in object_list:
                if "body" in obj.name or "stem" in obj.name or "leaf" in obj.name:
                    obj.select_set(True)
            if bpy.ops.object.join() != {'FINISHED'}:
                print("Error -------> not able to join the object")
            
            body_image  = body_image.split('.')[0]         
            if  leaf_image:
                leaf_image = leaf_image.split('.')[0]
            
            if  stem_image:
                stem_image = stem_image.split('.')[0]
        
            active_obj = bpy.context.view_layer.objects.active
            print("active Object Name ---> ", active_obj.name)
            folder = active_obj.name = folder + "_"+ body_image+ "_" + leaf_image+ "_" + stem_image
            print("folder --->",folder)
            
            os.makedirs(SAVE_PATH+"\\"+folder)
            bpy.ops.export_scene.obj(filepath=SAVE_PATH + "\\"+ folder +"\\"+active_obj.name +".obj")
        
            object_list.clear()  
            
            print("<  Saved the object -------------------------------->")
    
def Delete_the_object():
    object_list = [obj for obj in bpy.data.objects if "Camera" not in obj.name]
    print("object_list ---- >", object_list)
    
    for obj in object_list:
        if ("Camera" not in obj.name):
            obj.select_set(True)
    
    bpy.ops.object.delete()
    print("Deleted the object ---->")
                    

def apply_Image_texture(root_path):
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
        
    
#def Generate_models():

dirs = [] #saving the directory structure

for filename in os.listdir(Root):
    f = os.path.join(Root, filename)
    if not os.path.isfile(f):
        dirs.append(f)
print("Directores: ", dirs)

#main for loop
for i in dirs:
    
    print("i ->>>>>>",i)
    folder = i.split('\\')[-1]

    object_path = os.path.join(i,source)
    texture_path = os.path.join(i,texture)
    print("objectPath -->",object_path)
    print("TexturePath -->",texture_path)
    
    import_object(object_path)          
    object_list = [ obj for obj in bpy.data.objects if "Camera" not in obj.name ]
    
    
    body_texture_path = os.path.join(texture_path,body_texture)
    leaf_texture_path = os.path.join(texture_path,leaf_texture)
    stem_texture_path = os.path.join(texture_path,stem_texture)
    
    print("body_texture_path --- >",body_texture_path)
    print("leaf_texture_path --- >",leaf_texture_path)
    print("stem_texture_path --- >",stem_texture_path)
    
    body_texture_images = leaf_texture_images = stem_texture_images = []
    
    if os.path.isdir(body_texture_path):
        body_texture_images = os.listdir(body_texture_path)
    if os.path.isdir(leaf_texture_path):
        leaf_texture_images = os.listdir(leaf_texture_path)
    if os.path.isdir(stem_texture_path):
        stem_texture_images = os.listdir(stem_texture_path)
        
    print("body_texture_images --- >",body_texture_images)
    print("leaf_texture_images --- >",leaf_texture_images)
    print("stem_texture_images --- >",stem_texture_images)
            
        
    body_leaf = body_stem = False
    only_body = True
    
    for obj in object_list:
        if "leaf" in obj.name:
            body_leaf = True
        if "stem" in obj.name:
            body_stem = True
            
    Delete_the_object()
    object_list.clear()
    
    # iterate when object has all the  segments body,stem,leaf 
    if body_leaf and body_stem: #all

        for stem in stem_texture_images:
            for leaf in leaf_texture_images:
                for body in body_texture_images:
                    
                    import_object(object_path)
                    object_list = [ obj for obj in bpy.data.objects if "Camera" not in obj.name ]
                    
                    for obj in object_list:
                        if "body" in obj.name:
                            set_active_object(obj)
                            apply_Image_texture(os.path.join(body_texture_path,body))
                            deselect_active_object(obj)
                            
                        if "leaf" in obj.name:
                            set_active_object(obj)
                            apply_Image_texture(os.path.join(leaf_texture_path,leaf))
                            deselect_active_object(obj)
                            
                        if "stem" in obj.name:
                            set_active_object(obj)
                            apply_Image_texture(os.path.join(stem_texture_path,stem))
                            deselect_active_object(obj)
                            
                    #save the model
                    join_and_save(folder,body,leaf,stem)
                    Delete_the_object()
                            
    #Iterate only when object has body and leaf 
    elif body_leaf:
        
        for leaf in leaf_texture_images:
            for body in body_texture_images:
                
                import_object(object_path) 
                object_list = [ obj for obj in bpy.data.objects if "Camera" not in obj.name ]
                
                for obj in object_list:
                    if "body" in obj.name:
                            set_active_object(obj)
                            apply_Image_texture(os.path.join(body_texture_path,body))
                            deselect_active_object(obj)
                            
                    if "leaf" in obj.name:
                            set_active_object(obj)
                            apply_Image_texture(os.path.join(leaf_texture_path,leaf))
                            deselect_active_object(obj)
                #save the model
                join_and_save(folder,body,leaf)
                Delete_the_object()
        
    #Iterate only when object ahs  body and stem 
    elif body_stem:
        for stem in stem_texture_images:
            for body in body_texture_images:
                
                import_object(object_path)
                object_list = [ obj for obj in bpy.data.objects if "Camera" not in obj.name ]
                
                for obj in object_list:
                    if "body" in obj.name:
                            set_active_object(obj)
                            apply_Image_texture(os.path.join(body_texture_path,body))
                            deselect_active_object(obj)
                            
                    if "stem" in obj.name:
                            set_active_object(obj)
                            
                            apply_Image_texture(os.path.join(stem_texture_path,stem))
                            deselect_active_object(obj)
                #save the model
                join_and_save(folder,body,stem)
                Delete_the_object()
                
    #Iterate only when object has body segment
    else:
        for body in body_texture_images:
            
            import_object(object_path)
            object_list = [ obj for obj in bpy.data.objects if "Camera" not in obj.name ]
            
            for obj in object_list:
                    if "body" in obj.name:
                        set_active_object(obj)
                        
                        apply_Image_texture(os.path.join(body_texture_path,body))
                        deselect_active_object(obj)
                        print("applied texture----------->",body)
            #save the model
            join_and_save(folder,body)
            Delete_the_object()    
                        
        
print("<-----Completed Generating textured objects ---->")
    
    
#if __name__ == '__main__':
#    Generate_models()