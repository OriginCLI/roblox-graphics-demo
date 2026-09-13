"""Pack final texture sources and export all UVs with material links for Studio."""
import bpy, contextlib, io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
scene=bpy.data.scenes['Lumenwild_Refined'];bpy.context.window.scene=scene
stone=bpy.data.images.load(str(ROOT/'Assets/Textures/WetBasalt_Color.png'),check_existing=True)
normal=bpy.data.images.load(str(ROOT/'Assets/Textures/WetBasalt_Normal.png'),check_existing=True);normal.colorspace_settings.name='Non-Color'
leaves=bpy.data.images.load(str(ROOT/'Assets/Textures/ForestLeaves_Color.png'),check_existing=True)
seen=set()
for o in scene.objects:
 if o.type!='MESH':continue
 for m in o.data.materials:
  if not m or m.name in seen:continue
  seen.add(m.name);nt=m.node_tree;p=nt.nodes.get('Principled BSDF')
  im=leaves if m.name.startswith(('Leaf','Moss','Fern')) else stone if m.name.startswith('Stone') else None
  if im:
   t=nt.nodes.new('ShaderNodeTexImage');t.image=im;nt.links.new(t.outputs['Color'],p.inputs['Base Color'])
  if m.name.startswith('Stone'):
   t=nt.nodes.new('ShaderNodeTexImage');t.image=normal;n=nt.nodes.new('ShaderNodeNormalMap');nt.links.new(t.outputs['Color'],n.inputs['Color']);nt.links.new(n.outputs['Normal'],p.inputs['Normal'])
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:o.select_set(o.type=='MESH')
with contextlib.redirect_stdout(io.StringIO()):
 bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_Refined.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild.blend'))
result={'packed':len(bpy.data.images),'materials':len(seen),'export':str(ROOT/'Assets/Exports/Lumenwild_Refined.glb')}
