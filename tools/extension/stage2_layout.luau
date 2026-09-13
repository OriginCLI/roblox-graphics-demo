-- Scene layout transforms mirrored by stage2_layout.py in the editable Blender scene.
local world=workspace.DreamWorld
if world:GetAttribute('Stage2LayoutAdjusted') then return 'Already adjusted' end
for _,p in world:GetChildren() do
 if not p:IsA('MeshPart') then continue end
 local delta=Vector3.zero
 if p.Name:find('HeroLeft') then delta=Vector3.new(-7,-6,0)
 elseif p.Name:find('HeroRight') then delta=Vector3.new(0,-12,0)
 elseif p.Name:match('Forest_10__') then delta=Vector3.new(23,0,-20)
 elseif p.Name:find('^Citadel') then delta=Vector3.new(0,-8,0)
 elseif p.Name:match('^Fall_1__') or p.Name:match('^Foam_1__') or p.Name:match('^Water_Head_1__') then delta=Vector3.new(7,0,-12)
 end
 p.CFrame+=delta
 if p.Name:find('__WetSlate') then
  local sa=p:FindFirstChildOfClass('SurfaceAppearance')
  if sa then sa.RoughnessMap=sa.ColorMap end
 end
end
world:SetAttribute('Stage2LayoutAdjusted',true)
return 'Projected canopy, foreground, castle and waterfall placement adjusted'
