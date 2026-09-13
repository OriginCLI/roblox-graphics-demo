"""Lumenwild editable asset source. Execute in Blender 5.1 via Blender MCP.
Coordinates in this builder are Roblox studs, Y up. The mesh helper converts
to Blender Z up so glTF's Y-up export restores the authored world coordinates.
Default scenes are preserved. Seeded composition is intentionally reproducible.
"""
import bpy, math, random, json
from pathlib import Path
from mathutils import Vector

ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
random.seed(31)
scene=bpy.data.scenes.new('Lumenwild_Production')
bpy.context.window.scene=scene
scene.unit_settings.system='NONE'
groups={}
materials={}

def material(name,color,rough=.7,metal=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    materials[name]=m
    return m

palette={
 'Stone':((.19,.245,.235),.78), 'StoneLight':((.29,.36,.32),.72),
 'WetSlate':((.14,.22,.225),.17), 'WetSlateLight':((.21,.29,.28),.2),
 'Earth':((.105,.15,.125),.95), 'Moss':((.24,.39,.17),.96),
 'MossLight':((.36,.48,.21),.94),'Bark':((.135,.19,.13),.95),
 'BarkLight':((.23,.28,.16),.9), 'LeafDark':((.075,.245,.15),.9),
 'LeafMid':((.13,.35,.18),.85), 'LeafLight':((.25,.46,.21),.82),
 'Grass':((.26,.47,.23),.85), 'Fern':((.18,.42,.28),.8),
 'Water':((.075,.44,.44),.09), 'Waterfall':((.23,.69,.66),.2),
 'Foam':((.6,.87,.79),.25), 'GlowCyan':((.18,.85,.83),.35),
 'Stem':((.25,.51,.46),.75), 'Brass':((.54,.35,.12),.26),
 'GlowAmber':((1,.55,.12),.25), 'Roof':((.16,.30,.28),.55),
 'Cloth':((.09,.18,.18),.85), 'Armor':((.22,.29,.30),.3),
 'Leather':((.17,.13,.10),.83), 'Face':((.52,.40,.29),.85),
}
for n,(c,r) in palette.items(): material(n,c,r,.7 if n in ('Armor','Brass') else 0)

def convert(v): return (v[0],-v[2],v[1])
def geo(name,mat,verts,faces):
    key=(name,mat)
    g=groups.setdefault(key,[[],[]]); off=len(g[0])
    g[0].extend(convert(v) for v in verts); g[1].extend(tuple(off+i for i in f) for f in faces)

def box(name,mat,center,size,angle=0):
    x,y,z=center; sx,sy,sz=(s/2 for s in size); c=math.cos(angle); s=math.sin(angle)
    vs=[]
    for dx,dy,dz in [(-sx,-sy,-sz),(sx,-sy,-sz),(sx,sy,-sz),(-sx,sy,-sz),(-sx,-sy,sz),(sx,-sy,sz),(sx,sy,sz),(-sx,sy,sz)]:
        vs.append((x+dx*c+dz*s,y+dy,z-dx*s+dz*c))
    geo(name,mat,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)])

def beam(name,mat,a,b,width,depth=None):
    a=Vector(a); b=Vector(b); d=(b-a).normalized(); ref=Vector((0,1,0))
    if abs(d.dot(ref))>.95: ref=Vector((1,0,0))
    side=d.cross(ref).normalized()*width/2; up=d.cross(side).normalized()*(depth or width)/2
    vs=[tuple(p+u*side+v*up) for p in (a,b) for u,v in [(-1,-1),(1,-1),(1,1),(-1,1)]]
    geo(name,mat,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)])

def cone(name,mat,center,r1,r2,h,n=8):
    x,y,z=center
    vs=[(x+math.cos(i*math.tau/n)*r,y+dy,z+math.sin(i*math.tau/n)*r) for dy,r in [(-h/2,r1),(h/2,r2)] for i in range(n)]
    fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    geo(name,mat,vs,fs)

