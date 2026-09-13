-- Run in Studio Edit after importing the Blender tree patch at scene origin.
local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:FindFirstChild('Lumenwild_TreePatch2.001') or workspace:FindFirstChild('Lumenwild_TreePatch2')
assert(patch,'Import Lumenwild_TreePatch2.glb first')
local storage=game:GetService('ServerStorage')
local archive=Instance.new('Folder');archive.Name='ExtensionTree2_Archive';archive.Parent=storage
local data=storage:FindFirstChild('MaterialData') or Instance.new('Folder');data.Name='MaterialData';data.Parent=storage
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
local removed,added=0,0
for _,p in world:GetChildren() do
 if p.Name:match('^HeroTrunk') or p.Name:match('^HeroBranch') or p.Name:match('^HeroRoots') or p.Name:match('^HeroBarkRelief') or p.Name:match('^RootMoss') or p.Name:match('^RootFingers') then p.Parent=archive;removed+=1 end
end
local ids={}
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','')
 if p.Name:match('^Data_') then ids[p.Name]=p.TextureID;p.Parent=data;continue end
 p.Anchored=true;p.CanCollide=false;p.CanQuery=false;p.CanTouch=false;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic
 local mat=p.Name:match('__(%w+)$')
 local tints={Bark=Color3.fromRGB(168,153,119),Stone=Color3.fromRGB(140,157,143),Moss=Color3.fromRGB(147,165,105),LeafDark=Color3.fromRGB(115,151,119),LeafMid=Color3.fromRGB(156,187,140)}
 p.Color=tints[mat] or Color3.new(1,1,1);p.Parent=world;added+=1
end
patch.Parent=archive
world:SetAttribute('GroundedTreePatch',true)
return {archived=removed,added=added,dataTextureIDs=ids}
