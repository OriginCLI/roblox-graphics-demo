"""Import PBR data textures through the proven albedo image path.
The small editable mesh swatches are archived after import, not rendered in the demo.
Run through Blender MCP only.
"""
import bpy, json, contextlib, io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
scene=bpy.data.scenes.new('Lumenwild_MaterialData');bpy.context.window.scene=scene
objects=[]
sources={'RoughWet':'WetSlate_Roughness_v2.png','RoughMetal':'Armor_Roughness_v2.png','NormalStone':'WetBasalt_Normal.png','NormalWater':'Water_Normal.png'}
for i,(name,filename) in enumerate(sources.items()):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata([(i*2,0,0),(i*2+1,0,0),(i*2+1,0,1),(i*2,0,1)],[],[(0,1,2,3)]);mesh.update()
    uv=mesh.uv_layers.new(name='UVMap')
    for j,p in enumerate([(0,0),(1,0),(1,1),(0,1)]):uv.data[j].uv=p
    ob=bpy.data.objects.new('Data_'+name,mesh);scene.collection.objects.link(ob);objects.append(ob)
    m=bpy.data.materials.new('Data_'+name);m.use_nodes=True
    im=bpy.data.images.load(str(ROOT/'Assets/Textures'/filename),check_existing=False)
    # Keep the file bytes intact. Roblox reads the uploaded image as a data map.
    im.colorspace_settings.name='sRGB'
    nt=m.node_tree;t=nt.nodes.new('ShaderNodeTexImage');t.image=im;nt.links.new(t.outputs['Color'],nt.nodes.get('Principled BSDF').inputs['Base Color']);mesh.materials.append(m)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_MaterialData.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_MaterialData.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'scene':scene.name,'meshes':len(objects),'sources':sources}
