"""Broken bridge masonry, broad leaf plants and larger luminous mushrooms. Blender MCP."""
import bpy,math,random,contextlib,io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
exec((ROOT/'tools/build_forest.py').read_text().split('# Walkable continuous')[0])
scene.name='Lumenwild_Foreground7';random.seed(719)
old=bpy.data.scenes['Lumenwild_Stage2']
for o in old.objects:
 if '__' in o.name and o.data.materials:materials[o.name.split('__')[-1].split('.')[0]]=o.data.materials[0]

for z in range(-18,73,10):
 width=11+max(0,z-20)*.16
 for side in [-1,1]:
    x=side*(width/2+.4);h=random.uniform(2.1,3.2)
    for j in range(4):
      box('BridgePier7',random.choice(['Stone','StoneLight']),(x,((j+.5)/4)*h,z),(1.8+random.uniform(-.1,.1),h/4-.055,1.9),random.uniform(-.04,.04))
    box('BridgeCapital7','StoneLight',(x,h+.13,z),(2.15,.32,2.2))
    for k in range(12):
      xx=x+random.uniform(-.9,.9);zz=z+random.uniform(-.9,.9)
      box('BridgePierMoss7','Moss',(xx,h+.34,zz),(random.uniform(.25,.65),.13,random.uniform(.25,.65)),random.random())
    for k in range(7):
      yy=random.uniform(.4,h);box('BridgePierIvy7','LeafDark',(x+side*1,yy,z+random.uniform(-.8,.8)),(.45,.7,.55),random.random())
    for zz in [z+2.3,z+4.2,z+6.1]:
      if random.random()<.25:continue
      box('BrokenWall7','Stone',(x,.65,zz),(1.15,1.3,1.82),random.uniform(-.05,.05))
      box('BrokenWallMoss7','Moss',(x,.65+ .7,zz),(1.2,.15,1.65),random.uniform(-.05,.05))

def broadleaf(tag,x,y,z,size):
 for k in range(random.randint(5,8)):
    a=k*2.4+random.uniform(-.3,.3);dx,dz=math.cos(a),math.sin(a);L=size*random.uniform(.75,1.3)
    vs=[]
    for j in range(6):
      t=j/5;w=math.sin(t*math.pi)**.7*L*.22;xx=x+dx*L*t;zz=z+dz*L*t;yy=y+L*(.7*math.sin(t*1.8)+.2*t)
      vs.extend([(xx-dz*w,yy-.07,zz+dx*w),(xx,yy+.06,zz),(xx+dz*w,yy-.07,zz-dx*w)])
    fs=[]
    for j in range(5):
      for q in range(2):fs.append((j*3+q,j*3+q+1,(j+1)*3+q+1,(j+1)*3+q))
    geo(tag,random.choice(['LeafDark','LeafMid','Fern']),vs,fs)

beds=[(-8,24,-.4,3.6,5),(8,23,-.4,3.1,5),(-8,41,-.4,3.7,6),(-45,18,2.2,5,5),(-48,-20,4.2,5,5),(-8,-22,.7,4,5),(12,-25,.7,5,5),(19,-23,.8,5,6)]
for k,(x,z,y,rx,rz)in enumerate(beds):
 for i in range(30):
    a=random.random()*math.tau;r=math.sqrt(random.random());xx=x+math.cos(a)*rx*r;zz=z+math.sin(a)*rz*r
    broadleaf('BroadLeafGarden7',xx,y,zz,random.uniform(.65,1.5))
    if i%2==0:
      for j in range(3):
        xx2=xx+random.uniform(-.6,.6);zz2=zz+random.uniform(-.6,.6);h=random.uniform(.5,1.1)
        beam('Flowers7Stem','LeafDark',(xx2,y,zz2),(xx2,y+h,zz2),.055)
        for q in range(5):
          a=q*math.tau/5;box('PurpleFlowers7','Flower',(xx2+math.cos(a)*.2,y+h,zz2+math.sin(a)*.2),(.25,.12,.25),a)

# Larger, deliberately spaced hero mushroom groups on existing ground beds.
for i,(x,y,z,h,r)in enumerate([(18,.9,-22,2.3,1.85),(20,.9,-24,1.3,.9),(16,.9,-21,1.4,1.0),(11,.8,-25,1.9,1.3),(-7,.8,-23,2,1.4),(-9,.8,-22,1.2,.8),(-44,2.3,19,2.1,1.55),(-46,2.3,18,1.4,.9),(8,-.3,24,1.5,1.15),(-8,-.3,24,1.7,1.2)]):
 cone('HeroMushroomStem7','Stem',(x,y+h*.5,z),.15,.1,h,10)
 profiles=[(.08,.58),(.4,.49),(.72,.29),(1,0),(.97,-.08),(.78,-.16),(.12,-.22)]
 vs=[];fs=[];N=24
 for rad,dy in profiles:
  for j in range(N):
   a=j*math.tau/N;vs.append((x+rad*r*math.cos(a),y+h+dy*r,z+rad*r*math.sin(a)))
 for k in range(len(profiles)-1):
  for j in range(N):fs.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
 fs.extend([tuple(reversed(range(N))),tuple((len(profiles)-1)*N+j for j in range(N))])
 geo('Glow_MushroomHero7_%d'%i,'GlowCyan',vs,fs)
 for j in range(20):
  a=random.random()*math.tau;rr=random.uniform(.18,.83);sz=random.uniform(.075,.14)*r;yy=y+h+r*(.58*(1-rr**1.55))
  box('MushroomHeroSpots7','Foam',(x+math.cos(a)*rr*r,yy+.035,z+math.sin(a)*rr*r),(sz,.05,sz),a)

# Ragged leafy overhangs hide the remaining exposed modular bank edges.
for cx,cy,cz,rx,rz in [(-25,-1,-6,11,13),(-49,2,32,15,14),(35,-2,-6,17,25),(-65,-3,-21,12,11),(-60,8,-42,13,13)]:
 for i in range(130):
  a=random.random()*math.tau;rr=random.uniform(.53,.87);x=cx+math.cos(a)*rx*rr;z=cz+math.sin(a)*rz*rr
  drop=max(0,math.floor((rr-.48)*6))*2.3;y=cy-drop+.65*math.sin(x*.23+z*.14)+.35*math.cos(z*.5)
  broadleaf('BankBroadLeaves7',x,y+.3,z,random.uniform(.7,1.7))
  if i%3==0:
   for j in range(random.randint(3,8)):box('BankDrape7','LeafDark',(x,y-j*.55,z),(.8,.65,.85),random.random())

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
  me=bpy.data.meshes.new(name);me.from_pydata(cv,[],cf);me.update();o=bpy.data.objects.new(name+('_%d'%(offset//5000)if offset else '')+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
  uv=me.uv_layers.new(name='UVMap')
  for p in me.polygons:
   n=p.normal;axes=(0,1)if abs(n.z)>.5 else ((0,2)if abs(n.y)>.5 else (1,2))
   for li in p.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.14,co[axes[1]]*.14)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_Foreground7.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_Foreground7.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'meshes':len(objects),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
