"""Run through Blender MCP after polish_tree.py to align falls with cliff lips."""
import bpy, json, contextlib, io
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
scene=bpy.data.scenes['Lumenwild_Refined'];bpy.context.window.scene=scene
offsets=[(0,5.5),(0,6),(19,19),(0,6.5),(0,7.5)]
changed=[]
for i,(dx,dz) in enumerate(offsets):
 for prefix in ('Water_Head_', 'Fall_', 'Foam_'):
  for o in scene.objects:
   if o.type=='MESH' and o.name.startswith(prefix+str(i)+'__') and not o.get('LipAligned'):
    for v in o.data.vertices:v.co+=Vector((dx,-dz,0))
    o['LipAligned']=True;changed.append(o.name)
bpy.ops.object.select_all(action='DESELECT')
objects=[o for o in scene.objects if o.type=='MESH']
for o in objects:o.select_set(True)
with contextlib.redirect_stdout(io.StringIO()):
 bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_Refined.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild.blend'))
deps=bpy.context.evaluated_depsgraph_get();tris=0
for o in objects:
 ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();tris+=len(me.loop_triangles);ev.to_mesh_clear()
manifest={'scene':scene.name,'iteration':3,'meshObjects':len(objects),'triangles':tris,'walkBounds':[-4.5,-18,4.5,28],'geometrySource':'Blender 5.1.2 MCP','refinements':['curved hero trunk','clear shrine opening','expanded pool','aligned waterfalls']}
(ROOT/'Assets/Exports/refined-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
result={'changed':changed,'manifest':manifest}
