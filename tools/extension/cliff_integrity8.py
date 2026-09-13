"""Close cliff strata and rebuild distant support ground. Blender MCP only."""
import bpy,math,random,contextlib,io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
scene=bpy.data.scenes.new('Lumenwild_CliffIntegrity8');bpy.context.window.scene=scene
source=bpy.data.scenes['Lumenwild_Landscape3'];objects=[]
for old in source.objects:
 if not old.name.startswith('TerraceCliff_'):continue
 vs=[];fs=[]
 for p in old.data.polygons:
  coords=[old.data.vertices[i].co.copy() for i in p.vertices];n=p.normal
  start=len(vs);vs.extend(tuple(v)for v in coords);vs.extend(tuple(v-n*1.25)for v in coords);N=len(coords)
  fs.append(tuple(start+i for i in range(N)));fs.append(tuple(start+N+i for i in reversed(range(N))))
  for i in range(N):fs.append((start+i,start+(i+1)%N,start+(i+1)%N+N,start+i+N))
 # Closed stone blocks overlap inward; bright sky gaps between strata are removed.
 for offset in range(0,len(fs),5000):
  used={};cv=[];cf=[]
  for f in fs[offset:offset+5000]:
   face=[]
   for v in f:
    if v not in used:used[v]=len(cv);cv.append(vs[v])
    face.append(used[v])
   cf.append(face)
  me=bpy.data.meshes.new(old.name);me.from_pydata(cv,[],cf);me.update()
  tag,mat=old.name.split('__');o=bpy.data.objects.new(tag.replace('TerraceCliff_','CliffClosed8_')+'_'+str(offset//5000)+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(old.data.materials[0]);objects.append(o)
  uv=me.uv_layers.new(name='UVMap')
  for p in me.polygons:
   n=p.normal;axes=(0,1)if abs(n.z)>.5 else ((0,2)if abs(n.y)>.5 else (1,2))
   for li in p.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.14,co[axes[1]]*.14)

# A continuous low basin surrounds the actual scene for camera orbit.
N=96;vs=[(0,0,-58)];fs=[]
for ring in range(1,7):
 r=ring*85
 for i in range(N):
  a=i*math.tau/N;y=-58+max(0,ring-2)*6+4*math.sin(a*7+ring)
  vs.append((math.cos(a)*r,math.sin(a)*r,y))
for i in range(N):fs.append((0,1+i,1+(i+1)%N))
for ring in range(5):
 for i in range(N):
  a=1+ring*N+i;b=1+ring*N+(i+1)%N;fs.append((a,b,b+N,a+N))
me=bpy.data.meshes.new('DistantBasin');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('DistantBasin8__Stone',me);scene.collection.objects.link(o)
m=next(o.data.materials[0] for o in source.objects if o.name.endswith('__Stone'));me.materials.append(m);objects.append(o)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_CliffIntegrity8.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_CliffIntegrity8.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'meshes':len(objects),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
