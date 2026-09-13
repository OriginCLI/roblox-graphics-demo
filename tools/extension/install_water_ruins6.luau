local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_WaterRuins6')
local archive=Instance.new('Folder');archive.Name='ExtensionWaterCastle5_Archive';archive.Parent=game:GetService('ServerStorage')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
for _,p in world:GetChildren() do if p.Name:match('^Citadel') or p.Name=='Water_Near__Water' then p.Parent=archive end end
local n=0
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','')
 p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic
 p.Parent=world;n+=1
 local mat=p.Name:match('__(%w+)$');local sa=p:FindFirstChildOfClass('SurfaceAppearance')
 if mat=='Water' then
  p.Color=Color3.fromRGB(35,121,113);p.Transparency=.28;p.CastShadow=false;p.Reflectance=.05
  if sa then sa.Color=p.Color;sa.RoughnessMap='rbxassetid://116759003152394';sa.MetalnessMap='' end
 elseif mat=='Stone' or mat=='StoneLight' then
  p.Color=mat=='StoneLight' and Color3.fromRGB(191,196,177) or Color3.fromRGB(140,157,143)
 elseif mat=='Moss' then p.Color=Color3.fromRGB(147,165,105)
 elseif mat=='LeafDark' then p.Color=Color3.fromRGB(115,151,119) end
 if p.Name:match('^FarForestGround') then p.TextureID='';p.Color=Color3.fromRGB(103,128,117);p.CastShadow=false end
end
patch.Parent=archive;world:SetAttribute('WaterRuinsIteration',6)
return {added=n}
