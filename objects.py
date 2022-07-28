import bpy
import os

OBECT_ROOT_PATH = "D:\\Blender\\3D_MODELS\\apple_seperated.obj" 
SAVE_OBJECTS = ""
APPLE_body = "D:\\Blender\\apple\\body\\download(3).jpg"
IMAGE_ROOT_FOLDER = "D:\\Blender\\apple\\body"
STEM_IMAGE_PATH = "D:\\Blender\\apple\\stem\\Apple_stem.jpg"

imported_object = bpy.ops.import_scene.obj(filepath=OBECT_ROOT_PATH)
""" storing the objects in the list"""
object_list = [ obj for obj in bpy.data.objects if obj.name != "Camera" ]