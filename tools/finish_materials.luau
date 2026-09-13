-- Preserve imported MeshPart.TextureID for albedo-only materials and
-- SurfaceAppearance maps for PBR materials. An empty new SurfaceAppearance
-- would hide the importer's albedo-only texture.
local world=workspace:WaitForChild('DreamWorld')
for _,p in world:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 local sa=p:FindFirstChildOfClass('SurfaceAppearance')
 if p.Name:find('__Leaf') or p.Name:find('__Moss') or p.Name:find('__Fern') then
  p.Color=Color3.fromRGB(194,208,185)
 elseif p.Name:find('__Bark') then
  p.Color=Color3.fromRGB(205,201,170)
 elseif p.Name:find('__Stone') and sa then
  sa.Color=Color3.fromRGB(173,190,173);sa.MetalnessMap='';sa.RoughnessMap=''
  p.Color=Color3.new(1,1,1)
 elseif p.Name:find('__Water') and sa then
  sa.MetalnessMap='';sa.Color=Color3.fromRGB(70,148,137)
  p.Transparency=.18;p.Material=Enum.Material.Glass
  if p.Name:find('__Waterfall') then
   sa.Color=Color3.fromRGB(164,217,202);p.Transparency=.32;p.Material=Enum.Material.SmoothPlastic
  end
 end
end
return 'Imported texture bindings preserved'
