import bpy
from mathutils import Vector
scene=bpy.data.scenes['Lumenwild_Stage2']
if not scene.get('Stage2LayoutAdjusted'):
    for o in scene.objects:
        n=o.name;delta=(0,0,0)
        if 'HeroLeft' in n:delta=(-7,-6,0)
        elif 'HeroRight' in n:delta=(0,-12,0)
        elif 'Forest_10__' in n:delta=(23,0,-20)
        elif n.startswith('Citadel'):delta=(0,-8,0)
        elif n.startswith(('Fall_1__','Foam_1__','Water_Head_1__')):delta=(7,0,-12)
        o.location+=Vector((delta[0],-delta[2],delta[1]))
    scene['Stage2LayoutAdjusted']=True
result={'scene':scene.name,'adjusted':bool(scene.get('Stage2LayoutAdjusted'))}
