"""Modeled depth layers, rooted planting, shrine and mushroom silhouette refinement."""
import bpy, math, random, contextlib, io
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
exec((ROOT/'tools/build_forest.py').read_text().split('# Walkable continuous')[0])
scene.name='Lumenwild_DepthGarden4'
old=bpy.data.scenes['Lumenwild_Stage2']
for o in old.objects:
    if '__' in o.name and o.data.materials:materials[o.name.split('__')[-1].split('.')[0]]=o.data.materials[0]
src=(ROOT/'tools/extension/build_reworked.py').read_text()
exec(src[src.index('def tube('):src.index('# The same bounded')])
random.seed(482)

# Broad, fully modeled mountain ridges behind the ravine, visible during orbit.
right=Vector((.819152,0,-.573576));forward=Vector((-.573576,0,-.819152))
for band in range(3):
    verts=[];faces=[];width=720;depth=150;N=60;M=10
    for j in range(M+1):
      d=230+band*135+j*depth/M
      for i in range(N+1):
        t=-width/2+i*width/N
        ridge=57+band*18+28*math.sin(t*.018+band)+15*math.sin(t*.049-band*.6)+8*math.cos(t*.09)
        y=-55+(ridge+55)*math.sin(math.pi*j/M)**.65
        p=right*t+forward*d;verts.append((p.x,y,p.z))
    for j in range(M):
      for i in range(N):
        a=j*(N+1)+i;faces.extend([(a,a+N+1,a+N+2),(a,a+N+2,a+1)])
    geo('DistantRidge_%d'%band,'CliffDark',verts,faces)
# Irregular forest silhouettes occupy several real distances rather than one wall.
for i in range(95):
    t=random.uniform(-220,210);d=random.uniform(175,310);p=right*t+forward*d
    y=random.uniform(-2,17);h=random.uniform(14,32);r=random.uniform(5,12)
    tube('DeepForestTrunks','Bark',[(p.x,y,p.z),(p.x-1,y+h*.7,p.z),(p.x+2,y+h,p.z)],[1.7,1,.3],7,4)
    for j in range(45):
        a=random.random()*math.tau;rr=r*math.sqrt(random.random());sz=random.uniform(1.8,3.8)
        box('DeepForestCrowns',random.choice(['LeafDark','LeafDark','LeafMid']),(p.x+math.cos(a)*rr,y+h+random.uniform(-2.5,3),p.z+math.sin(a)*rr*.7),(sz,random.uniform(1,3),sz),random.uniform(-.1,.1))

# Source-tree surface samples create coherent living patches on the lower bark.
treeScene=bpy.data.scenes.get('Lumenwild_TreePatch2.001') or bpy.data.scenes['Lumenwild_TreePatch2']
tree=next(o for o in treeScene.objects if o.name.startswith('SOURCE_UnifiedTree'))
candidates=[]
for p in tree.data.polygons:
    c=p.center;n=p.normal;x,y,z=c.x,c.z,-c.y
    visible=n.x*.52+n.z*.4-n.y*.75
    clustered=math.sin(x*.5+z*.18)+math.cos(y*.43-z*.4)>.3
    if -.5<y<32 and visible>.05 and clustered:candidates.append(p)
for p in random.sample(candidates,min(3500,len(candidates))):
    c=p.center+p.normal*.22;x,y,z=c.x,c.z,-c.y;s=random.uniform(.45,1.0)
    box('RootLivingMoss',random.choice(['Moss','LeafDark','LeafMid']),(x,y,z),(s,.5,s),random.uniform(-.2,.2))
    if random.random()<.3:
        for side in (-1,1):
            geo('RootLeafSprays','Fern',[(x,y,z),(x+side*.55,y+.3,z+.1),(x+side*.2,y+.65,z+.25)],[(0,1,2)])

