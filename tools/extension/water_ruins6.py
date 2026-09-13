"""Modeled shallow water, continuous riverbed and open ruined masonry. Blender MCP."""
import bpy, math, random, contextlib, io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
exec((ROOT/'tools/build_forest.py').read_text().split('# Walkable continuous')[0])
scene.name='Lumenwild_WaterRuins6'; random.seed(661)
old=bpy.data.scenes['Lumenwild_Stage2']
for o in old.objects:
    if '__' in o.name and o.data.materials:materials[o.name.split('__')[-1].split('.')[0]]=o.data.materials[0]

poly=[(-70,39),(-42,79),(59,82),(40,-17),(-13,-30),(-52,-12)]
def inside(x,z):
    hit=False
    for i,(ax,az) in enumerate(poly):
        bx,bz=poly[(i+1)%len(poly)]
        if (az>z)!=(bz>z) and x<(bx-ax)*(z-az)/(bz-az)+ax:hit=not hit
    return hit
for ix in range(-70,60):
 for iz in range(-30,83):
    if not inside(ix+.5,iz+.5):continue
    points=[(ix,iz),(ix+1,iz),(ix+1,iz+1),(ix,iz+1)]
    def wave(x,z):return -5+.065*math.sin(x*1.7+z*.8)+.035*math.sin(z*2.3-x*.6)+.015*math.cos(x*4+z*3)
    geo('WaterNear6','Water',[(x,wave(x,z),z)for x,z in points],[(0,3,2,1)])
    if ix%2==0 and iz%2==0:
        y=-7.1+.25*math.sin(ix*.3)+.2*math.cos(iz*.4)
        geo('RiverBed6',random.choices(['Stone','StoneLight','Moss'],[5,3,1])[0],[(ix,y,iz),(ix+2,y+.15,iz),(ix+2,y,iz+2),(ix,y-.1,iz+2)],[(0,3,2,1)])

# Nested rock shelves establish shallow water and eroded margins beneath cascades.
for cx,cz,rx,rz,top in [(-26,8,8,5,-4.7),(-40,33,7,5,-4.6),(-26,27,5,4,-5.2),(19,10,7,8,-5.5),(-17,51,6,7,-5.4)]:
 for i in range(85):
    a=random.random()*math.tau;r=math.sqrt(random.random());x=cx+math.cos(a)*rx*r;z=cz+math.sin(a)*rz*r
    y=top-r*.8; s=random.uniform(.8,2.5)
    box('ShoalStone6',random.choice(['Stone','StoneLight']),(x,y-.5,z),(s,random.uniform(.6,1.2),s*random.uniform(.7,1.3)),random.uniform(-.3,.3))
    if y> -5 and random.random()<.25:box('ShoalMoss6','Moss',(x,y+.1,z),(s*.7,.16,s*.6),random.random())

# Open arches use individual voussoirs, so openings are genuine geometry.
def arch6(tag,cx,base,cz,rise,radius,depth,angle=0,thick=1.1):
    c,s=math.cos(angle),math.sin(angle)
    def pt(x,y,z):return (cx+x*c+z*s,y,cz-x*s+z*c)
    for side in [-1,1]:
        box(tag,'Stone',pt(side*(radius+thick*.5),base+rise*.5,0),(thick,rise,depth),angle)
    for i in range(13):
        a=math.pi*i/13;b=math.pi*(i+1)/13
        vs=[]
        for zz in [-depth/2,depth/2]:
            for rr,aa in [(radius,a),(radius,b),(radius+thick,b),(radius+thick,a)]:vs.append(pt(math.cos(aa)*rr,base+rise+math.sin(aa)*rr,zz))
        geo(tag,random.choice(['Stone','StoneLight']),vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])

