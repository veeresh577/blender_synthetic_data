import bpy
import os
import time

IMAGE_ROOT_FOLDER = "D:\\Blender\\texture_imges\\"

bpy.ops.object.delete(use_global=False, confirm=False)

bpy.ops.mesh.primitive_monkey_add(size=3, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

active_obj = bpy.context.active_object

mod_subsurf = active_obj.modifiers.new("my modifier", "SUBSURF")
mod_subsurf.levels=4


#active_material = bpy.context.object.active_material
#nodes = mat.node_tree.nodes
#nodes.clear()

new_mat = bpy.data.materials.new("my_material")
active_obj.data.materials.append(new_mat)

new_mat.use_nodes = True
nodes = new_mat.node_tree.nodes

node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
node_principled.location = 0,0
node_tex = nodes.new('ShaderNodeTexImage')
 
node_tex.image = bpy.data.images.load(r"C:\Users\vs6993\Pictures\CycleOfLife.jpg")
    


node_tex.location = -400,0
node_output = nodes.new(type='ShaderNodeOutputMaterial')   
node_output.location = 400,0
links = new_mat.node_tree.links
link = links.new(node_tex.outputs["Color"], node_principled.inputs["Base Color"])
link = links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])


print("completed")