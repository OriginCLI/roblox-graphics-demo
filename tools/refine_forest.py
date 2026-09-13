"""Second composition pass, executed through Blender MCP. Preserves first scene.
Uses the original mesh-authoring helpers; all new geometry remains editable.
"""
import bpy, math, random, json, contextlib, io
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
source=(ROOT/'tools'/'build_forest.py').read_text()
exec(source.split('# Walkable continuous')[0])
scene.name='Lumenwild_Refined'
random.seed(92)
material('Flower',(.44,.18,.62),.8)
material('LeafGold',(.39,.48,.15),.85)
material('ShrineDark',(.07,.12,.10),.9)

def arch(name,mat,x,y,z,width,height,depth,thickness=.6):
 r=width/2
 for side in (-1,1): box(name,mat,(x+side*(r+thickness/2),y+(height-r)/2,z),(thickness,height-r,depth))
 for i in range(11):
  a=i*math.pi/11; b=(i+1)*math.pi/11
  v=[]
  for zz in (z-depth/2,z+depth/2):
   for rad,ang in [(r,a),(r,b),(r+thickness,b),(r+thickness,a)]: v.append((x+rad*math.cos(ang),y+height-r+rad*math.sin(ang),zz))
  geo(name,mat,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])

def island(i,x,z,r,top,bottom):
 # Varied narrow vertical blocks create a fractured ledge silhouette.
 for dx in range(-int(r),int(r)+1,3):
  for dz in range(-int(r),int(r)+1,3):
   if dx*dx+dz*dz>(r+random.uniform(-2,2))**2: continue
   yy=top+random.uniform(-.65,.65)
   box('Island_%s'%i,'Stone',(x+dx,(yy+bottom)/2,z+dz),(3.1,yy-bottom,3.1))
   box('IslandMoss_%s'%i,random.choice(['Moss','Moss','MossLight']),(x+dx,yy+.07,z+dz),(3.04,.18,3.03))
   if random.random()<.23: box('LedgeRubble_%s'%i,'StoneLight',(x+dx,yy+.4,z+dz),(1.5,.65,1.5),random.uniform(-.25,.25))

# Narrow bridge into the monumental tree. Walking remains on a convex strip.
box('Walkable_Base','WetSlate',(0,-.28,4),(11,.55,54))
for iz in range(27):
 for ix in range(5):
  x=(ix-2)*2.15+random.uniform(-.055,.055); z=-22+iz*2
  box('Walkable_Paving',random.choice(['WetSlate','WetSlate','WetSlateLight']),(x,.035,z),(2.04,.22,1.91),random.uniform(-.023,.023))
for z in range(-21,32,3):
 for x in (-5.65,5.65):
  box('BridgeSides','Stone',(x,-2.35,z),(1.25,4.7,2.95))
  if z%9==0:
   for k in range(3): box('BridgePiers','StoneLight',(x,.4+k*.73,z),(1.7,.69,1.65))
   box('BridgePierMoss','Moss',(x,2.33,z),(1.78,.13,1.76))
  else:
   box('BrokenParapets','Stone',(x,.42,z),(1.25,.8,2.9))
   box('ParapetMoss','Moss',(x,.9,z),(1.26,.13,2.9))
for z in (-18,-3,12,27):
 for x in (-5.5,5.5): box('BridgeFootings','Stone',(x,-7,z),(2.2,9,3))

island('Hero',0,-36,23,.3,-30)
island('LeftNear',-34,17,14,-1,-28)
island('LeftMid',-32,-19,12,2,-38)
island('RightNear',27,22,15,-3,-32)
island('RightBack',39,-46,18,5,-40)
island('FarLeft',-58,-70,13,17,-50)
island('FarMid',-19,-86,13,13,-50)
island('FarRight',29,-95,18,16,-50)

# Pools and waterfalls: broad textured sheets with a few irregular foam lips.
box('Water_Pool','Water',(-12,-6,2),(103,.14,92))
box('Water_Gorge','Water',(-28,-28,-74),(175,.15,112))
for i,(x,z,w,top,bottom) in enumerate([(-29,28,7,-.2,-6),(-25,-10,7,2.4,-6),(21,-44,6,5,-6),(-52,-62,7,17,-28),(-15,-78,5,13,-28)]):
 box('Water_Head_%d'%i,'Water',(x,top,z-3),(w,.16,7))
 # Different depth and height for each ribbon, avoiding parallel bright bars.
 for j in range(4):
  xx=x+(j-1.5)*w/4; h=top-bottom+random.uniform(-.4,.4)
  box('Fall_%d'%i,'Waterfall',(xx,top-h/2,z),(w/4+.04,h,.09),random.uniform(-.025,.025))
 for j in range(9):
  box('Foam_%d'%i,'Foam',(x+random.uniform(-w/2,w/2),bottom+.08,z+random.uniform(.2,3)),(random.uniform(.5,1.9),.04,random.uniform(.3,1.3)))

