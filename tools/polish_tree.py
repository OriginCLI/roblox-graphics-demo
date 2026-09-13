"""Blender MCP refinement: taper the hero trunk and leave shrine entrance clear."""
import bpy, math, json, contextlib, io
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
scene=bpy.data.scenes['Lumenwild_Refined'];bpy.context.window.scene=scene
def convert(v):return (v[0],-v[2],v[1])
def tube(points,radii,sides=12):
 vs=[];fs=[]
 for j,p in enumerate(points):
  d=(Vector(points[min(j+1,len(points)-1)])-Vector(points[max(j-1,0)])).normalized()
  side=d.cross(Vector((0,0,1))).normalized();up=side.cross(d).normalized()
  for n in range(sides):
   a=n*math.tau/sides
   v=Vector(p)+(side*math.cos(a)+up*math.sin(a))*radii[j]
   vs.append(convert(v))
 for j in range(len(points)-1):
  for n in range(sides):fs.append((j*sides+n,j*sides+(n+1)%sides,(j+1)*sides+(n+1)%sides,(j+1)*sides+n))
 fs.extend([tuple(reversed(range(sides))),tuple(range((len(points)-1)*sides,len(points)*sides))])
 return vs,fs
def replace(prefix,vs,fs):
 o=next(o for o in scene.objects if o.name.startswith(prefix+'__'))
 mat=o.data.materials[0]
 me=bpy.data.meshes.new(prefix+'_Sculpted');me.from_pydata(vs,[],fs);me.update();o.data=me;me.materials.append(mat)
 uv=me.uv_layers.new(name='UVMap')
 for poly in me.polygons:
  ax=(0,2) if abs(poly.normal.y)>.5 else (1,2)
  for li in poly.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[ax[0]]*.19,co[ax[1]]*.19)
 return o
points=[];r=[]
for j in range(20):
 y=j*3;points.append((1-y*.14+math.sin(y*.09)*1.5,y,-35-y*.085+math.sin(y*.08)));r.append(6.5-y*.035+math.sin(j*.7)*.22)
vs,fs=tube(points,r,14);trunk=replace('HeroTrunk',vs,fs)
verts=[];faces=[]
for i in range(15):
 a=i*math.tau/15
 # Opening faces +Z. Buttresses frame it on both sides.
 if math.sin(a)>.78:continue
 radius=15+(i%3)*2
 pts=[]
 for t in (0,.22,.47,.72,1):
  rad=radius*(1-t)+4.2*t
  pts.append((1+math.cos(a)*rad,.1+12*t*t,-35+math.sin(a)*rad))
 v,f=tube(pts,[.35,1.05,1.75,2.3,2.6],7);off=len(verts);verts.extend(v);faces.extend(tuple(k+off for k in face) for face in f)
roots=replace('HeroRoots',verts,faces)
# Widen water sheets so their outer rectangular edges stay beyond the view.
pool=next(o for o in scene.objects if o.name.startswith('Water_Pool__'))
if not pool.get('expanded'):
 for v in pool.data.vertices:
  v.co.x=-12+(v.co.x+12)*3
  v.co.y=-2+(v.co.y+2)*3
 pool['expanded']=True
bark=bpy.data.images.load(str(ROOT/'Assets'/'Textures'/'AncientBark_Color.png'),check_existing=True)
water=bpy.data.images.load(str(ROOT/'Assets'/'Textures'/'Water_Normal.png'),check_existing=True);water.colorspace_settings.name='Non-Color'
for o in scene.objects:
 if o.type!='MESH':continue
 for m in o.data.materials:
  if m is None:continue
  nt=m.node_tree;p=nt.nodes.get('Principled BSDF')
  if m.name.startswith('Bark'):
   if not any(n.type=='TEX_IMAGE' and n.image==bark for n in nt.nodes):
    t=nt.nodes.new('ShaderNodeTexImage');t.image=bark;nt.links.new(t.outputs['Color'],p.inputs['Base Color'])
  if m.name.startswith('Water'):
   if not any(n.type=='TEX_IMAGE' and n.image==water for n in nt.nodes):
    t=nt.nodes.new('ShaderNodeTexImage');t.image=water;n=nt.nodes.new('ShaderNodeNormalMap');nt.links.new(t.outputs['Color'],n.inputs['Color']);nt.links.new(n.outputs['Normal'],p.inputs['Normal'])
bpy.ops.object.select_all(action='DESELECT')
for o in (trunk,roots):o.select_set(True)
bpy.context.view_layer.objects.active=trunk
with contextlib.redirect_stdout(io.StringIO()):
 bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets'/'Exports'/'HeroTree_Polish.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
# Final full export matches the source geometry/materials, including the patch.
for o in scene.objects:o.select_set(o.type=='MESH')
with contextlib.redirect_stdout(io.StringIO()):
 bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets'/'Exports'/'Lumenwild_Refined.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets'/'Blender'/'Lumenwild.blend'))
result={'patched':[trunk.name,roots.name],'pool_size':list(pool.dimensions),'source':bpy.data.filepath}
