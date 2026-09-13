-- Clone imported Blender meshes at the same placements as forest_depth.py.
-- Only needed for the earlier imported revision, not the final full GLB.
local world=workspace.DreamWorld
local positions={{-95,-65,0},{-98,-28,-8},{-80,-102,6},{-57,-113,2},{-125,-72,10},{-126,-24,-3},{-91,14,-12},{-68,33,-15},{72,-55,-7},{63,-100,3}}
local sources={}
for _,p in world:GetChildren() do
 if p:IsA('MeshPart') and (p.Name:match('^Island_FarLeft__') or p.Name:match('^IslandMoss_FarLeft__') or p.Name:match('^LedgeRubble_FarLeft__') or p.Name:match('^Trunk_03__') or p.Name:match('^Canopy_03__') or p.Name:match('^Vines_03__') or p.Name:match('^VineLeaves_03__')) then table.insert(sources,p) end
end
local count=0
for i,pos in positions do
 for _,source in sources do
  local name=string.format('Depth_%02d_',i-1)..source.Name
  if not world:FindFirstChild(name) then
   local p=source:Clone();p.Name=name;p.CFrame+=Vector3.new(pos[1]+56,pos[3],pos[2]+72);p.Parent=world;count+=1
  end
 end
end
return count
