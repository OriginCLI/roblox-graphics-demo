local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_CanopyWild9')
local archive=Instance.new('Folder');archive.Name='ExtensionCanopy8_Archive';archive.Parent=game:GetService('ServerStorage')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
for _,p in world:GetChildren() do if p.Name:match('^CanopyVolume_') or p.Name:match('^CanopyFringe_') or p.Name:match('^DeepForestTrunks') then p.Parent=archive end end
local n=0
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','');p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic;p.Parent=world;n+=1
 local mat=p.Name:match('__(%w+)$')
 local colors={LeafDark=Color3.fromRGB(115,151,119),LeafMid=Color3.fromRGB(156,187,140),LeafLight=Color3.fromRGB(191,211,150),Bark=Color3.fromRGB(168,153,119)}
 p.Color=colors[mat] or Color3.new(1,1,1)
 if p.Name:match('^DeepForestGrounded') then p.Transparency=.3;p.CastShadow=false end
end
patch.Parent=archive;world:SetAttribute('CanopyIteration',9)
return {added=n}
