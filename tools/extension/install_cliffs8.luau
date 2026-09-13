local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_CliffIntegrity8')
local archive=Instance.new('Folder');archive.Name='ExtensionCliffs7_Archive';archive.Parent=game:GetService('ServerStorage')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
for _,p in world:GetChildren() do if p.Name:match('^TerraceCliff_') then p.Parent=archive end end
local n=0
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','');p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic;p.Parent=world;n+=1
 local mat=p.Name:match('__(%w+)$')
 p.Color=mat=='CliffDark' and Color3.fromRGB(96,119,111) or (mat=='StoneLight' and Color3.fromRGB(191,196,177) or Color3.fromRGB(140,157,143))
 if p.Name:match('^DistantBasin') then p.TextureID='';p.Color=Color3.fromRGB(95,121,108);p.CastShadow=false end
end
patch.Parent=archive;world:SetAttribute('CliffIntegrityIteration',8)
return {added=n}