# Walkable continuous surface, segmented low curbs, and irregular wet paving.
box('Walkable_Base','WetSlate',(0,-.38,3),(42,.7,34))
for i in range(-7,7):
 for j in range(-5,6):
    x=i*3+1.5; z=j*3+3
    box('Walkable_Paving','WetSlate' if random.random()<.6 else 'WetSlateLight',(x,-.025+random.uniform(0,.025),z),(2.92,.18,2.92),random.uniform(-.01,.01))
    if random.random()<.23 and (abs(x)>12 or abs(z-3)>10):
       box('MossSeams','Moss',(x+1.4,.075,z),(random.uniform(.08,.3),.025,2.8))

# Multi-level fractured escarpment extends well beyond the playable clearing.
for ring in range(3):
 step=6 if ring==0 else 10
 for x in range(-76,77,step):
  for z in range(-80,59,step):
   if -23<x<23 and -17<z<23: continue
   if ring==0 and (abs(x)>37 or z<-43 or z>33): continue
   if ring==1 and (abs(x)<37 and -43<z<33): continue
   if ring==2 and (abs(x)<57 and -63<z<43): continue
   # Stream snakes to the left of the walk platform.
   if -37<x<-21 and -50<z<35: continue
   h=random.uniform(1.5,4) + (max(0,-z-25)*.19)
   if ring==2: h+=random.uniform(4,12)
   mat='Stone' if random.random()<.7 else 'StoneLight'
   name='Cliffs_%d'%ring
   box(name,mat,(x,-5+h/2,z),(step*.99,h+5,step*.99))
   box('MossShelf_%d'%ring,'Moss' if random.random()<.75 else 'MossLight',(x,h-2.42,z),(step*.97,.2,step*.97))

# Deep turquoise stream with stair-like waterfall shelves.
box('Water_Stream','Water',(-29,-1.15,-1),(16,.16,85))
box('Water_Pool','Water',(-14,-1.3,29),(45,.14,16))
for k,(z,top,bottom) in enumerate([(-45,20,11),(-38,11,4),(-30,4,-1)]):
 box('FallsRock_%d'%k,'Stone',(-29,(top-6)/2,z-3),(16,top+6,7))
 box('Water_Shelf_%d'%k,'Water',(-29,top+.1,z-3),(13,.18,7))
 box('Fall_%d'%k,'Waterfall',(-29,(top+bottom)/2,z+.61),(11.4,top-bottom,.18))
 for n in range(9):
    box('FallStreak_%d'%k,'Foam',(-34+n*1.25,(top+bottom)/2+random.uniform(-.3,.3),z+.77),(.13+random.random()*.14,top-bottom,.025))
 box('Foam_%d'%k,'Foam',(-29,bottom+.15,z+1.5),(11.7,.08,1.4))

# Shrine at the back right: stepped plinth, four columns, layered roof and rune.
for k in range(3): box('ShrineSteps','StoneLight',(16,k*.55,-21),(13-k*1.5,.55,10-k*1.2))
for x in (12,20):
 for z in (-24,-18):
    box('ShrineColumns','Stone',(x,4.6,z),(1.05,7.3,1.05))
    for y in (1.8,7.5): box('ShrineCaps','StoneLight',(x,y,z),(1.65,.55,1.65))
for k in range(4): box('ShrineRoof','Roof',(16,8.2+k*.65,-21),(14-k*2,.6,11-k*1.6))
box('ShrineRoof','Moss',(16,10.4,-21),(4.7,.18,3.8))
box('Altar','Stone',(16,2.15,-21),(3.5,1.6,2.6))
cone('ShrineCrystal','GlowCyan',(16,4.2,-21),.8,0,2.6,6)
for x in (10,22):
 box('ShrineLanternStand','Bark',(x,2,-16.5),(.3,4,.3))
 box('Glow_ShrineLantern','GlowAmber',(x,4.2,-16.5),(.65,.85,.65))
 box('ShrineLanternCap','Brass',(x,4.75,-16.5),(1,.2,1))

