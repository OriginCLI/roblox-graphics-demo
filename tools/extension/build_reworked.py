"""Three-hour composition rebuild. Run only through Blender 5.1 MCP.
Keeps every prior scene; all terrain, trees, buildings and actor are editable meshes.
"""
import bpy, math, random, json, io, contextlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
source=(ROOT/'tools/build_forest.py').read_text()
exec(source.split('# Walkable continuous')[0])
scene.name='Lumenwild_Reworked'
random.seed(131)
material('Flower',(.45,.19,.63),.85)
material('LeafGold',(.34,.43,.12),.9)
material('ShrineDark',(.035,.055,.045),.9)
material('CliffDark',(.13,.19,.18),.9)
material('FallVeil',(.8,.95,.93),.4)

def tube(name,mat,points,radii,sides=10,steps=8):
    ps=[Vector(p) for p in points]; vs=[]; fs=[]; centers=[]
    for k in range(len(ps)-1):
        a,b,c,d=ps[max(0,k-1)],ps[k],ps[k+1],ps[min(len(ps)-1,k+2)]
        for j in range(steps):
            t=j/steps
            p=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)
            rad=radii[k]*(1-t)+radii[k+1]*t
            centers.append((p,rad))
    centers.append((ps[-1],radii[-1]))
    for k,(p,r) in enumerate(centers):
        direction=(centers[min(k+1,len(centers)-1)][0]-centers[max(0,k-1)][0]).normalized()
        ref=Vector((0,1,0)) if abs(direction.y)<.94 else Vector((1,0,0))
        u=direction.cross(ref).normalized();v=direction.cross(u).normalized()
        for j in range(sides):
            ang=j*math.tau/sides; rr=r*(1+.09*math.sin(j*2.7+k*.43))
            vs.append(tuple(p+rr*(math.cos(ang)*u+math.sin(ang)*v)))
        if k:
            for j in range(sides):
                q=(k-1)*sides+j;n=(j+1)%sides
                fs.append((q,(k-1)*sides+n,k*sides+n,k*sides+j))
    fs.extend([tuple(reversed(range(sides))),tuple((len(centers)-1)*sides+j for j in range(sides))])
    geo(name,mat,vs,fs)
    return centers

def arch(name,mat,x,y,z,w,h,depth,th=.65):
    r=w/2
    for s in (-1,1):box(name,mat,(x+s*(r+th/2),y+(h-r)/2,z),(th,h-r,depth))
    for i in range(14):
        a=i*math.pi/14;b=(i+1)*math.pi/14
        vs=[(x+rad*math.cos(ang),y+h-r+rad*math.sin(ang),zz) for zz in (z-depth/2,z+depth/2) for rad,ang in [(r,a),(r,b),(r+th,b),(r+th,a)]]
        geo(name,mat,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])

# The same bounded walk surface, but the bridge now extends beyond the near frame.
box('Walkable_Base','WetSlate',(0,-.28,4),(11,.55,54))
for iz,z in enumerate(range(-22,71,2)):
    width=11+max(0,z-25)*.085
    for ix in range(5):
        x=(ix-2)*width/5+random.uniform(-.035,.035)
        box('Walkable_Paving' if z<=30 else 'ForegroundTrail',random.choice(['WetSlate','WetSlate','WetSlateLight']),(x,.035,z),(width/5-.1,.22,1.91),random.uniform(-.018,.018))
    for side in (-1,1):
        x=side*(width/2+.45)
        box('BridgeSides','Stone',(x,-2.25,z),(.95,4.5,1.98))
        if iz%5==0:
            box('BridgePiers','StoneLight',(x,.75,z),(1.3,1.5,1.35))
            box('BridgePierMoss','Moss',(x,1.55,z),(1.42,.16,1.43))
        elif iz%7!=3:
            box('BrokenParapets','Stone',(x,.28,z),(.85,.58,1.87))
            box('ParapetMoss','Moss',(x,.62,z),(.95,.13,1.85))
for z in (-18,-2,14,30,46,62):
    for x in (-5.7,5.7):box('BridgeFootings','Stone',(x,-10,z),(2.0,17,3.3))

