"""Instance Blender-authored cliff/tree assets into a continuous distant forest."""
import bpy, json, contextlib, io
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
scene=bpy.data.scenes['Lumenwild_Refined'];bpy.context.window.scene=scene
positions=[(-95,-65,0),(-98,-28,-8),(-80,-102,6),(-57,-113,2),(-125,-72,10),(-126,-24,-3),(-91,14,-12),(-68,33,-15),(72,-55,-7),(63,-100,3)]
prefixes=('Island_FarLeft__','IslandMoss_FarLeft__','LedgeRubble_FarLeft__','Trunk_03__','Canopy_03__','Vines_03__','VineLeaves_03__')
sources=[o for o in scene.objects if o.type=='MESH' and o.name.startswith(prefixes)]
added=[]
for i,(x,z,y) in enumerate(positions):
 for source in sources:
  name='Depth_%02d_'%i+source.name.split('.')[0]
  if scene.objects.get(name):continue
  obj=source.copy();obj.data=source.data;obj.name=name;scene.collection.objects.link(obj)
  obj.location+=Vector((x+56,-(z+72),y));obj['source']='Blender mesh instance';added.append(obj.name)
bpy.ops.object.select_all(action='DESELECT')
objects=[o for o in scene.objects if o.type=='MESH']
for o in objects:o.select_set(True)
with contextlib.redirect_stdout(io.StringIO()):
 bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_Refined.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild.blend'))
deps=bpy.context.evaluated_depsgraph_get();tris=0
for o in objects:
 ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();tris+=len(me.loop_triangles);ev.to_mesh_clear()
manifest={'scene':scene.name,'iteration':4,'meshObjects':len(objects),'triangles':tris,'walkBounds':[-4.5,-18,4.5,28],'geometrySource':'Blender 5.1.2 MCP','depthInstances':len(added)}
(ROOT/'Assets/Exports/refined-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
result=manifest