# Ancient boundary fragments, carefully kept outside the walk rectangle.
for i in range(12):
 x=-20+i*3.6
 if 7<x<22: continue
 for y in range(random.choice([1,2,3])):
    box('RuinedWall','Stone',(x,.45+y*.85,-16.5),(3.3,.8,1.4))
 box('WallMoss','Moss',(x,.95+y*.85,-16.5),(3.35,.1,1.5))
for x,z in [(-18,22),(18,22),(-21,-12),(23,-7)]:
 for k in range(3): box('Waystone','Stone',(x,k*.8+.3,z),(1.4-k*.15,.75,1.4-k*.15))
 box('Glow_Waystone','GlowCyan',(x,2.1,z-.66),(.18,.65,.035))

# Giant angular trees: buttress roots, branching trunks and layered canopy plates.
trees=[(-39,-19,31,1.2),(-18,-29,29,1),(-2,-39,36,1.25),(37,-22,33,1.2),(31,9,27,.95),(-40,15,28,1.1),(-57,-44,36,1.3),(53,-49,39,1.3),(21,-61,43,1.35),(-25,-67,41,1.5),(66,-17,33,1.2),(-63,0,30,1.1),(52,29,33,1.2)]
for ti,(x,z,h,s) in enumerate(trees):
 base=max(0,-z-30)*.18
 for n in range(5):
    a=n*math.tau/5+.3
    beam('Trunk_%02d'%ti,'Bark',(x+math.cos(a)*5*s,base,z+math.sin(a)*5*s),(x,base+7*s,z),1.3*s,1.7*s)
 beam('Trunk_%02d'%ti,'Bark',(x,base,z),(x+1.2*s,base+h,z-.6*s),2.7*s,3.2*s)
 beam('TrunkRidge_%02d'%ti,'BarkLight',(x-1.2*s,base+3,z+1.2*s),(x-.3*s,base+h*.8,z+.8*s),.48*s,.6*s)
 for n in range(5):
    a=n*math.tau/5+ti*.63; end=(x+math.cos(a)*8*s,base+h-4+random.uniform(-2,3),z+math.sin(a)*8*s)
    beam('Branch_%02d'%ti,'Bark',(x,base+h*.6,z),end,1.5*s,1.3*s)
 for level in range(3):
  for n in range(8-level*2):
    a=n*math.tau/(8-level*2)+level*.5
    radius=(7-level*1.5)*s
    xx=x+math.cos(a)*radius; zz=z+math.sin(a)*radius
    size=(random.uniform(6,10)*s,random.uniform(2.4,4)*s,random.uniform(5,9)*s)
    box('Canopy_%02d'%ti,['LeafDark','LeafMid','LeafLight'][level],(xx,base+h+level*2.5,zz),size,random.choice([0,math.pi/2]))
 for j in range(5):
    xx=x+random.uniform(-8,8)*s; zz=z+random.uniform(-7,7)*s
    beam('Vines_%02d'%ti,'LeafDark',(xx,base+h-2,zz),(xx+.5,base+h-random.uniform(6,11),zz+.3),.18)

# Smaller distant trees close the horizon, without heavy trunk detail.
for i in range(20):
 x=random.uniform(-110,110); z=random.uniform(-110,-75); h=random.uniform(30,47); base=12
 box('DistantTrunks','Bark',(x,base+h/2,z),(2,h,2))
 for k in range(3): box('DistantCanopy','LeafDark' if k==0 else 'LeafMid',(x,base+h+k*2,z),(16-k*3,4,14-k*2))

