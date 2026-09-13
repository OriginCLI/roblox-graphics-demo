"""Reassemble editable Blender geometry from current Studio transforms, preserving sources."""
import bpy,json,re,math
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
records=json.loads((ROOT/'Assets/assembly-source-map.json').read_text())
priority=['Lumenwild_CanopyWild9','Lumenwild_CliffIntegrity8','Lumenwild_Foreground7','Lumenwild_WaterRuins6','Lumenwild_Paving5','Lumenwild_DepthGarden4_Adjusted','Lumenwild_DepthGarden4','Lumenwild_Landscape3','Lumenwild_TreePatch2.001','Lumenwild_TreePatch2','Lumenwild_Stage2','Lumenwild_Refined','Lumenwild_Production']
lookup={}
for name in priority:
 s=bpy.data.scenes.get(name)
 if not s:continue
 for o in s.objects:
  if o.type!='MESH':continue
  key=re.sub(r'\.\d+$','',o.name)
  if key not in lookup:lookup[key]=o
scene=bpy.data.scenes.new('Lumenwild_Assembled_90');bpy.context.window.scene=scene
missing=[];sources={}
for r in records:
 src=lookup.get(r['name'])
 if not src:missing.append(r['name']);continue
 o=src.copy();o.data=src.data.copy();o.name='ASSEMBLY_'+r['name'];scene.collection.objects.link(o)
 pts=[Vector((v.co.x,v.co.z,-v.co.y))for v in src.data.vertices]
 lo=Vector(tuple(min(p[k]for p in pts)for k in range(3)));hi=Vector(tuple(max(p[k]for p in pts)for k in range(3)));center=(lo+hi)/2
 scale=Vector(tuple(r['size'][k]/max(hi[k]-lo[k],.00001)for k in range(3)))
 cf=r['cf'];pos=Vector(cf[:3]);rot=Matrix([cf[3:6],cf[6:9],cf[9:12]])@Matrix.Diagonal(Vector((-1,1,-1)))
 for v,p in zip(o.data.vertices,pts):
  q=p-center;q=Vector(tuple(q[k]*scale[k]for k in range(3)));q=pos+rot@q;v.co=(q.x,-q.z,q.y)
 o.matrix_world=Matrix.Identity(4);o.data.update();o['RobloxName']=r['name'];sources[r['name']]=src.name
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_Assembled90.blend'))
(ROOT/'Assets/assembly-mapping.json').write_text(json.dumps({'missing':missing,'sources':sources},indent=2))
result={'assembled':len(scene.objects),'missing':missing}
