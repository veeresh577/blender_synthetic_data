#import bpy
import os
import time


IMAGE_ROOT_FOLDER = "D:\\Blender\\texture_imges"


# mat = bpy.context.object.active_material
# nodes = mat.node_tree.nodes
# nodes.clear()
#
# node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
# node_principled.location = 0,0
# node_texture = nodes.new('ShaderNodeTexImage')
#
# node_texture.image = bpy.data.images.load(r"C:\Users\vs6993\Downloads\Red_brick_wall_texture.JPG")
#
# node_texture.location = -400,0
# node_output = nodes.new(type='ShaderNodeOutputMaterial')
# node_output.location = 400,0
# links = mat.node_tree.links
# link = links.new(node_tex.outputs["Color"], node_principled.inputs["Base Color"])
# link = links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])

for image in os.listdir(IMAGE_ROOT_FOLDER):
    print(image)