# Cyan mushrooms on both banks, with individual glowing cap assets.
for i in range(42):
 x,z=random.choice([(-22,9),(-22,-12),(24,14),(24,-10),(-38,-20),(-36,21),(8,-18)])
 x+=random.uniform(-2.7,2.7); z+=random.uniform(-4,4); h=random.uniform(.65,1.9)
 y=.1 if x>-23 else 0
 cone('MushroomStems','Stem',(x,y+h*.5,z),.15,.1,h,6)
 cone('Glow_Mushroom_%02d'%i,'GlowCyan',(x,y+h,z),h*.65,.15,h*.4,8)
 box('MushroomGills','Foam',(x,y+h-.15,z),(h*.6,.07,h*.6))

# Grass and ferns use flat authored leaves, clustered at the banks and paving edge.
for i in range(760):
 x=random.uniform(-45,45); z=random.uniform(-36,32)
 if -20<x<20 and -14<z<20: continue
 if -36<x<-24: continue
 y=max(0,-z-25)*.19
 for k in range(3):
    a=random.random()*math.tau; h=random.uniform(.4,1.3); w=random.uniform(.12,.32)
    dx,dz=math.cos(a),math.sin(a)
    geo('GroundGrass','Grass',[(x-dz*w,y,z+dx*w),(x+dz*w,y,z-dx*w),(x+dx*.35,y+h,z+dz*.35)],[(0,1,2)])
for i in range(70):
 x=random.choice([-23,24,-40,33])+random.uniform(-2,2); z=random.uniform(-28,25); y=max(0,-z-25)*.19
 for a in [k*math.tau/5 for k in range(5)]:
  for j in range(4):
    t=(j+1)/4; c=(x+math.cos(a)*t*1.8,y+math.sin(t*2.3)*1.2,z+math.sin(a)*t*1.8)
    for sign in (-1,1):
     tip=(c[0]+math.cos(a+sign*1.1)*.7,c[1]+.05,c[2]+math.sin(a+sign*1.1)*.7)
     geo('Ferns','Fern',[c,(c[0]+math.cos(a)*.35,c[1]-.1,c[2]+math.sin(a)*.35),tip],[(0,1,2)])

# Hero traveler, feet at origin. Separate limb meshes support client animation.
box('Actor_LegL','Leather',(-.33,.65,0),(.49,1.1,.6))
box('Actor_LegR','Leather',(.33,.65,0),(.49,1.1,.6))
box('Actor_BootL','Armor',(-.33,.18,-.15),(.55,.35,.88))
box('Actor_BootR','Armor',(.33,.18,-.15),(.55,.35,.88))
box('Actor_Body','Armor',(0,1.85,0),(1.35,1.35,.72))
box('Actor_Belt','Brass',(0,1.4,0),(1.42,.16,.8))
box('Actor_ArmL','Armor',(-.9,1.9,0),(.48,1.1,.56))
box('Actor_ArmR','Armor',(.9,1.9,0),(.48,1.1,.56))
box('Actor_PauldronL','Brass',(-.8,2.4,0),(.69,.42,.82))
box('Actor_PauldronR','Armor',(.8,2.4,0),(.69,.42,.82))
box('Actor_Hood','Cloth',(0,2.93,.02),(1.02,.96,1.03))
box('Actor_Face','Face',(0,2.88,-.51),(.58,.48,.025))
box('Actor_Visor','Leather',(0,3.04,-.54),(.67,.18,.03))
geo('Actor_Cloak','Cloth',[(-.65,2.6,.39),(.65,2.6,.39),(.95,.5,.77),(-.95,.5,.77),(-.5,2.55,.56),(.5,2.55,.56),(.8,.45,.95),(-.8,.45,.95)],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(0,3,7,4),(1,5,6,2)])
beam('Actor_Sword','Armor',(.6,.8,.75),(-.45,2.65,.75),.15,.32)
beam('Actor_SwordGuard','Brass',(-.65,2.32,.75),(-.05,2.68,.75),.12)
box('Actor_Lantern','GlowAmber',(-1.05,1.14,-.18),(.29,.42,.29))

