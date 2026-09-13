-- Sun direction was evaluated in the client against the desired water reflection.
local L=game:GetService('Lighting')
L.ClockTime=15.4;L.GeographicLatitude=-2;L.Brightness=3.6;L.ExposureCompensation=.05
local a=L:FindFirstChildOfClass('Atmosphere')
a.Density=.32;a.Offset=0;a.Haze=1.2;a.Color=Color3.fromRGB(226,228,211);a.Decay=Color3.fromRGB(165,195,183)
for _,p in workspace.DreamWorld:GetChildren() do
 if not p:IsA('MeshPart') then continue end
 if p.Name:find('DistantRidge') then
  local n=tonumber(p.Name:match('Ridge_(%d)'))
  p.Material=Enum.Material.SmoothPlastic;p.TextureID='';p.Color=Color3.fromRGB(165,181,169);p.Transparency=.35+n*.1;p.CastShadow=false
  if not p:GetAttribute('DepthLowered') then p.CFrame-=Vector3.new(0,32,0);p:SetAttribute('DepthLowered',true) end
 elseif p.Name:find('DeepForest') then
  p.Transparency=.3;p.CastShadow=false
  if not p:GetAttribute('DepthLowered') then p.CFrame-=Vector3.new(0,45,0);p:SetAttribute('DepthLowered',true) end
 end
end
return 'Refined sun direction and distant atmosphere'
