-- Install Blender landscape replacement; retain all prior geometry in ServerStorage.
local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_Landscape3')
local archive=Instance.new('Folder');archive.Name='ExtensionLandscape2_Archive';archive.Parent=game:GetService('ServerStorage')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
local count=0
for _,p in world:GetChildren() do
 if p.Name:match('^Canopy_') or p.Name:match('^Vines_') or p.Name:match('^VineLeaves_') or p.Name:match('^ForestTrunk_') or p.Name:match('^ForestBranch_') or p.Name:match('^Ledge') or p.Name:match('^Cliff') or p.Name=='Water_Near__Water' then p.Parent=archive;count+=1 end
end
local added=0
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','')
 if p.Name=='WaterNear3__Water' then p.Name='Water_Near__Water' end
 p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic;p.Parent=world;added+=1
end
patch.Parent=archive
for _,p in world:GetChildren() do
 if not p:IsA('MeshPart') then continue end
 local i=p.Name:match('^Fall_(%d+)__')
 if i=='0' or i=='1' then
  local top=i=='0' and -.5 or 2
  local scale=(top+5)/(top+7)
  p.Size=Vector3.new(p.Size.X,p.Size.Y*scale,p.Size.Z)
  p.CFrame=p.CFrame+Vector3.new(0,2,0)+Vector3.new(0,(p.Position.Y+7)*(scale-1),0)
 elseif p.Name:match('^Foam_[01]__') then p.CFrame+=Vector3.new(0,2,0) end
end
world:SetAttribute('LandscapeIteration',3)
return {archived=count,added=added}
