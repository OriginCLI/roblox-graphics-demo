"""Volume-first foliage and stepped, planted ravine banks. Run via Blender MCP."""
import bpy, math, random, contextlib, io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
exec((ROOT/'tools/build_forest.py').read_text().split('# Walkable continuous')[0])
scene.name='Lumenwild_Landscape3'
old=bpy.data.scenes['Lumenwild_Stage2']
for o in old.objects:
    if '__' in o.name and o.data.materials:materials[o.name.split('__')[-1].split('.')[0]]=o.data.materials[0]
random.seed(932)
src=(ROOT/'tools/extension/build_reworked.py').read_text()
exec(src[src.index('def tube('):src.index('def arch(')])

# Exposed voxel surfaces have solid volume without overlapping interior boxes.
def voxel_surface(tag,cells,step,origin,leaf=False):
    dirs=[((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((-1,0,0),[(0,0,1),(0,1,1),(0,1,0),(0,0,0)]),((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),((0,-1,0),[(0,0,1),(0,0,0),(1,0,0),(1,0,1)]),((0,0,1),[(1,0,1),(1,1,1),(0,1,1),(0,0,1)]),((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)])]
    for cell in cells:
        ix,iy,iz=cell
        for d,face in dirs:
            if tuple(cell[k]+d[k] for k in range(3)) in cells:continue
            if leaf:mat=random.choices(['LeafDark','LeafMid','LeafLight'],[7,5,1] if d[1]<=0 else [1,5,4])[0]
            else:mat=random.choice(['Stone','Stone','CliffDark','StoneLight'])
            geo(tag,mat,[tuple(origin[k]+(cell[k]+v[k])*step for k in range(3))for v in face],[(0,1,2,3)])

def crown(tag,x,y,z,rx,ry,rz,step=1.1):
    cells=set()
    for ix in range(-math.ceil(rx/step)-1,math.ceil(rx/step)+1):
      for iy in range(-math.ceil(ry/step)-1,math.ceil(ry/step)+1):
       for iz in range(-math.ceil(rz/step)-1,math.ceil(rz/step)+1):
        dx,dy,dz=(ix+.5)*step,(iy+.5)*step,(iz+.5)*step
        noise=.1*math.sin(dx*.9+dz*.6)+.08*math.sin(dz*1.7-dy)
        if (dx/rx)**2+(dy/ry)**2+(dz/rz)**2<1+noise:cells.add((ix,iy,iz))
    voxel_surface('CanopyVolume_'+tag,cells,step,(x,y,z),True)
    # Leaf clusters and pendant vines soften silhouette in three dimensions.
    for i in range(int(rx*6)):
        a=random.random()*math.tau;rr=random.uniform(.72,1.02)
        xx=x+math.cos(a)*rx*rr;zz=z+math.sin(a)*rz*rr;yy=y-ry*.35
        for j in range(random.randint(2,5)):
            s=random.uniform(.35,.9)
            box('CanopyFringe_'+tag,random.choice(['LeafDark','LeafMid']),(xx+random.uniform(-.7,.7),yy-j*.5,zz+random.uniform(-.7,.7)),(s,.4,s),random.uniform(-.2,.2))
    for i in range(int(rx*1.2)):
        a=random.random()*math.tau;rr=random.uniform(.5,.9);xx=x+math.cos(a)*rx*rr;zz=z+math.sin(a)*rz*rr
        start=y-ry*.7;length=random.uniform(2,7)
        tube('VinesVolume_'+tag,'Bark',[(xx,start,zz),(xx+.3,start-length*.5,zz+.2),(xx-.2,start-length,zz+.5)],[.055,.04,.015],5,3)
        for j in range(int(length*2)):
            box('VineLeafVolume_'+tag,'LeafMid',(xx+random.uniform(-.25,.25),start-j*.5,zz+.3),(.4,.3,.45),random.random())

crown('HeroLeft',-36,31,-37,20,5.8,12)
crown('HeroLeftLower',-29,28,-26,11,4,8)
crown('HeroRight',29,31,-37,24,6,15)
crown('HeroHigh',-3,51,-47,19,5,13,1.3)
# Lower, overlapping mid-distance crowns leave the castle's backlit opening.
forest=[(-49,32,2,17,10),(-95,7,4,14,13),(-114,-41,1,16,12),(-142,-70,2,15,12),(-62,-39,8,12,13),(-79,-88,8,18,14),(44,-75,4,19,15),(-180,-113,8,18,18),(39,-7,-2,17,12),(-25,66,-5,14,13),(48,29,-4,16,13),(-103,-12,1,13,11)]
for i,(x,z,y,h,r) in enumerate(forest):
    tube('ForestVolumeTrunk_%d'%i,'Bark',[(x,y,z),(x-2,y+h*.55,z+1),(x+1,y+h,z)],[2.3,1.5,.6],9,6)
    for side in (-1,1):tube('ForestVolumeBranch_%d'%i,'Bark',[(x-2,y+h*.5,z),(x+side*4,y+h*.8,z+2),(x+side*7,y+h*.95,z+2)],[1.2,.8,.2],8,5)
    crown('Forest_%d'%i,x,y+h,z,r,3.7,r*.75,1.2 if i<7 else 1.5)

# Heightfield cliffs use broad terraces with varying silhouettes and exposed strata.
lands=[('Hero',7,-38,28,25,1,-27),('LeftNear',-49,32,15,14,2,-25),('LeftMid',-92,9,19,22,4,-43),('Central',-65,-21,12,11,-3,-40),('UpperCentral',-60,-42,13,13,8,-45),('FallTerrace',-25,-6,11,13,-1,-23),('RightNear',35,-6,17,25,-2,-23),('ForegroundRight',25,44,22,21,-4,-24),('ForegroundLeft',-28,64,24,19,-5,-24),('FarLeft',-116,-36,24,19,1,-56),('Castle',-149,-66,30,27,2,-62),('FarRight',-77,-92,24,24,8,-59),('RightBack',44,-78,25,32,4,-40),('VeryFar',-180,-110,43,31,8,-68)]
for tag,x,z,rx,rz,top,bottom in lands:
    step=2 if tag in ('Hero','LeftNear','FallTerrace','RightNear','ForegroundRight','ForegroundLeft') else 3
    heights={}
    for ix in range(-math.ceil(rx/step)-4,math.ceil(rx/step)+4):
      for iz in range(-math.ceil(rz/step)-4,math.ceil(rz/step)+4):
        xx=x+ix*step;zz=z+iz*step
        a=math.atan2((zz-z)/rz,(xx-x)/rx);d=math.sqrt(((xx-x)/rx)**2+((zz-z)/rz)**2)
        edge=1+.10*math.sin(a*5+rx)+.09*math.sin(a*3)
        if d>edge*1.14:continue
        if tag=='Hero' and -6.5<xx<6.5 and zz>-23:continue
        # Several differently recessed ledges, never continuous vertical columns.
        drop=max(0,math.floor((d/edge-.48)*6))*2.3
        yy=top-drop+.65*math.sin(xx*.23+zz*.14)+.35*math.cos(zz*.5)
        heights[ix,iz]=round(yy*2)/2
    for (ix,iz),yy in heights.items():
        xx=x+ix*step;zz=z+iz*step
        mat=random.choice(['Stone','Stone','StoneLight'])
        geo('TerraceTop_'+tag,mat,[(xx-step/2,yy,zz-step/2),(xx+step/2,yy,zz-step/2),(xx+step/2,yy,zz+step/2),(xx-step/2,yy,zz+step/2)],[(0,3,2,1)])
        for dx,dz,face in [(1,0,[(.5,-.5),(.5,.5)]),(-1,0,[(-.5,.5),(-.5,-.5)]),(0,1,[(.5,.5),(-.5,.5)]),(0,-1,[(-.5,-.5),(.5,-.5)])]:
            ny=heights.get((ix+dx,iz+dz),bottom)
            if ny>=yy:continue
            # Outward strata bulges interrupt the large planar cliff surfaces.
            levels=max(1,math.ceil((yy-ny)/3.2))
            for k in range(levels):
                hi=yy-(yy-ny)*k/levels;lo=yy-(yy-ny)*(k+1)/levels
                bump=0 if k==0 else .35*math.sin(k*2.1+ix*.8+iz*.7)
                p=[(xx+f[0]*step+dx*bump,h,zz+f[1]*step+dz*bump)for h in (hi,lo)for f in face]
                geo('TerraceCliff_'+tag,random.choice(['Stone','Stone','CliffDark']),p,[(0,1,3,2)])
        if random.random()<.72:
            box('TerraceMoss_'+tag,random.choice(['Moss','Moss','MossLight']),(xx,yy+.07,zz),(step*random.uniform(.7,1.03),random.uniform(.14,.3),step*random.uniform(.7,1.03)),random.uniform(-.16,.16))
        if random.random()<.28:
            for j in range(random.randint(2,5)):
                box('TerracePlants_'+tag,random.choice(['LeafDark','LeafMid','Moss']),(xx+random.uniform(-.8,.8),yy+random.uniform(.25,.7),zz+random.uniform(-.8,.8)),(random.uniform(.5,1),random.uniform(.4,.8),random.uniform(.5,1)),random.random())
        if random.random()<.16:
            box('TerraceRock_'+tag,'StoneLight',(xx,yy+.35,zz),(random.uniform(.5,1.4),random.uniform(.4,1.1),random.uniform(.6,1.6)),random.uniform(-.2,.2))
        if any(heights.get((ix+dx,iz+dz),bottom)<yy-2 for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]) and random.random()<.4:
            length=random.uniform(1,5)
            for j in range(int(length*1.7)):
                box('TerraceIvy_'+tag,'LeafDark',(xx+random.uniform(-.5,.5),yy-j*.6,zz+random.uniform(-.5,.5)),(.7,.55,.7),random.random())

# A broader, shallower near pool with visible stepping stones and submerged rock.
geo('WaterNear3','Water',[(-70,-5,39),(-42,-5,79),(59,-5,82),(40,-5,-17),(-13,-5,-30),(-52,-5,-12)],[(0,5,4,3,2,1)])
for i in range(140):
    x=random.uniform(-42,30);z=random.uniform(4,62)
    if -8<x<9:continue
    h=random.uniform(.3,1.6);y=-6.8 if i>16 else -4.8
    box('PoolBedRocks',random.choice(['Stone','StoneLight','Moss']),(x,y,z),(random.uniform(1.1,3.3),h,random.uniform(1.2,3.6)),random.uniform(-.25,.25))
    if i<=16:box('PoolRockMoss','Moss',(x,y+h/2+.06,z),(1.4,.15,1.5),random.random())

# Deliberate dark foreground corners frame the path without covering the traveler.
crown('ForegroundLeft',-19,2,43,7,2.7,6,.8)
crown('ForegroundRight',34,0,14,8,3,7,.8)

# Split geometry by material and a strict triangle limit; keep all sources editable.
objects=[]
for (name,mat),(vs,fs) in groups.items():
    for offset in range(0,len(fs),6000):
        used={};cv=[];cf=[]
        for face in fs[offset:offset+6000]:
            f=[]
            for v in face:
                if v not in used:used[v]=len(cv);cv.append(vs[v])
                f.append(used[v])
            cf.append(f)
        me=bpy.data.meshes.new(name);me.from_pydata(cv,[],cf);me.update()
        o=bpy.data.objects.new(name+('_%d'%(offset//6000) if offset else '')+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
        uv=me.uv_layers.new(name='UVMap')
        for p in me.polygons:
            n=p.normal;axes=(0,1) if abs(n.z)>.5 else ((0,2) if abs(n.y)>.5 else (1,2))
            for li in p.loop_indices:
                co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.22,co[axes[1]]*.22)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_Landscape3.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_Landscape3.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'objects':len(objects),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
