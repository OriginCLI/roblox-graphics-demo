-- Verified imported image data and supported emissive materials, applied in Edit.
local world=workspace:WaitForChild('DreamWorld')
local gray='rbxassetid://140651532164331' -- Armor_Roughness_v2.png, client preload succeeded.
local count=0
for _,p in world:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 local mat=p.Name:match('__(%w+)$')
 local sa=p:FindFirstChildOfClass('SurfaceAppearance')
 if mat=='Water' or mat=='WetSlate' or mat=='WetSlateLight' or mat=='Brass' or mat=='Armor' then
  if sa then sa.RoughnessMap=gray end
 end
 if mat=='Water' then
  p.Transparency=.36;p.Reflectance=0;p.Color=Color3.fromRGB(43,144,132)
  if sa then sa.Color=Color3.fromRGB(43,144,132);sa.MetalnessMap='';sa.NormalMap='rbxassetid://98564679456510' end
 elseif mat=='GlowCyan' then
  p.Material=Enum.Material.SmoothPlastic;p.Color=Color3.new(1,1,1)
  sa=sa or Instance.new('SurfaceAppearance');sa.Name='Bioluminescence';sa.Parent=p
  p.Color=Color3.fromRGB(51,190,191);sa.Color=Color3.fromRGB(51,190,191)
  sa.EmissiveMaskContent=Content.fromUri(gray);sa.EmissiveTint=Color3.fromRGB(49,184,184);sa.EmissiveStrength=.85
  sa.RoughnessMap=gray;count+=1
 end
end
local L=game:GetService('Lighting')
L.Brightness=3.4;L.ExposureCompensation=.08
L.Ambient=Color3.fromRGB(35,47,46);L.OutdoorAmbient=Color3.fromRGB(85,105,96)
local a=L:FindFirstChildOfClass('Atmosphere')
if a then a.Density=.29;a.Haze=1.4;a.Color=Color3.fromRGB(208,225,214);a.Decay=Color3.fromRGB(104,144,145);a.Glare=.25 end
return {emissiveCaps=count,roughness=gray}
