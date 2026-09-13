-- Placement equivalent of align_waterfalls.py for the already imported scene.
local offsets = {Vector3.new(0,0,5.5),Vector3.new(0,0,6),Vector3.new(19,0,19),Vector3.new(0,0,6.5),Vector3.new(0,0,7.5)}
local changed = {}
for _,p in workspace.DreamWorld:GetDescendants() do
 if p:IsA('MeshPart') then
  local index = p.Name:match('^Water_Head_(%d+)__') or p.Name:match('^Fall_(%d+)__') or p.Name:match('^Foam_(%d+)__')
  if index and not p:GetAttribute('LipAligned') then
   p.CFrame += offsets[tonumber(index)+1]
   p:SetAttribute('LipAligned',true)
   table.insert(changed,p.Name)
  end
 end
end
return changed
