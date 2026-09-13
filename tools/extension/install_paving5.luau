local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_Paving5')
local storage=game:GetService('ServerStorage')
local archive=Instance.new('Folder');archive.Name='ExtensionPaving4_Archive';archive.Parent=storage
local data=storage:WaitForChild('MaterialData')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
for _,p in world:GetChildren() do if p.Name:match('^Walkable_Paving__') or p.Name:match('^ForegroundTrail__') then p.Parent=archive end end
local ids={};local n=0
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','')
 if p.Name:match('^Data_') then ids[p.Name]=p.TextureID;p.Parent=data;continue end
 p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=p.Name:match('^Walkable_')~=nil;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic;p.Parent=world;n+=1
 p:SetAttribute('Walkable',p.CanQuery)
 local sa=p:FindFirstChildOfClass('SurfaceAppearance')
 if sa then sa.RoughnessMap='rbxassetid://140651532164331';sa.MetalnessMap='';sa.Color=Color3.fromRGB(188,196,188) end
end
patch.Parent=archive;world:SetAttribute('PavingIteration',5)
return {added=n,dataTextureIDs=ids}
