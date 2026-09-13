local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_DepthGarden4')
local archive=Instance.new('Folder');archive.Name='ExtensionGarden3_Archive';archive.Parent=game:GetService('ServerStorage')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
local removed=0
for _,p in world:GetChildren() do
 if p.Name:match('^Glow_Mushroom_') or p.Name:match('^MushroomStem') or p.Name:match('^MushroomSpots') or p.Name:match('^BankFerns') or p.Name:match('^PurpleFlowers') then p.Parent=archive;removed+=1 end
end
local added=0
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','')
 p.Anchored=true;p.CanCollide=false;p.CanQuery=false;p.CanTouch=false;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic;p.Parent=world;added+=1
end
patch.Parent=archive
-- Raise the near-left framing tree while preserving the fixed comparison camera.
if not world:GetAttribute('LeftFrameRaised') then
 for _,p in world:GetChildren() do
  if not p:IsA('MeshPart') then continue end
  if p.Name:match('Forest_0__') then p.CFrame+=Vector3.new(0,14,0)
  elseif p.Name:match('^ForestVolumeTrunk_0__') or p.Name:match('^ForestVolumeBranch_0__') then
   local f=31/17;p.Size=Vector3.new(p.Size.X,p.Size.Y*f,p.Size.Z);p.CFrame+=Vector3.new(0,(p.Position.Y-2)*(f-1),0)
  end
 end
 world:SetAttribute('LeftFrameRaised',true)
end
world:SetAttribute('GardenIteration',4)
return {removed=removed,added=added}