# Hero tree: offset trunk, angular buttress roots, and massive asymmetric limbs.
beam('HeroTrunk','Bark',(1,0,-35),(-1,29,-36),12,14)
beam('HeroTrunk','Bark',(-1,25,-36),(-7,55,-40),9,11)
beam('HeroBranch','Bark',(-2,30,-36),(-20,43,-32),6,7)
beam('HeroBranch','Bark',(-20,43,-32),(-34,46,-25),3.5,4)
beam('HeroBranch','Bark',(-2,32,-36),(18,45,-39),5.5,7)
beam('HeroBranch','Bark',(18,45,-39),(30,45,-31),3.4,4.2)
for n in range(13):
 a=n*math.tau/13; rad=random.uniform(13,20)
 start=(1+math.cos(a)*rad,.1,-35+math.sin(a)*rad)
 mid=(1+math.cos(a)*8,3.6,-35+math.sin(a)*8)
 end=(1+math.cos(a)*4.7,13+random.uniform(-3,3),-35+math.sin(a)*4.7)
 beam('HeroRoots','Bark',start,mid,2.4,3.7); beam('HeroRoots','Bark',mid,end,3,4)
 for j in range(5):
  t=j/5; p=Vector(start).lerp(Vector(mid),t)
  box('RootMoss',random.choice(['Moss','MossLight']),(p.x,p.y+1.5,p.z),(1.8,.3,1.5),a)
for i in range(170):
 a=random.uniform(0,math.tau); y=random.uniform(2,46); r=5.9-y*.035
 x=1+math.cos(a)*r-y*.12; z=-35+math.sin(a)*r-y*.08
 box('BarkPlates',random.choice(['Bark','Bark','BarkLight']),(x,y,z),(random.uniform(.7,1.7),random.uniform(1.3,3.3),.7),-a)

# The shrine is a shallow arched niche, set into the tree rather than a pavilion.
box('ShrineNiche','ShrineDark',(0,5,-27.15),(5.5,9.5,.2))
arch('ShrineArch','StoneLight',0,2,-26.7,4.3,8.6,1.4,.85)
arch('ShrineInnerGold','Brass',0,2.2,-25.94,3.7,7.7,.13,.18)
for x in (-3.3,3.3):
 box('ShrinePillars','Stone',(x,5,-27),(1.2,8,1.8))
 box('ShrineCaps','Moss',(x,9.2,-27),(1.6,.2,2))
for k in range(6): box('ShrineSteps','StoneLight',(0,.2+k*.35,-20.7-k*.8),(8.8-k*.2,.4,1.8))
box('RuneVertical','GlowAmber',(0,6.6,-26.93),(.18,2.3,.07))
box('RuneCross','GlowAmber',(0,6.85,-26.9),(1.2,.18,.07))
for i,(x,y,z) in enumerate([(-4,2.9,-21),(4,2.9,-21),(-3.9,6,-25.5)]):
 box('LanternPost','Stone',(x,y/2-.3,z),(.85,y-1,.85))
 box('Glow_Lantern_%d'%i,'GlowAmber',(x,y,z),(.58,.95,.58))
 box('LanternRoof','Brass',(x,y+.6,z),(.95,.18,.95))
 for dx in (-.33,.33):
  for dz in (-.33,.33): box('LanternFrame','Brass',(x+dx,y,z+dz),(.08,1.1,.08))
for i in range(5):
 x=random.uniform(-1.3,1.3)
 box('ShrineCandles','GlowAmber',(x,2.8,-25.5),( .14,random.uniform(.4,.9),.14))

