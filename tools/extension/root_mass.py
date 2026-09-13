"""Grounded, unified voxel tree replacement plus material data swatches.
Run in Blender MCP. Prior tree and scene remain preserved in Lumenwild_Stage2.
"""
import bpy, math, random, contextlib, io
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
src=(ROOT/'tools/extension/build_reworked.py').read_text()
base=(ROOT/'tools/build_forest.py').read_text()
exec(base.split('# Walkable continuous')[0])
scene.name='Lumenwild_TreePatch2'
old=bpy.data.scenes['Lumenwild_Stage2']
for o in old.objects:
    if '__' in o.name and o.data.materials:
        materials[o.name.split('__')[-1].split('.')[0]]=o.data.materials[0]
exec(src[src.index('def tube('):src.index('def arch(')])
random.seed(883)
for o in old.objects:
    if o.name.startswith(('HeroTrunk__','HeroBranch__')):
        key=('HeroTreeUnified','Bark');g=groups.setdefault(key,[[],[]]);off=len(g[0])
        g[0].extend(tuple(v.co)for v in o.data.vertices)
        g[1].extend(tuple(off+i for i in p.vertices)for p in o.data.polygons)
roots=[
 ([(-3,14,-36),(-9,6,-30),(-13,2,-23),(-18,-.5,-14)],[4.3,3.3,2.5,.7]),
 ([(8,20,-41),(14,9,-33),(20,3,-25),(26,0,-21)],[4.5,3.8,3,1.3]),
 ([(8,9,-44),(18,4,-44),(27,1,-36),(32,0,-29)],[4.6,3.6,2.5,.9]),
 ([(6,9,-34),(10,5,-29),(13,2,-24),(16,.3,-20)],[2.8,2.4,1.7,.7]),
 ([(-3,8,-33),(-3,4,-29),(-7,1,-25),(-10,.3,-21)],[2.8,2.4,1.7,.7]),
 ([(-5,12,-44),(-13,5,-45),(-21,2,-45),(-26,.3,-39)],[4.0,3.4,2.2,.9]),
]
for ps,rs in roots:tube('HeroTreeUnified','Bark',ps,rs,14,10)
tube('HeroTreeUnified','Bark',[(-9,1,-43),(-15,12,-41),(-20,22,-38),(-30,30,-34)],[4,3.4,2.6,.9],12,10)
tube('HeroTreeUnified','Bark',[(-20,22,-38),(-29,26,-28),(-39,29,-22)],[2.7,1.7,.5],11,8)
# Broader grounding mound joins the left buttresses to the shrine terrace.
for x in range(-19,-4,2):
    for z in range(-32,-15,2):
        d=((x+11)/9)**2+((z+25)/11)**2
        if d<1:
            y=.7+1.2*(1-d)
            box('RootBed','Stone',(x,y-2,z),(2.05,4,2.05))
            box('RootBedMoss','Moss',(x,y+.1,z),(2,.22,2))

objects=[]
for (name,mat),(vs,fs) in list(groups.items()):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
tree=next(o for o in objects if o.name.startswith('HeroTreeUnified'))
bpy.ops.object.select_all(action='DESELECT');tree.select_set(True);bpy.context.view_layer.objects.active=tree
mod=tree.modifiers.new('Unified block-cut bark','REMESH');mod.mode='BLOCKS';mod.octree_depth=8;mod.scale=.94;mod.use_remove_disconnected=False;mod.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=mod.name)
tree.data.update()
# Small top-facing moss growth follows the actual remeshed surface.
groups={}
faces=[p for p in tree.data.polygons if p.normal.z>.25 and p.center.z<30]
for p in random.sample(faces,min(2200,len(faces))):
    co=p.center+p.normal*.14;x,y,z=co.x,co.z,-co.y
    size=random.uniform(.28,.8)
    box('TreeSurfaceMoss',random.choice(['Moss','Moss','LeafDark']),(x,y+.08,z),(size,.2,size),random.random()*3)
    if random.random()<.17:box('TreeLeafSprigs','LeafMid',(x,y+.32,z),(size*.7,.35,size*.7),random.random()*3)
for (name,mat),(vs,fs) in groups.items():
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name+'__'+mat,me);scene.collection.objects.link(o);me.materials.append(materials[mat]);objects.append(o)
# Retain the unified source, but partition export meshes below 15,000 triangles.
cells={}
for p in tree.data.polygons:
    key=tuple(math.floor(v/12) for v in p.center)
    cells.setdefault(key,[]).append(p)
objects.remove(tree)
chunkIndex=0
for polys in cells.values():
    for offset in range(0,len(polys),7000):
        vs=[];fs=[];remap={}
        for p in polys[offset:offset+7000]:
            f=[]
            for vi in p.vertices:
                if vi not in remap:remap[vi]=len(vs);vs.append(tuple(tree.data.vertices[vi].co))
                f.append(remap[vi])
            fs.append(tuple(f))
        me=bpy.data.meshes.new('TreeChunk');me.from_pydata(vs,[],fs);me.update()
        o=bpy.data.objects.new('HeroTreeUnified_%03d__Bark'%chunkIndex,me);scene.collection.objects.link(o);me.materials.append(materials['Bark']);objects.append(o);chunkIndex+=1
tree.name='SOURCE_UnifiedTree_NotExported';tree.hide_render=True;tree.hide_set(True)
for o in objects:
    me=o.data;uv=me.uv_layers.new(name='UVMap')
    for p in me.polygons:
        n=p.normal;axes=(0,1) if abs(n.z)>.5 else ((0,2) if abs(n.y)>.5 else (1,2))
        for li in p.loop_indices:
            co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*.22,co[axes[1]]*.22)
    o['source']='Blender MCP grounded voxel tree iteration'
for original in bpy.data.scenes['Lumenwild_MaterialData'].objects:
    o=original.copy();o.data=original.data.copy();scene.collection.objects.link(o);objects.append(o)
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=tree
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_TreePatch2.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_TreePatch2.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'meshes':len(objects),'treeFaces':len(tree.data.polygons),'treeVertices':len(tree.data.vertices),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons)for o in objects)}
