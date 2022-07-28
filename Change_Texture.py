import bpy
import os

IMAGE_ROOT_FOLDER = "D:\\Blender\\texture_imges\\"

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
            active_obj = bpy.context.active_object
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


#Iterate our images in local folder
for image in os.listdir(IMAGE_ROOT_FOLDER):
    image = IMAGE_ROOT_FOLDER + image
    apply_Image_texture(image)