def canopy(tag,x,y,z,r):
 # Individual offset cubes make a dappled, ragged canopy outline.
 for dx in range(-int(r),int(r)+1,2):
  for dz in range(-int(r),int(r)+1,2):
   d=math.sqrt(dx*dx+dz*dz)
   if d>r+random.uniform(-2,1): continue
   yy=y+max(0,1-d/r)*4+random.uniform(-1.1,1.1)
   mat=random.choices(['LeafDark','LeafMid','LeafLight','LeafGold'],[3,5,3,1])[0]
   box('Canopy_'+tag,mat,(x+dx,yy,z+dz),(random.uniform(1.9,3.6),random.uniform(1.4,3.2),random.uniform(1.9,3.6)))
 for i in range(15):
  xx=x+random.uniform(-r,r); zz=z+random.uniform(-r,r); length=random.uniform(3,9)
  beam('Vines_'+tag,'LeafDark',(xx,y-1,zz),(xx+.25,y-length,zz),.1)
  for j in range(int(length*2)):
   box('VineLeaves_'+tag,random.choice(['LeafMid','LeafDark']),(xx+random.uniform(-.25,.25),y-1-j*.5,zz),(.45,.18,.45),random.random()*3)

canopy('HeroA',-22,45,-33,18)
canopy('HeroB',12,48,-37,18)
canopy('HeroC',-7,56,-40,14)
for i,(x,z,h,r) in enumerate([(-39,16,39,15),(-38,-24,29,12),(35,-41,33,13),(-56,-72,35,13),(-17,-88,29,12),(29,-96,32,15),(40,30,30,11)]):
 base=17 if z<-60 else (-1 if z>0 else 3)
 beam('Trunk_%02d'%i,'Bark',(x,base,z),(x+1.5,base+h,z-1),3.7,4.7)
 for j in range(4):
  a=j*math.tau/4
  beam('TreeRoots','Bark',(x+math.cos(a)*7,base,z+math.sin(a)*7),(x,base+8,z),1.4,2)
  beam('TreeBranches','Bark',(x,base+h*.65,z),(x+math.cos(a)*r*.7,base+h,z+math.sin(a)*r*.7),1.5,2)
 canopy('%02d'%i,x,base+h,z,r)

# Distant arches and ruined towers establish scale across the open ravine.
for x in (-54,-42,-30): arch('DistantBridge','Stone',x,1,-67,9,17,3,.9)
box('DistantBridgeDeck','Stone',(-42,19,-67),(39,1.5,5))
for x in range(-60,-23,3):
 for z in (-69.4,-64.6): box('DistantBridgeRail','StoneLight',(x,20.6,z),(.5,2,.5))
for x,z,h in [(-50,-118,39),(-64,-116,31),(-35,-120,33)]:
 box('Citadel','Stone',(x,18+h/2,z),(5,h,6))
 for xx in (-2,0,2): box('CitadelCrown','StoneLight',(x+xx,18+h+.8,z),(1,1.8,6))
 cone('CitadelSpire','Stone',(x,18+h+4,z),3,0,8,4)
arch('CitadelGate','Stone',-49,19,-114,13,30,4,1.8)
box('CitadelGround','Stone',(-49,10,-118),(41,18,23))

# Bank plants, scattered rubble and tiny purple flowers concentrate near the path.
for i in range(650):
 side=random.choice([-1,1]); x=side*random.uniform(6,13); z=random.uniform(-26,35)
 y=.5 if z<-19 else random.uniform(.5,.85)
 if abs(x)>8 and z>-18: y=-3
 for k in range(5):
  a=k*math.tau/5+random.random(); h=random.uniform(.45,1.4); w=.18
  dx,dz=math.cos(a),math.sin(a)
  geo('PathFoliage','Fern',[(x-dz*w,y,z+dx*w),(x+dz*w,y,z-dx*w),(x+dx*.7,y+h,z+dz*.7)],[(0,1,2)])
 if i%4==0:
  for j in range(3):
   xx=x+random.uniform(-.5,.5); zz=z+random.uniform(-.5,.5)
   box('PurpleFlowers','Flower',(xx,y+.5,zz),(.3,.16,.3),random.random()*3)
 if i%7==0: box('EdgeMoss','Moss',(side*random.uniform(4.1,5.4),.18,z),(random.uniform(.3,1.1),.035,random.uniform(.3,1.3)),random.random())
for i in range(47):
 x,z=random.choice([(-10,-22),(11,-21),(-34,16),(-29,-14),(20,-35),(6,17),(-7,30)])
 x+=random.uniform(-2,2); z+=random.uniform(-2,2); y=0 if z<-19 or x<-20 else -.4
 h=random.uniform(.5,1.7)
 cone('MushroomStem','Stem',(x,y+h*.5,z),.12,.09,h,7)
 cone('Glow_Mushroom_%02d'%i,'GlowCyan',(x,y+h,z),h*.62,.1,h*.38,9)
 for j in range(4): box('MushroomSpots','Foam',(x+random.uniform(-h*.25,h*.25),y+h+.12,z+random.uniform(-h*.25,h*.25)),(.08,.035,.08))
