"""Second structural iteration: camera-projected landmarks and layered ledges.
Runs through Blender MCP and preserves the previous authored scene.
"""
from pathlib import Path
ROOT=Path(r'C:\Dev\RobloxGraphicDemo')
s=(ROOT/'tools/extension/build_reworked.py').read_text()
s=s.replace("scene.name='Lumenwild_Reworked'","scene.name='Lumenwild_Stage2'")
s=s.replace("'Lumenwild_Reworked.blend'","'Lumenwild_Stage2.blend'").replace("'Lumenwild_Reworked.glb'","'Lumenwild_Stage2.glb'")
s=s.replace('Lumenwild_Reworked.blend','Lumenwild_Stage2.blend').replace('Lumenwild_Reworked.glb','Lumenwild_Stage2.glb')
s=s.replace('11+max(0,z-25)*.085','11+max(0,z-20)*.16')
start=s.index('# Connected escarpments.')
end=s.index('# Monumental asymmetric tree')
terrain=r'''
# Deliberate asymmetric land masses at several elevations; distant banks overlap.
lands=[
 ('Hero',7,-38,27,25,1,-27),('LeftNear',-49,32,15,14,2,-30),
 ('LeftMid',-92,9,19,22,4,-48),('Central',-65,-21,13,12,-3,-48),
 ('UpperCentral',-60,-42,13,13,8,-49),('FallTerrace',-25,-6,11,13,-1,-28),
 ('RightNear',35,-6,17,25,-2,-29),('ForegroundRight',25,44,22,21,-4,-30),
 ('ForegroundLeft',-28,64,24,19,-5,-30),('FarLeft',-116,-36,24,19,1,-61),
 ('Castle',-149,-66,30,27,2,-67),('FarRight',-77,-92,24,24,8,-64),
 ('RightBack',44,-78,25,32,4,-45),('VeryFar',-180,-110,43,31,8,-73),
 ('NearRockA',-19,27,4,4,-5,-20),('NearRockB',-33,38,3,3,-4,-22),
]
def height(x,z):
    l=min(lands,key=lambda l:((x-l[1])/l[3])**2+((z-l[2])/l[4])**2)
    return l[5]
def riverx(z):return -38
def width(z):return 15
for tag,x,z,rx,rz,top,bottom in lands:
    step=1.65 if tag in ('Hero','LeftNear','FallTerrace','RightNear','ForegroundRight','ForegroundLeft') else 2.5
    for ix in range(-int(rx/step)-1,int(rx/step)+2):
        for iz in range(-int(rz/step)-1,int(rz/step)+2):
            xx=x+ix*step;zz=z+iz*step
            angle=math.atan2((zz-z)/rz,(xx-x)/rx)
            edge=1+.1*math.sin(angle*5+rx)+.055*math.sin(angle*11)
            d=((xx-x)/rx)**2+((zz-z)/rz)**2
            if d>edge:continue
            if tag=='Hero' and -6.5<xx<6.5 and zz>-23:continue
            yy=top+random.uniform(-.5,.5)+.45*math.sin(xx*.33+zz*.16)
            # Chipped masonry-sized surface pieces; recessed strata break up cliffs.
            box('LedgeCap_'+tag,random.choice(['Stone','Stone','StoneLight']),(xx,yy-.45,zz),(step*.97,.9,step*.97),random.uniform(-.035,.035))
            if random.random()<.68:
                box('LedgeMoss_'+tag,random.choice(['Moss','Moss','MossLight']),(xx,yy+.04,zz),(step*random.uniform(.6,.97),.15,step*random.uniform(.6,.97)),random.uniform(-.08,.08))
            if d>.67:
                for k in range(7):
                    hi=yy-(yy-bottom)*k/7;lo=yy-(yy-bottom)*(k+1)/7
                    inset=random.uniform(-.22,.16)
                    box('CliffStrata_'+tag,random.choice(['Stone','Stone','CliffDark','StoneLight']),(xx+math.cos(angle)*inset,(hi+lo)/2,zz+math.sin(angle)*inset),(step*random.uniform(.84,1.05),hi-lo-.06,step*random.uniform(.84,1.05)))
                if random.random()<.32:
                    drop=random.uniform(1,7)
                    box('CliffIvy_'+tag,'LeafDark',(xx,yy-drop/2,zz),(step*.55,drop,.32),-angle)
            else:
                box('CliffCore_'+tag,'CliffDark',(xx,(yy+bottom)/2,zz),(step*1.01,yy-bottom,step*1.01))
            if random.random()<.12:
                box('LedgeRubble_'+tag,'StoneLight',(xx,yy+.4,zz),(random.uniform(.4,1),random.uniform(.4,.9),random.uniform(.4,1)),random.random()*3)

geo('Water_Near','Water',[(-69,-7,38),(-40,-7,73),(33,-7,74),(28,-7,-16),(-13,-7,-30),(-52,-7,-12)],[(0,5,4,3,2,1)])
geo('Water_Mid','Water',[(-140,-29,-77),(-134,-29,14),(-45,-29,36),(-35,-29,-42),(-87,-29,-109)],[(0,4,3,2,1)])
geo('Water_Far','Water',[(-240,-48,-160),(-220,-48,10),(-102,-48,-10),(-75,-48,-130)],[(0,3,2,1)])
falls=[(-24,6,10,-.5,-7),(-45,43,8,2,-7),(-60,-30,9,8,-29),(-117,-22,8,1,-29),(-146,-43,7,2,-48)]
for i,(x,z,w,top,bottom) in enumerate(falls):
    box('Water_Head_%d'%i,'Water',(x,top,z-2.6),(w,.12,5.3))
    for j in range(5):
        yy=top-(top-bottom)*j/5;ny=top-(top-bottom)*(j+1)/5
        zz=z+2*(j/5)**2;nz=z+2*((j+1)/5)**2
        geo('Fall_%d'%i,'FallVeil',[(x-w/2,yy,zz),(x+w/2,yy,zz),(x+w*.56,ny,nz),(x-w*.56,ny,nz)],[(0,1,2,3)])
    for j in range(22):
        box('Foam_%d'%i,'Foam',(x+random.uniform(-w*.55,w*.55),bottom+.08,z+random.uniform(1,5)),(random.uniform(.2,1.3),.035,random.uniform(.2,1.1)),random.random())
'''
s=s[:start]+terrain+s[end:]
# Forest trunks now occupy ledges seen around the central ravine.
s=s.replace("[(-64,-29),(-76,-66),(-55,-97),(-84,-122),(35,-73),(49,-102),(16,-119),(-105,-60),(54,9),(-57,30),(37,37),(-36,63)]","[(-49,32),(-95,7),(-114,-41),(-142,-70),(-62,-39),(-79,-88),(44,-75),(-180,-113),(39,-7),(-25,66),(25,49),(-103,-12)]")
# Transform only the modeled distant architecture, not camera or target.
pos=s.index('# Restrained bankside plants;')
adjust=r'''
for (name,mat),(vs,fs) in groups.items():
    if name.startswith('Citadel'):
        for i,p in enumerate(vs):
            x,y,z=p[0],p[2],-p[1]
            vs[i]=convert((-147+(x+65)*.65,4+(y-25)*.65,-58+(z+148)*.65))
    elif name.startswith('DistantBridge'):
        for i,p in enumerate(vs):
            x,y,z=p[0],p[2],-p[1]
            vs[i]=convert((-82+(x+58.5)*.85,6+(y-26.2)*.85,-23+(z+101)*.85))

# Bark relief follows the trunk surface, breaking its smooth cylinder outline.
for i in range(650):
    y=random.uniform(1,39);a=random.random()*math.tau
    if y<13:cx=4-3*y/13;cz=-41+2*y/13;r=9.3-1.8*y/13
    elif y<29:cx=1-3*(y-13)/16;cz=-39-(y-13)/16;r=7.5-1.7*(y-13)/16
    else:cx=-2+8*(y-29)/16;cz=-40-3*(y-29)/16;r=5.8-(y-29)/16
    x=cx+math.cos(a)*r;z=cz+math.sin(a)*r
    box('HeroBarkRelief',random.choice(['Bark','Bark','BarkLight']),(x,y,z),(random.uniform(.45,1.1),random.uniform(.8,2.3),.45),-a+math.pi/2)
for tag,x,z,rx,rz,top,bottom in lands[:9]:
    for i in range(85):
        a=random.random()*math.tau;rr=random.uniform(.6,1)
        xx=x+math.cos(a)*rx*rr;zz=z+math.sin(a)*rz*rr
        if -6.5<xx<6.5 and zz>-23:continue
        for j in range(3):
            box('LedgeLeafClumps_'+tag,random.choice(['LeafMid','LeafDark','Moss']),(xx+random.uniform(-.4,.4),top+random.uniform(.2,1.2),zz+random.uniform(-.4,.4)),(.65,.45,.65),random.random()*3)
'''
s=s[:pos]+adjust+s[pos:]
exec(compile(s,'stage2-generated-from-build_reworked.py','exec'))