# Ground-contact banks support every near mushroom cluster and bridge-edge garden.
beds=[(-8,24,-.7,3.6,5),(8,23,-.7,3.1,5),(-8,41,-.7,3.7,6),(-45,18,2,5,5),(-48,-20,4,5,5),(-8,-22,.5,4,5),(12,-25,.5,5,5),(19,-23,.6,5,6)]
def fern(tag,x,y,z,size):
    for k in range(6):
        a=k*math.tau/6+random.uniform(-.15,.15);dx,dz=math.cos(a),math.sin(a)
        for j in range(5):
            t=(j+.5)/5;xx=x+dx*t*size;zz=z+dz*t*size;yy=y+math.sin(t*2)*size*.7
            leaf=.28*size*(1-t*.6)
            for side in (-1,1):
                geo(tag,'Fern',[(xx,yy,zz),(xx-dz*side*leaf+dx*.1,yy+.1,zz+dx*side*leaf+dz*.1),(xx+dx*.22,yy+.2,zz+dz*.22)],[(0,1,2)])
for k,(x,z,y,rx,rz) in enumerate(beds):
    for i in range(24):
        a=random.random()*math.tau;rr=math.sqrt(random.random());xx=x+math.cos(a)*rx*rr;zz=z+math.sin(a)*rz*rr
        box('GardenGround','Stone',(xx,y-2.5,zz),(random.uniform(1.5,2.6),5,random.uniform(1.5,2.6)),random.uniform(-.2,.2))
        box('GardenMoss','Moss',(xx,y+.07,zz),(random.uniform(1.5,2.6),.22,random.uniform(1.5,2.6)),random.uniform(-.2,.2))
    for i in range(50):
        a=random.random()*math.tau;rr=math.sqrt(random.random());xx=x+math.cos(a)*rx*rr;zz=z+math.sin(a)*rz*rr
        fern('GardenFerns',xx,y+.2,zz,random.uniform(.65,1.3))
        if i%3==0:
            for j in range(3):
                xx2=xx+random.uniform(-.3,.3);zz2=zz+random.uniform(-.3,.3)
                beam('FlowerStems','LeafDark',(xx2,y,zz2),(xx2,y+.7,zz2),.04)
                for q in range(4):box('GardenFlowers','Flower',(xx2+.12*math.cos(q*math.pi/2),y+.7,zz2+.12*math.sin(q*math.pi/2)),(.19,.1,.19),q*.4)

# Larger individual umbrella profiles, with shaded gills and discrete luminous spots.
for i in range(47):
    bx,bz,by,rx,rz=beds[i%len(beds)];x=bx+random.uniform(-rx*.65,rx*.65);z=bz+random.uniform(-rz*.65,rz*.65);y=by+.2
    h=random.uniform(.7,1.7);r=h*random.uniform(.55,.8)
    if i in (6,14,22):h*=1.4;r*=1.5
    cone('MushroomNewStem','Stem',(x,y+h*.5,z),.13,.09,h,9)
    profiles=[(r*.1,y+h+r*.52),(r*.46,y+h+r*.43),(r*.79,y+h+r*.25),(r,y+h),(r*.83,y+h-r*.12),(r*.13,y+h-r*.18)]
    vs=[];fs=[];N=16
    for rad,yy in profiles:
        for j in range(N):
            a=j*math.tau/N;vs.append((x+rad*math.cos(a),yy,z+rad*math.sin(a)))
    for k in range(len(profiles)-1):
        for j in range(N):fs.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
    fs.extend([tuple(reversed(range(N))),tuple((len(profiles)-1)*N+j for j in range(N))])
    geo('Glow_MushroomNew_%02d'%i,'GlowCyan',vs,fs)
    for j in range(12):
        a=random.random()*math.tau;rr=random.uniform(.15,.88)*r;yy=y+h+r*.52*(1-(rr/r)**1.5)
        sz=random.uniform(.06,.14)*r
        box('MushroomNewSpots','Foam',(x+math.cos(a)*rr,yy+.025,z+math.sin(a)*rr),(sz,.04,sz),a)
    for j in range(12):
        a=j*math.tau/12
        beam('MushroomNewGills','Stem',(x,y+h-r*.2,z),(x+math.cos(a)*r*.83,y+h-r*.12,z+math.sin(a)*r*.83),.025)

