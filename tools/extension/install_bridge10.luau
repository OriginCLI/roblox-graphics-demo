local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_BridgeFlow10')
local archive=Instance.new('Folder');archive.Name='ExtensionBridge9_Archive';archive.Parent=game:GetService('ServerStorage')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
local n=0;local missing={}
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 local name=p.Parent.Name:gsub('%.%d+$',''):gsub('^Flow10_','');local old=world:FindFirstChild(name)
 if not old then table.insert(missing,name);continue end
 p.Name=name;p.Anchored=true;p.CanCollide=old.CanCollide;p.CanTouch=old.CanTouch;p.CanQuery=old.CanQuery;p.DoubleSided=old.DoubleSided;p.RenderFidelity=old.RenderFidelity
 p.Color=old.Color;p.Material=old.Material;p.Transparency=old.Transparency;p.Reflectance=old.Reflectance;p.CastShadow=old.CastShadow;p.TextureID=old.TextureID
 for key,value in old:GetAttributes() do p:SetAttribute(key,value) end
 for _,c in p:GetChildren() do if c:IsA('SurfaceAppearance') then c:Destroy() end end
 for _,c in old:GetChildren() do if c:IsA('SurfaceAppearance') or c:IsA('Light') then c:Clone().Parent=p end end
 old.Parent=archive;p.Parent=world;n+=1
end
patch.Parent=archive;world:SetAttribute('BridgeFlowIteration',10)
return {replaced=n,missing=missing}
