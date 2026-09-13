"""Asymmetric lobed crowns with open fringes replace regular canopy disks."""
import bpy,math,random,contextlib,io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
exec((ROOT/'tools/build_forest.py').read_text().split('# Walkable continuous')[0])
scene.name='Lumenwild_CanopyWild9';random.seed(922)
old=bpy.data.scenes['Lumenwild_Stage2']
for o in old.objects:
 if '__' in o.name and o.data.materials:materials[o.name.split('__')[-1].split('.')[0]]=o.data.materials[0]
source=bpy.data.scenes['Lumenwild_Landscape3']
bounds={}
for o in source.objects:
 if not o.name.startswith('CanopyVolume_'):continue
 tag=o.name.split('__')[0].replace('CanopyVolume_','')
 # The original crown chunks share the same tag; handle a possible numeric chunk suffix.
 if tag not in bounds:bounds[tag]=[[],[],[]]
 for v in o.data.vertices:
  bounds[tag][0].append(v.co.x);bounds[tag][1].append(v.co.z);bounds[tag][2].append(-v.co.y)
dirs=[((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((-1,0,0),[(0,0,1),(0,1,1),(0,1,0),(0,0,0)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,-1,0),[(0,0,1),(0,0,0),(1,0,0),(1,0,1)]),((0,0,1),[(1,0,1),(1,1,1),(0,1,1),(0,0,1)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)])]
for tag,b in bounds.items():
 x,y,z=[(min(v)+max(v))/2 for v in b];rx,ry,rz=[(max(v)-min(v))/2 for v in b]
 step=.85 if tag.startswith('Hero') or tag.startswith('Foreground') else 1.1
 lobes=[]
 for i in range(8):
  a=i*2.4;rr=random.uniform(.2,.7)
  lobes.append((math.cos(a)*rx*rr,random.uniform(-1.5,1.8),math.sin(a)*rz*rr,rx*random.uniform(.32,.53),ry*random.uniform(.7,1.2),rz*random.uniform(.35,.56)))
 lobes.append((0,0,0,rx*.55,ry*.9,rz*.55))
 cells=set()
 for ix in range(-math.ceil(rx/step)-2,math.ceil(rx/step)+3):
  for iy in range(-math.ceil(ry*1.5/step)-3,math.ceil(ry*1.5/step)+4):
   for iz in range(-math.ceil(rz/step)-2,math.ceil(rz/step)+3):
    dx,dy,dz=(ix+.5)*step,(iy+.5)*step,(iz+.5)*step
    field=min(((dx-lx)/lr)**2+((dy-ly)/lh)**2+((dz-lz)/ld)**2 for lx,ly,lz,lr,lh,ld in lobes)
    noise=.16*math.sin(dx*2.3+dz*1.7+dy)+.14*math.cos(dz*3.1-dy*2.2)
    if field<.93+noise and (field<.64 or random.random()>.12):cells.add((ix,iy,iz))
 for cell in cells:
  for d,face in dirs:
   if tuple(cell[k]+d[k]for k in range(3))in cells:continue
   mat=random.choices(['LeafDark','LeafMid','LeafLight'],[6,5,1]if d[1]<=0 else [2,6,4])[0]
   geo('CanopyWild9_'+tag,mat,[tuple((x,y,z)[k]+(cell[k]+v[k])*step for k in range(3))for v in face],[(0,1,2,3)])
 # Individual small leaf clusters break the long, straight fringe silhouettes.
 for i in range(int(rx*12)):
  a=random.random()*math.tau;r=random.uniform(.65,1.02);xx=x+math.cos(a)*rx*r;zz=z+math.sin(a)*rz*r;yy=y-ry*.5+random.uniform(-2,2)
  for j in range(random.randint(2,5)):
   sz=random.uniform(.25,.65);box('CanopyWildFringe9_'+tag,random.choice(['LeafDark','LeafMid']),(xx+random.uniform(-.3,.3),yy-j*.35,zz+random.uniform(-.3,.3)),(sz,sz*.75,sz),random.uniform(-.2,.2))

objects=[]
for (name,mat),(vs,fs)in groups.items():
 for offset in range(0,len(fs),6000):
  used={};cv=[];cf=[]
  for face in fs[offset:offset+6000]:
   f=[]
   for v in face:
    if v not in used:used[v]=len(cv);cv.append(vs[v])
    f.append(used[v])
   cf.append(f)
  me=bpy.data.meshes.new(name);me.from_pydata(cv,[],cf);me.update();o=bpy.data.objects.new(name+('_%d'%(offset//6000)if offset else '')+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
  uv=me.uv_layers.new(name='UVMap')
  for p in me.polygons:
   n=p.normal;axes=(0,1)if abs(n.z)>.5 else ((0,2)if abs(n.y)>.5 else (1,2))
   for li in p.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.32,co[axes[1]]*.32)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_CanopyWild9.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_CanopyWild9.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'meshes':len(objects),'crowns':list(bounds),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