for i in range(180):
 x=random.choice([-5.4,5.4])+random.uniform(-.35,.35); z=random.uniform(-20,29)
 box('BridgeIvy','LeafMid',(x,random.uniform(-3,.7),z),(.3,.2,.5),random.random()*3)

# Reuse the authored traveler geometry, with a larger readable silhouette.
exec(source.split('# Hero traveler, feet at origin.')[1].split('\n',1)[1].split('# Create real editable')[0])
objects=[]
for (name,mat),(vs,fs) in groups.items():
 mesh=bpy.data.meshes.new(name+'Mesh'); mesh.from_pydata(vs,[],fs); mesh.update()
 o=bpy.data.objects.new(name+'__'+mat,mesh); scene.collection.objects.link(o); mesh.materials.append(materials[mat]); objects.append(o)
 uv=mesh.uv_layers.new(name='UVMap')
 for poly in mesh.polygons:
  normal=poly.normal; axes=(0,1) if abs(normal.z)>.5 else ((0,2) if abs(normal.y)>.5 else (1,2))
  for li in poly.loop_indices:
   co=mesh.vertices[mesh.loops[li].vertex_index].co; uv.data[li].uv=(co[axes[0]]*.23,co[axes[1]]*.23)
 if mat not in ('Grass','Fern','Water','Waterfall','Foam','LeafDark','LeafMid','LeafLight','LeafGold','Flower'):
  mod=o.modifiers.new('Chipped silhouette','BEVEL'); mod.width=.055; mod.segments=1
 o['source']='Blender MCP authored';o['iteration']=2

stone=bpy.data.images.load(str(ROOT/'Assets'/'Textures'/'WetBasalt_Color.png'),check_existing=True)
for matname in ('WetSlate','WetSlateLight'):
 nt=materials[matname].node_tree; p=nt.nodes.get('Principled BSDF')
 tex=nt.nodes.new('ShaderNodeTexImage');tex.image=stone;nt.links.new(tex.outputs['Color'],p.inputs['Base Color'])
for matname in ('WetSlate','WetSlateLight','Water','Armor','Brass'):
 nt=materials[matname].node_tree;p=nt.nodes.get('Principled BSDF')
 im=bpy.data.images.load(str(ROOT/'Assets'/'Textures'/(matname+'_Roughness.png')),check_existing=True)
 tex=nt.nodes.new('ShaderNodeTexImage');tex.image=im;nt.links.new(tex.outputs['Color'],p.inputs['Roughness'])
normalPath=ROOT/'Assets'/'Textures'/'WetBasalt_Normal.png'
if normalPath.exists():
 im=bpy.data.images.load(str(normalPath),check_existing=True);im.colorspace_settings.name='Non-Color'
 for mn in ('WetSlate','WetSlateLight'):
  nt=materials[mn].node_tree;t=nt.nodes.new('ShaderNodeTexImage');t.image=im;n=nt.nodes.new('ShaderNodeNormalMap');nt.links.new(t.outputs['Color'],n.inputs['Color']);nt.links.new(n.outputs['Normal'],nt.nodes.get('Principled BSDF').inputs['Normal'])
scene.world=bpy.data.worlds.get('LumenwildSky')
camdata=bpy.data.cameras.new('RefinedPreview');cam=bpy.data.objects.new('RefinedPreview',camdata);scene.collection.objects.link(cam);cam.location=(30,-54,28);cam.rotation_euler=(Vector((0,13,9))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.lens=35;scene.camera=cam
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
# Pack texture sources for a portable editable Blender file.
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets'/'Blender'/'Lumenwild.blend'))
with contextlib.redirect_stdout(io.StringIO()):
 bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets'/'Exports'/'Lumenwild_Refined.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
deps=bpy.context.evaluated_depsgraph_get();tris=0
for o in objects:
 ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();tris+=len(me.loop_triangles);ev.to_mesh_clear()
manifest={'scene':scene.name,'iteration':2,'meshObjects':len(objects),'triangles':tris,'walkBounds':[-4.5,-18,4.5,28],'texture':'WetBasalt_Color.png','geometrySource':'Blender 5.1 MCP'}
(ROOT/'Assets'/'Exports'/'refined-manifest.json').write_text(json.dumps(manifest,indent=2))
result=manifest