# Broken, planted path edges and sparse moss seams interrupt the paving's glare.
for z in range(-18,71):
    width=11+max(0,z-20)*.16
    for side in (-1,1):
        x=side*(width/2+.3)
        if random.random()<.7:
            for j in range(5):box('BridgeLivingEdges',random.choice(['Moss','LeafDark','LeafMid']),(x+random.uniform(-.45,.5),random.uniform(.25,.8),z+random.uniform(-.5,.5)),(.55,.4,.65),random.random())
        if random.random()<.32:
            length=random.uniform(1.5,5)
            for j in range(int(length*2)):
                box('BridgeHangingIvy','LeafDark',(x+side*.5,-j*.5,z+random.uniform(-.4,.4)),(.5,.6,.65),random.random())
    if z%2==0 and random.random()<.65:
        x=random.choice([-1,1])*random.uniform(width*.23,width*.43)
        box('PavingMossSeams','Moss',(x,.175,z),(random.uniform(.4,1.4),.04,.1),random.uniform(-.15,.15))

# Waterfall lips join the new terraced heights without floating water slabs.
for i,(x,z,w,top,bottom) in enumerate([(-24,6,10,-.5,-5),(-38,31,8,2,-5),(-60,-30,9,8,-29),(-117,-22,8,1,-29),(-146,-43,7,2,-48)]):
    for j in range(6):
        xx=x-w/2+w*j/5
        box('FallLipRock','Stone',(xx,top-2,z-1.5),(w/5+.1,4,3))
        box('FallLipMoss','Moss',(xx,top+.04,z-2.5),(w/5+.1,.12,1.1))

# Layered carved shrine surround instead of a flat doorway.
for side in (-1,1):
    x=3+side*3.7
    for j in range(7):
        box('ShrineMasonry','StoneLight',(x,4.1+j*1.3,-29.8),(1.15,1.22,1.3))
    box('ShrinePlinth','StoneLight',(x,3.55,-29.7),(1.7,.6,1.8))
    box('ShrineCapital','StoneLight',(x,13.1,-29.7),(1.7,.5,1.8))
    cone('ShrineFinial','StoneLight',(x,14.1,-29.7),.55,.06,1.5,4)
arch('ShrineOuterCarving','Stone',3,3.8,-29.8,5.9,11.1,.6,.35)
for j in range(9):
    a=math.pi*j/8
    box('ShrineGoldStuds','Brass',(3+3.05*math.cos(a),11.6+3.05*math.sin(a),-29.43),(.23,.35,.15),a)
for i in range(7):
    x=3+random.uniform(-1.3,1.3);z=-29.2+random.uniform(-.5,.3);h=random.uniform(.25,.7)
    box('ShrineCandles','StoneLight',(x,3.9+h/2,z),(.16,h,.16))
    cone('CandleFlames','GlowAmber',(x,3.9+h+.1,z),.08,.01,.22,6)

objects=[]
for (name,mat),(vs,fs) in groups.items():
    for offset in range(0,len(fs),6000):
        remap={};cv=[];cf=[]
        for face in fs[offset:offset+6000]:
            f=[]
            for vi in face:
                if vi not in remap:remap[vi]=len(cv);cv.append(vs[vi])
                f.append(remap[vi])
            cf.append(f)
        me=bpy.data.meshes.new(name);me.from_pydata(cv,[],cf);me.update()
        o=bpy.data.objects.new(name+('_%d'%(offset//6000)if offset else '')+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
        uv=me.uv_layers.new(name='UVMap')
        for p in me.polygons:
            n=p.normal;axes=(0,1)if abs(n.z)>.5 else ((0,2)if abs(n.y)>.5 else (1,2))
            for li in p.loop_indices:
                co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.18,co[axes[1]]*.18)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_DepthGarden4.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_DepthGarden4.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'objects':len(objects),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
