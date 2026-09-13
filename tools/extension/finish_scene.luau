-- Material and lighting pass for Lumenwild_Reworked, after configure_studio.luau.
local world=workspace:WaitForChild('DreamWorld')
local Lighting=game:GetService('Lighting')
for _,p in world:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 local mat=p.Name:match('__(%w+)$')
 local sa=p:FindFirstChildOfClass('SurfaceAppearance')
 if mat and (mat:find('Leaf') or mat:find('Moss') or mat=='Fern') then
  local tints={LeafDark=Color3.fromRGB(115,151,119),LeafMid=Color3.fromRGB(156,187,140),LeafLight=Color3.fromRGB(191,211,150),LeafGold=Color3.fromRGB(211,207,140),Moss=Color3.fromRGB(147,165,105),MossLight=Color3.fromRGB(183,196,120),Fern=Color3.fromRGB(159,194,148)}
  p.Color=tints[mat] or Color3.new(1,1,1)
 elseif mat=='Bark' or mat=='BarkLight' then
  p.Color=Color3.fromRGB(168,153,119)
 elseif mat=='Stone' or mat=='StoneLight' or mat=='CliffDark' then
  p.Color=mat=='CliffDark' and Color3.fromRGB(96,119,111) or (mat=='StoneLight' and Color3.fromRGB(191,196,177) or Color3.fromRGB(140,157,143))
 elseif mat=='WetSlate' or mat=='WetSlateLight' then
  p.Color=Color3.new(1,1,1);p.Reflectance=0
  if sa then sa.Color=Color3.fromRGB(188,196,188);sa.MetalnessMap='' end
 elseif mat=='Water' then
  p.Color=Color3.fromRGB(47,124,121);p.Transparency=.22;p.Reflectance=.12;p.CastShadow=false
  if sa then sa.Color=Color3.fromRGB(47,124,121);sa.MetalnessMap='' end
 elseif mat=='FallVeil' then
  p.Color=Color3.fromRGB(214,241,234);p.Material=Enum.Material.SmoothPlastic;p.Transparency=.3;p.CastShadow=false
  if sa then sa.AlphaMode=Enum.AlphaMode.Transparency;sa.Color=Color3.fromRGB(210,239,234);sa.MetalnessMap='' end
 elseif mat=='Foam' then
  p.Material=Enum.Material.SmoothPlastic;p.Color=Color3.fromRGB(191,221,212);p.Transparency=.55;p.CastShadow=false
 elseif mat=='GlowCyan' then
  p.Color=Color3.fromRGB(54,191,199)
 end
 for _,l in p:GetChildren() do
  if l:IsA('PointLight') then
   if mat=='GlowCyan' then l.Brightness=.25;l.Range=7 else l.Brightness=2.2;l.Range=16;l.Color=Color3.fromRGB(255,181,89) end
  end
 end
end
Lighting.ClockTime=15.5
Lighting.GeographicLatitude=-35
Lighting.Brightness=4
Lighting.Ambient=Color3.fromRGB(29,38,39)
Lighting.OutdoorAmbient=Color3.fromRGB(80,96,88)
Lighting.EnvironmentDiffuseScale=.55
Lighting.EnvironmentSpecularScale=1
Lighting.ExposureCompensation=.12
Lighting.ColorShift_Top=Color3.fromRGB(255,209,138)
Lighting.ShadowSoftness=.22
local a=Lighting:FindFirstChildOfClass('Atmosphere')
a.Density=.31;a.Offset=.05;a.Haze=1.8;a.Glare=.45
a.Color=Color3.fromRGB(230,222,197);a.Decay=Color3.fromRGB(127,158,151)
local grade=Lighting:FindFirstChild('ForestGrade')
grade.TintColor=Color3.fromRGB(255,250,240);grade.Saturation=.03;grade.Contrast=.14
return 'Reworked material bindings and directional lighting configured'
