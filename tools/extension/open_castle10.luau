local w=workspace.DreamWorld
if w:GetAttribute('CastleSightlineOpened') then return 'Already adjusted' end
local changes={[2]={base=1,height=16,delta=-5},[3]={base=2,height=15,delta=-7},[7]={base=8,height=18,delta=-12}}
local n=0
for _,p in w:GetChildren() do
 if not p:IsA('MeshPart') then continue end
 for i,c in changes do
  if p.Name:match('Forest_'..i..'__') and (p.Name:find('Canopy') or p.Name:find('Vine')) then p.CFrame+=Vector3.new(0,c.delta,0);n+=1
  elseif p.Name:match('^ForestVolumeTrunk_'..i..'__') or p.Name:match('^ForestVolumeBranch_'..i..'__') then
   local scale=(c.height+c.delta)/c.height
   p.Size=Vector3.new(p.Size.X,p.Size.Y*scale,p.Size.Z)
   p.CFrame=CFrame.new(p.Position.X,c.base+(p.Position.Y-c.base)*scale,p.Position.Z)*p.CFrame.Rotation;n+=1
  end
 end
end
w:SetAttribute('CastleSightlineOpened',true)
return {adjusted=n}
