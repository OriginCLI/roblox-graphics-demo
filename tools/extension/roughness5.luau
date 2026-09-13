-- These two spatial data images passed client PreloadAsync in this session.
local water='rbxassetid://116759003152394'
local stone='rbxassetid://126979061121564'
for _,p in workspace.DreamWorld:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 local mat=p.Name:match('__(%w+)$');local sa=p:FindFirstChildOfClass('SurfaceAppearance')
 if sa and (mat=='Water' or mat=='WetSlate' or mat=='WetSlateLight') then
  sa.RoughnessMap=mat=='Water' and water or stone
 end
 if mat=='Water' then
  p.Transparency=.25;p.Color=Color3.fromRGB(35,121,113)
  if sa then sa.Color=p.Color;sa.MetalnessMap='' end
 end
end
return {waterRoughness=water,stoneRoughness=stone}
