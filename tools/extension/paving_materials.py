"""Irregular beveled paving plus spatially varied roughness data. Blender MCP only."""
import bpy, math, random, contextlib, io
from pathlib import Path
import numpy as np
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
exec((ROOT/'tools/build_forest.py').read_text().split('# Walkable continuous')[0])
scene.name='Lumenwild_Paving5';random.seed(527)
old=bpy.data.scenes['Lumenwild_Stage2']
for o in old.objects:
    if '__' in o.name and o.data.materials:materials[o.name.split('__')[-1].split('.')[0]]=o.data.materials[0]
# Large, gently varying data maps avoid uniform broad specular glare.
N=512;yy,xx=np.mgrid[0:N,0:N]/N*math.tau
noise=(np.sin(xx*2+np.cos(yy*3))+.6*np.sin(yy*5+xx)+.35*np.cos(xx*7-yy*6))/1.95
data={'WaterGloss_v3':np.clip(.075+noise*.04+.015*np.sin(xx*23+yy*17),.035,.16),
      'StoneGloss_v3':np.clip(.22+noise*.23+.08*np.cos(xx*13)*np.sin(yy*17),.06,.64)}
for name,arr in data.items():
    im=bpy.data.images.new(name,width=N,height=N,float_buffer=True);im.colorspace_settings.name='Non-Color'
    rgba=np.empty((N,N,4),dtype=np.float32);rgba[:,:,:3]=arr[:,:,None];rgba[:,:,3]=1;im.pixels.foreach_set(rgba.ravel());im.update();im.filepath_raw=str(ROOT/'Assets/Textures'/(name+'.png'));im.file_format='PNG';im.save()

z=-22
while z<74:
    length=random.uniform(1.45,2.6);width=11+max(0,z-20)*.16
    count=random.choice([4,5,5,6]);weights=[random.uniform(.75,1.3)for _ in range(count)];total=sum(weights);x=-width/2
    for i,w in enumerate(weights):
        w=width*w/total
        mat=random.choices(['WetSlate','WetSlateLight'],[4,1])[0]
        box('Walkable_Paving5' if z<30 else 'ForegroundPaving5',mat,(x+w/2,random.uniform(.01,.035),z+length/2),(w-.07,.22,length-.065),random.uniform(-.013,.013));x+=w
    z+=length
# Small moss patches follow joints and edges, leaving a readable path through them.
for i in range(150):
    z=random.uniform(-18,65);width=11+max(0,z-20)*.16;side=random.choice([-1,1]);x=side*random.uniform(width*.33,width*.48)
    for j in range(random.randint(2,5)):
        s=random.uniform(.12,.45)
        box('PathJointGrowth',random.choice(['Moss','Moss','LeafDark']),(x+random.uniform(-.35,.35),.16,z+random.uniform(-.4,.4)),(s,random.uniform(.04,.12),s),random.random()*3)
objects=[]
for (name,mat),(vs,fs)in groups.items():
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    if mat.startswith('WetSlate'):
        b=o.modifiers.new('Chipped bevel catchlights','BEVEL');b.width=.035;b.segments=1;b.affect='EDGES';b.limit_method='ANGLE';b.angle_limit=.5
        bpy.ops.object.modifier_apply(modifier=b.name)
    uv=o.data.uv_layers.new(name='UVMap')
    for p in o.data.polygons:
        n=p.normal;axes=(0,1)if abs(n.z)>.5 else ((0,2)if abs(n.y)>.5 else (1,2))
        for li in p.loop_indices:
            co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.075,co[axes[1]]*.075)
for i,name in enumerate(data):
    me=bpy.data.meshes.new(name);me.from_pydata([(i*2,0,0),(i*2+1,0,0),(i*2+1,0,1),(i*2,0,1)],[],[(0,1,2,3)]);me.update()
    uv=me.uv_layers.new(name='UVMap')
    for j,p in enumerate([(0,0),(1,0),(1,1),(0,1)]):uv.data[j].uv=p
    o=bpy.data.objects.new('Data_'+name,me);scene.collection.objects.link(o);objects.append(o)
    m=bpy.data.materials.new('Data_'+name);m.use_nodes=True;nt=m.node_tree
    im=bpy.data.images.load(str(ROOT/'Assets/Textures'/(name+'.png')),check_existing=False);im.colorspace_settings.name='sRGB'
    t=nt.nodes.new('ShaderNodeTexImage');t.image=im;nt.links.new(t.outputs['Color'],nt.nodes.get('Principled BSDF').inputs['Base Color']);me.materials.append(m)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_Paving5.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_Paving5.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'meshes':len(objects),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