# Connected escarpments. A winding deep channel replaces equal-height round islands.
def riverx(z):return -29+11*math.sin((z+30)*.022)
def width(z):return 13+3*math.sin(z*.047)
def height(x,z):
    base=1.5+max(0,-z-35)*.14
    wave=1.8*math.sin(x*.095+z*.042)+1.3*math.cos(z*.11-x*.041)
    if x<riverx(z):base+=5+max(0,-z-65)*.08
    return math.floor((base+wave)*.6)/.6

step=3.0
for xi,x in enumerate(range(-126,94,3)):
    for zi,z in enumerate(range(-174,76,3)):
        cx=riverx(z); edge=width(z)+1.8*math.sin(z*.14)
        # Main gorge and near bridge tributaries form a continuous irregular channel.
        channel=abs(x-cx)<edge
        bridgegap=(-22<z<76 and -12<x<17+4*math.sin(z*.06))
        if channel or bridgegap:continue
        top=height(x,z)
        bottom=-42 if z<-45 else -24
        # Split faces in vertical strata rather than full-height uninterrupted posts.
        for level in range(3):
            lo=bottom+(top-bottom)*level/3; hi=bottom+(top-bottom)*(level+1)/3
            inset=random.uniform(-.2,.25)
            box('RavineRock_%d_%d'%(xi//13,zi//18),random.choice(['Stone','Stone','CliffDark','StoneLight']),(x,(lo+hi)/2,z),(step+inset,hi-lo+.06,step+inset))
        if random.random()<.87:
            box('RavineMoss_%d_%d'%(xi//13,zi//18),random.choice(['Moss','Moss','MossLight']),(x,top+.1,z),(2.96,.23,2.97))
        if random.random()<.12:
            box('Rubble_%d'% (zi//20),'StoneLight',(x+random.uniform(-1,1),top+.5,z),(random.uniform(.6,1.5),random.uniform(.5,1.1),random.uniform(.6,1.6)),random.random()*3)

# Narrow water ribbons sit down inside the gorge; no exposed ocean horizon.
for tag,z0,z1,y in [('Near',-45,85,-7),('Mid',-90,-45,-21),('Far',-190,-90,-34)]:
    for z in range(z0,z1,3):
        a=riverx(z);b=riverx(z+3);w=width(z)+2
        geo('Water_'+tag,'Water',[(a-w,y,z),(a+w,y,z),(b+w,y,z+3),(b-w,y,z+3)],[(0,3,2,1)])
for z in range(-18,79,3):
    geo('Water_BridgeInlet','Water',[(-15,-7,z),(19+4*math.sin(z*.06),-7,z),(19+4*math.sin((z+3)*.06),-7,z+3),(-15,-7,z+3)],[(0,3,2,1)])

falls=[(-25,-45,18,-7,-21),(-39,-90,15,-21,-34),(-43,14,10,5,-7),(-16,-20,8,1.5,-7),(-55,-110,10,22,-34)]
for i,(x,z,w,top,bottom) in enumerate(falls):
    box('Water_Head_%d'%i,'Water',(x,top,z-3),(w,.12,6))
    # Curved mesh backing; flowing transparent VFX is attached in Studio.
    for j in range(5):
        yy=top-(top-bottom)*j/5;ny=top-(top-bottom)*(j+1)/5
        zz=z+2*(j/5)**2;nz=z+2*((j+1)/5)**2
        geo('Fall_%d'%i,'FallVeil',[(x-w/2,yy,zz),(x+w/2,yy,zz),(x+w*.56,ny,nz),(x-w*.56,ny,nz)],[(0,1,2,3)])
    for j in range(22):
        box('Foam_%d'%i,'Foam',(x+random.uniform(-w*.55,w*.55),bottom+.08,z+random.uniform(1,5)),(random.uniform(.2,1.3),.035,random.uniform(.2,1.1)),random.random())

# Monumental asymmetric tree with rounded angular growth and curved buttresses.
tube('HeroTrunk','Bark',[(4,0,-41),(1,13,-39),(-2,29,-40),(6,45,-43),(3,67,-44)],[9.3,7.5,5.8,4.8,2.2],14,10)
tube('HeroBranch','Bark',[(-1,27,-40),(-13,36,-39),(-29,39,-31),(-42,43,-28)],[5.2,4.1,2.3,.7],12)
tube('HeroBranch','Bark',[(2,32,-40),(17,39,-44),(30,43,-38),(42,48,-41)],[4.4,3.3,1.8,.5],12)
tube('HeroBranch','Bark',[(4,43,-43),(-6,52,-48),(-19,56,-44)],[3.6,2.1,.5],10)
rootpaths=[([(-2,17,-37),(-6,9,-30),(-10,3,-22),(-17,1,-13)],[3.3,3,2.2,.35]),
 ([(8,21,-40),(14,10,-32),(18,4,-23),(24,0,-14)],[3.8,3.1,2.0,.25]),
 ([(5,11,-35),(9,6,-28),(12,3,-18),(16,-1,-8)],[3.5,2.7,1.5,.2]),
 ([(-5,12,-42),(-13,6,-40),(-21,4,-35),(-27,1,-28)],[3.8,2.9,1.7,.25]),
 ([(5,10,-48),(13,5,-56),(25,4,-62),(32,5,-67)],[4,3,1.7,.2]),
 ([(-1,13,-47),(-11,7,-53),(-20,4,-61),(-27,5,-69)],[3.4,2.8,1.7,.2])]
for i,(ps,rs) in enumerate(rootpaths):
    centers=tube('HeroRoots_%d'%i,'Bark',ps,rs,11,10)
    for j,(p,r) in enumerate(centers):
        if j%2==0:
            box('RootMoss','Moss',(p.x,p.y+r*.65,p.z),(r*.8,.3,r*.8),random.random()*3)
    p=Vector(ps[-2]);q=Vector(ps[-1]);s=q+Vector((random.uniform(-4,4),-.6,6))
    tube('RootFingers','Bark',[tuple(p),tuple(q),tuple(s)],[rs[-2]*.5,.5,.06],7,7)

# Raised, enlarged shrine at the target's upper-right focal point.
box('ShrineNiche','ShrineDark',(3,8.5,-31.6),(6.5,11,.4))
arch('ShrineArch','StoneLight',3,3.7,-31.0,5.2,10.9,1.6,.9)
arch('ShrineInnerGold','Brass',3,3.95,-30.12,4.7,10,.14,.17)
for side in (-1,1):
    box('ShrinePillars','Stone',(3+side*4,8,-31),(1.4,9.3,2))
    box('ShrineCaps','Moss',(3+side*4,12.7,-31),(1.7,.3,2.2))
for k in range(10):box('ShrineSteps','StoneLight',(.3*k,.18+k*.38,-20.3-k*1.05),(9.8-k*.17,.43,2.0))
box('RuneVertical','GlowAmber',(3,9.2,-31.32),(.16,2.8,.07))
for a in (-1,1):beam('RuneBranches','GlowAmber',(3,9.6,-31.28),(3+a*.8,10.4,-31.28),.13)
for i,(x,y,z) in enumerate([(-2,6.4,-28),(7,6.3,-28),(-2.5,3,-21)]):
    box('LanternPost','Stone',(x,y/2-1,z),(.65,y-2,.65))
    box('Glow_Lantern_%d'%i,'GlowAmber',(x,y,z),(.66,1.1,.66))
    box('LanternRoof','Brass',(x,y+.7,z),(1.08,.2,1.08))
    for dx in (-.4,.4):
        for dz in (-.4,.4):box('LanternFrame','Brass',(x+dx,y,z+dz),(.075,1.25,.075))

def canopy(tag,x,y,z,r,amount=550):
    # Overlapping small irregular clumps, with thinner trailing foliage.
    for i in range(amount):
        a=random.random()*math.tau;rr=r*math.sqrt(random.random());dx=math.cos(a)*rr;dz=math.sin(a)*rr
        yy=y+2.7*(1-rr/r)+1.1*math.sin(dx*.6)+random.uniform(-1.8,1.1)
        size=random.uniform(.5,1.45)
        box('Canopy_'+tag,random.choices(['LeafDark','LeafMid','LeafLight','LeafGold'],[4,5,3,1])[0],(x+dx,yy,z+dz),(size*1.4,size*.7,size*1.2),random.uniform(-.3,.3))
    for i in range(18):
        a=random.random()*math.tau;xx=x+math.cos(a)*r*.8;zz=z+math.sin(a)*r*.8;length=random.uniform(2,7)
        tube('Vines_'+tag,'Bark',[(xx,y,zz),(xx+.2,y-length*.5,zz+.2),(xx-.3,y-length,zz+.5)],[.06,.045,.02],5,3)
        for j in range(int(length*2)):
            box('VineLeaves_'+tag,'LeafMid',(xx+random.uniform(-.35,.35),y-j*.5,zz+.3),(.55,.16,.55),random.random()*3)

canopy('HeroLeft',-25,39,-35,18,1400)
canopy('HeroRight',27,43,-39,18,1300)
canopy('HeroHigh',-4,55,-48,17,1000)
for i,(x,z) in enumerate([(-64,-29),(-76,-66),(-55,-97),(-84,-122),(35,-73),(49,-102),(16,-119),(-105,-60),(54,9),(-57,30),(37,37),(-36,63)]):
    y=height(x,z);h=random.uniform(17,25)
    tube('ForestTrunk_%d'%i,'Bark',[(x,y,z),(x-1,y+h*.6,z+1),(x+3,y+h,z-1)],[2.0,1.3,.5],9,5)
    for s in (-1,1):tube('ForestBranch_%d'%i,'Bark',[(x,y+h*.6,z),(x+s*5,y+h*.88,z+2),(x+s*9,y+h,z+4)],[1.1,.7,.15],7,4)
    canopy('Forest_%d'%i,x,y+h,z,random.uniform(9,13),450)

# Distant arched bridge and a readable ruined citadel, placed in the sunlit opening.
for i in range(6):
    x=-86+i*11
    arch('DistantBridge','StoneLight',x,13,-101,9,12,3,1.1)
    box('DistantBridgeDeck','Stone',(x,26.2,-101),(11.3,1.1,4))
for i,(x,z,h,w) in enumerate([(-74,-139,34,8),(-59,-145,43,9),(-45,-148,30,7),(-65,-159,51,8),(-83,-154,39,6)]):
    y=25
    box('CitadelTower','StoneLight',(x,y+h/2,z),(w,h,w))
    for level in (y+8,y+20,y+h-2):box('CitadelCornice','Stone',(x,level,z),(w+1.3,.8,w+1.3))
    cone('CitadelSpire','Roof',(x,y+h+6,z),w*.72,.15,12,6)
    for side in (-1,1):
        box('CitadelButtress','Stone',(x+side*(w/2+.7),y+h*.28,z),(1.4,h*.56,w*.55))
        box('CitadelWindow','ShrineDark',(x+side*w*.22,y+h*.7,z+w*.501),(w*.17,h*.18,.06))
for x in (-77,-65,-53):arch('CitadelArcade','StoneLight',x,25,-135,8,16,3,1.2)

# Restrained bankside plants; avoid uniform decorative stripes.
for i in range(850):
    x,z=random.choice([(-7,25),(8,5),(-10,-22),(13,-24),(-46,19),(-53,-20),(20,39),(-15,51)])
    x+=random.uniform(-4,4);z+=random.uniform(-7,7)
    y=.25 if -15<x<17 and z<-18 else (height(x,z) if abs(x-riverx(z))>width(z) and (x<-12 or x>17) else -1)
    for k in range(4):
        a=k*math.tau/4+random.random();h=random.uniform(.5,1.6);dx,dz=math.cos(a),math.sin(a)
        geo('BankFerns','Fern',[(x-dz*.15,y,z+dx*.15),(x+dz*.15,y,z-dx*.15),(x+dx*.8,y+h,z+dz*.8)],[(0,1,2)])
    if i%5==0:
        for j in range(3):box('PurpleFlowers','Flower',(x+random.uniform(-.3,.3),y+.6,z+random.uniform(-.3,.3)),(.25,.15,.25),random.random())
for i in range(40):
    x,z=random.choice([(-8,-22),(12,-25),(-45,18),(-48,-20),(8,23),(-8,41)])
    x+=random.uniform(-2,2);z+=random.uniform(-3,3);y=.4 if z<-18 and x>-20 else (height(x,z) if x<-30 else -.3)
    h=random.uniform(.55,1.8)
    cone('MushroomStem','Stem',(x,y+h*.5,z),.13,.1,h,7)
    cone('Glow_Mushroom_%02d'%i,'GlowCyan',(x,y+h,z),h*.75,h*.12,h*.32,10)
    for j in range(4):box('MushroomSpots','Foam',(x+random.uniform(-.25,.25)*h,y+h+h*.17,z+random.uniform(-.25,.25)*h),(.09,.025,.09))

exec(source.split('# Hero traveler, feet at origin.')[1].split('\n',1)[1].split('# Create real editable')[0])
objects=[]
for (name,mat),(vs,fs) in groups.items():
    mesh=bpy.data.meshes.new(name+'Mesh');mesh.from_pydata(vs,[],fs);mesh.update()
    o=bpy.data.objects.new(name+'__'+mat,mesh);scene.collection.objects.link(o);mesh.materials.append(materials[mat]);objects.append(o)
    uv=mesh.uv_layers.new(name='UVMap')
    for poly in mesh.polygons:
        n=poly.normal;axes=(0,1) if abs(n.z)>.5 else ((0,2) if abs(n.y)>.5 else (1,2))
        for li in poly.loop_indices:
            co=mesh.vertices[mesh.loops[li].vertex_index].co
            uv.data[li].uv=(co[axes[0]]*.22,co[axes[1]]*.22)
    o['source']='Blender 5.1 MCP';o['iteration']='extension-1'

# Reuse generated source textures, with corrected explicit roughness data.
def image_link(mn,path,inputname='Base Color',normal=False):
    im=bpy.data.images.load(str(ROOT/'Assets/Textures'/path),check_existing=True)
    if normal:im.colorspace_settings.name='Non-Color'
    nt=materials[mn].node_tree;p=nt.nodes.get('Principled BSDF');t=nt.nodes.new('ShaderNodeTexImage');t.image=im
    if normal:
        n=nt.nodes.new('ShaderNodeNormalMap');nt.links.new(t.outputs['Color'],n.inputs['Color']);nt.links.new(n.outputs['Normal'],p.inputs['Normal'])
    else:nt.links.new(t.outputs['Color'],p.inputs[inputname])
for mn in ('Stone','StoneLight','CliffDark','WetSlate','WetSlateLight'):image_link(mn,'WetBasalt_Color.png')
for mn in ('Bark','BarkLight'):image_link(mn,'AncientBark_Color.png')
for mn in ('LeafDark','LeafMid','LeafLight','LeafGold','Moss','MossLight','Fern'):image_link(mn,'ForestLeaves_Color.png')
for mn in ('WetSlate','WetSlateLight'):image_link(mn,'WetBasalt_Normal.png',normal=True)
image_link('Water','Water_Normal.png',normal=True)
for mn,rough in [('WetSlate',.22),('WetSlateLight',.25),('Water',.12),('Armor',.3),('Brass',.32)]:
    im=bpy.data.images.new(mn+'_Roughness_v2',width=8,height=8,float_buffer=True);im.colorspace_settings.name='Non-Color';im.pixels.foreach_set([rough,rough,rough,1.0]*64);im.update();im.filepath_raw=str(ROOT/'Assets/Textures'/(mn+'_Roughness_v2.png'));im.file_format='PNG';im.save()
    nt=materials[mn].node_tree;t=nt.nodes.new('ShaderNodeTexImage');t.image=im;nt.links.new(t.outputs['Color'],nt.nodes.get('Principled BSDF').inputs['Roughness'])
image_link('FallVeil','WaterfallFlow_v2.png')
nt=materials['FallVeil'].node_tree;t=next(n for n in nt.nodes if n.type=='TEX_IMAGE');nt.links.new(t.outputs['Alpha'],nt.nodes.get('Principled BSDF').inputs['Alpha']);materials['FallVeil'].surface_render_method='DITHERED'
scene.world=bpy.data.worlds.get('LumenwildSky')
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_Reworked.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_Reworked.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_animations=False,export_yup=True)
tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objects)
result={'scene':scene.name,'objects':len(objects),'triangles':tris,'falls':falls}
(ROOT/'Assets/Exports/reworked-manifest.json').write_text(json.dumps(result,indent=2))