# Backlit ruined abbey replaces the closed blue-roof castle silhouette.
cx,cz=-150,-67
arch6('AbbeyMain6',cx,3,cz,12,5,4,.05,1.6)
arch6('AbbeyBell6',cx,23,cz,5,2.1,3,.05,.8)
for side in [-1,1]:
    x=cx+side*12
    for level in range(10):
        box('AbbeyButtress6',random.choice(['Stone','StoneLight']),(x,4+level*2.1,cz),(3.5-level*.16,2.05,5-level*.18),.05)
    arch6('AbbeySide6',x,24,cz,3,1.1,2,.05,.65)
    cone('AbbeyPinnacle6','StoneLight',(x,32.2,cz),1.8,.08,7,8)
    box('AbbeyCrossbar6','StoneLight',(x,34.8,cz),(2.8,.3,.4))
    for j in range(5):
        box('AbbeyRubble6','Stone',(x+random.uniform(-5,5),3+random.uniform(0,1),cz+random.uniform(-5,5)),(random.uniform(1,3),random.uniform(.6,2),random.uniform(1,2)),random.random())
cone('AbbeyCentralSpire6','StoneLight',(cx,35.5,cz),2.5,.03,8,8)
for side in [-1,1]:
    beam('AbbeyFlyingButtress6','Stone',(cx+side*5.5,19,cz),(cx+side*12,24,cz),1.2)
    for j in range(15):box('AbbeyIvy6','LeafDark',(cx+side*6+random.uniform(-.5,.5),19-j*.7,cz+2.1),(.9,.8,.4),random.random())

# A second, broken aqueduct and ruined river tower overlap the middle ravine.
angle=.61; c,s=math.cos(angle),math.sin(angle)
for i in range(3):
    x=-98+i*9*c;z=31-i*9*s
    arch6('BrokenAqueduct6',x,-3,z,8,3.6,3,angle,1.2)
    box('BrokenAqueductDeck6','StoneLight',(x,9.8,z),(9.3,1.2,4.1),angle)
    for side in [-1,1]:
        for j in range(4):
            if random.random()<.3:continue
            xx=(j-1.5)*2
            box('BrokenParapet6','Stone',(x+xx*c+side*1.8*s,11,z-xx*s+side*1.8*c),(1.7,1.4,.55),angle)
for j in range(6):
    box('RuinTower6','Stone',(-73, -1+j*1.6,-12),(6-j*.15,1.5,5.5-j*.15),.1)
arch6('RuinWindow6',-73,8,-12,3,1.35,3,.1,.8)
for side in [-1,1]:box('RuinBrokenCrown6','StoneLight',(-73+side*2.6,14+side*.7,-12),(1.2,3+side,3),.1)

# Broad distant ground prevents the background trees ending in open sky.
geo('FarForestGround6','Stone',[(-400,-46,-380),(180,-46,-380),(120,-46,-85),(-240,-46,-25)],[(0,3,2,1)])

objects=[]
for (name,mat),(vs,fs)in groups.items():
    for offset in range(0,len(fs),5000):
        used={};cv=[];cf=[]
        for face in fs[offset:offset+5000]:
            f=[]
            for v in face:
                if v not in used:used[v]=len(cv);cv.append(vs[v])
                f.append(used[v])
            cf.append(f)
        me=bpy.data.meshes.new(name);me.from_pydata(cv,[],cf);me.update()
        o=bpy.data.objects.new(name+('_%d'%(offset//5000)if offset else '')+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
        if name=='WaterNear6':
            for p in me.polygons:p.use_smooth=True
            # Shared vertices across cells for continuous surface normals.
            import bmesh
            bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001);bm.to_mesh(me);bm.free();me.update()
        uv=me.uv_layers.new(name='UVMap')
        for p in me.polygons:
            n=p.normal;axes=(0,1)if abs(n.z)>.5 else ((0,2)if abs(n.y)>.5 else (1,2))
            for li in p.loop_indices:
                co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.12,co[axes[1]]*.12)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_WaterRuins6.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_WaterRuins6.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'meshes':len(objects),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
