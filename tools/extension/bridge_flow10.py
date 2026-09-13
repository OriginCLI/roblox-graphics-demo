"""Broaden and curve the near bridge approach while preserving the comparison camera."""
import bpy,math,contextlib,io
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
source=bpy.data.scenes['Lumenwild_Assembled_90'];scene=bpy.data.scenes.new('Lumenwild_BridgeFlow10');bpy.context.window.scene=scene
prefixes=('Walkable_','ForegroundPaving5','BridgeSides','BridgeFootings','BridgeLivingEdges','BridgeHangingIvy','BridgePier','BridgeCapital','BrokenWall','Garden','FlowerStems','Flowers7Stem','PurpleFlowers7','BroadLeafGarden7','MushroomNew','Glow_MushroomNew','PathJointGrowth','PavingMossSeams')
objects=[]
for src in source.objects:
 name=src['RobloxName']
 if not name.startswith(prefixes):continue
 # Leave mesh groups wholly away from the near approach unchanged.
 if not any(-v.co.y>25 and abs(v.co.x)<18 for v in src.data.vertices):continue
 o=src.copy();o.data=src.data.copy();o.name='Flow10_'+name;scene.collection.objects.link(o);objects.append(o)
 for v in o.data.vertices:
  x,z=v.co.x,-v.co.y
  if z<=25 or abs(x)>=18:continue
  t=z-25;blend=min(1,t/8);shift=.55*t*blend;flare=1+.035*t*blend
  v.co.x=x*flare+shift
 o.data.update()
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Assets/Blender/Lumenwild_BridgeFlow10.blend'))
with contextlib.redirect_stdout(io.StringIO()):bpy.ops.export_scene.gltf(filepath=str(ROOT/'Assets/Exports/Lumenwild_BridgeFlow10.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False)
result={'meshes':len(objects),'names':[o.name for o in objects]}