# Create real editable mesh datablocks, projected UVs and small bevels.
objects=[]
for (name,mat),(vs,fs) in groups.items():
 mesh=bpy.data.meshes.new(name+'Mesh'); mesh.from_pydata(vs,[],fs); mesh.update()
 o=bpy.data.objects.new(name+'__'+mat,mesh); scene.collection.objects.link(o); o.data.materials.append(materials[mat]); objects.append(o)
 uv=mesh.uv_layers.new(name='UVMap')
 for poly in mesh.polygons:
  normal=poly.normal; axes=(0,1) if abs(normal.z)>.5 else ((0,2) if abs(normal.y)>.5 else (1,2))
  for li in poly.loop_indices:
   co=mesh.vertices[mesh.loops[li].vertex_index].co; uv.data[li].uv=(co[axes[0]]*.23,co[axes[1]]*.23)
 if mat not in ('Grass','Fern','Water','Waterfall','Foam'):
  mod=o.modifiers.new('Soft crafted edges','BEVEL'); mod.width=.055 if not name.startswith('Actor') else .035; mod.segments=1
  mod.affect='EDGES'
 o['source']='Authored in Blender 5.1 via MCP'; o['role']='character' if name.startswith('Actor_') else 'environment'

# Export material maps ensure low roughness survives PBR import.
for matname in ('WetSlate','WetSlateLight','Water','Armor','Brass'):
 m=materials[matname]; nt=m.node_tree; p=nt.nodes.get('Principled BSDF')
 im=bpy.data.images.new(matname+'_Roughness',width=8,height=8)
 value=palette[matname][1]; im.pixels[:]=[value,value,value,1]*64
 im.colorspace_settings.name='Non-Color'; im.filepath_raw=str(ROOT/'Assets'/'Textures'/(matname+'_Roughness.png')); im.file_format='PNG'; im.save()
 tex=nt.nodes.new('ShaderNodeTexImage'); tex.image=im; nt.links.new(tex.outputs['Color'],p.inputs['Roughness'])

# Blender presentation camera is for source inspection only, not runtime evidence.
camdata=bpy.data.cameras.new('SourcePreview'); cam=bpy.data.objects.new('SourcePreview',camdata); scene.collection.objects.link(cam)
cam.location=(48,-66,55); direction=Vector((0,4,4))-cam.location; cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler(); camdata.type='ORTHO'; camdata.ortho_scale=90; scene.camera=cam
world=bpy.data.worlds.new('LumenwildSky'); world.use_nodes=True; world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.3,.28,1); world.node_tree.nodes['Background'].inputs[1].default_value=.5; scene.world=world
ld=bpy.data.lights.new('Warm canopy sun','SUN'); lo=bpy.data.objects.new('Warm canopy sun',ld); scene.collection.objects.link(lo); lo.rotation_euler=(.4,-.5,-.45); ld.energy=3
scene.render.engine='CYCLES'; scene.cycles.samples=16
scene.render.resolution_x=1600; scene.render.resolution_y=1000; scene.render.resolution_percentage=100
bpy.ops.object.select_all(action='DESELECT')
for o in objects: o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets'/'Blender'/'Lumenwild.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets'/'Exports'/'Lumenwild.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
deps=bpy.context.evaluated_depsgraph_get(); tris=0
for o in objects:
 me=o.evaluated_get(deps).to_mesh(); me.calc_loop_triangles(); tris+=len(me.loop_triangles); o.evaluated_get(deps).to_mesh_clear()
manifest={'scene':scene.name,'seed':31,'objects':len(objects),'triangles':tris,'world_bounds_studs':[-120,-10,-120,120,80,70],'walk_bounds':[-20,-13,20,19],'coordinate_conversion':'Roblox(x,y,z) -> Blender(x,-z,y) -> glTF(x,y,z)','objects_by_name':[o.name for o in objects]}
(ROOT/'Assets'/'Exports'/'manifest.json').write_text(json.dumps(manifest,indent=2))
result=manifest

