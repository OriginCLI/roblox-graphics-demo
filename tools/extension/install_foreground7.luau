local world=workspace:WaitForChild('DreamWorld')
local patch=workspace:WaitForChild('Lumenwild_Foreground7')
local archive=Instance.new('Folder');archive.Name='ExtensionBridge6_Archive';archive.Parent=game:GetService('ServerStorage')
patch:PivotTo(CFrame.Angles(0,math.pi,0));patch.WorldPivot=CFrame.identity
for _,p in world:GetChildren() do if p.Name:match('^BridgePiers__') or p.Name:match('^BridgePierMoss__') or p.Name:match('^BrokenParapets__') then p.Parent=archive end end
local n=0
for _,p in patch:GetDescendants() do
 if not p:IsA('MeshPart') then continue end
 p.Name=p.Parent.Name:gsub('%.%d+$','');p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.DoubleSided=true;p.RenderFidelity=Enum.RenderFidelity.Automatic;p.Parent=world;n+=1
 local mat=p.Name:match('__(%w+)$');local sa=p:FindFirstChildOfClass('SurfaceAppearance')
 local tints={Stone=Color3.fromRGB(140,157,143),StoneLight=Color3.fromRGB(191,196,177),Moss=Color3.fromRGB(147,165,105),LeafDark=Color3.fromRGB(115,151,119),LeafMid=Color3.fromRGB(156,187,140),Fern=Color3.fromRGB(159,194,148),Flower=Color3.fromRGB(177,127,220),Stem=Color3.fromRGB(108,168,156)}
 if tints[mat] then p.Color=tints[mat] end
 if mat=='GlowCyan' then
  p.Material=Enum.Material.SmoothPlastic;p.Color=Color3.fromRGB(51,190,191)
  if sa then sa.Color=p.Color;sa.EmissiveMaskContent=Content.fromUri('rbxassetid://140651532164331');sa.EmissiveTint=Color3.fromRGB(49,184,184);sa.EmissiveStrength=.85;sa.RoughnessMap='rbxassetid://140651532164331' end
 elseif mat=='Foam' then p.Color=Color3.fromRGB(202,255,247);p.Material=Enum.Material.Neon;p.Transparency=.08;p.CastShadow=false end
end
patch.Parent=archive;world:SetAttribute('ForegroundIteration',7)
return {added=n}
