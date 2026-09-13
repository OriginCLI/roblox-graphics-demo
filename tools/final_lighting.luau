local world=workspace.DreamWorld
local L=game:GetService('Lighting')
L.Ambient=Color3.fromRGB(40,51,43)
L.OutdoorAmbient=Color3.fromRGB(93,108,92)
L.ExposureCompensation=.06
local atmosphere=L:FindFirstChildOfClass('Atmosphere')
if atmosphere then atmosphere.Density=.34;atmosphere.Haze=2.4;atmosphere.Glare=.42 end
local foliage={LeafDark=Color3.fromRGB(30,68,49),LeafMid=Color3.fromRGB(45,91,57),LeafLight=Color3.fromRGB(73,118,67),LeafGold=Color3.fromRGB(107,129,60)}
for _,p in world:GetDescendants() do
 if p:IsA('MeshPart') then
  local material=p.Name:match('__(%w+)$')
  if foliage[material] and p.TextureID=='' then p.Color=foliage[material] end
  if material=='GlowCyan' then
   for _,l in p:GetChildren() do if l:IsA('PointLight') then l.Brightness=.22;l.Range=6 end end
  end
 end
end
return 'Final lighting and foliage palette applied'
