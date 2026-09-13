-- Presentation-only motion, kept local to avoid network replication per frame.
local RunService = game:GetService("RunService")
local world = workspace:WaitForChild("DreamWorld", 60)
if not world then return end
local moving = {}
local lights = {}
local function particles(part, name, texture, rate, life, speed, size, color)
 local a = Instance.new("Attachment")
 a.Name = name .. "Origin"
 a.Parent = part
 local p = Instance.new("ParticleEmitter")
 p.Name = name
 p.Texture = texture
 p.Rate = rate
 p.Lifetime = NumberRange.new(life * .7, life)
 p.Speed = NumberRange.new(speed * .5, speed)
 p.Size = NumberSequence.new(size)
 p.Color = ColorSequence.new(color)
 p.Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0,1),NumberSequenceKeypoint.new(.2,.45),NumberSequenceKeypoint.new(.8,.65),NumberSequenceKeypoint.new(1,1)})
 p.SpreadAngle = Vector2.new(35,35)
 p.LightEmission = .4
 p.Parent = a
 return p
end
local mushroomCount = 0
for _,p in world:GetDescendants() do
 if not p:IsA("BasePart") then continue end
 if p.Name:find("Canopy_") or p.Name:find("Vines_") or p.Name:find("CanopyVolume_") or p.Name:find("CanopyFringe_") or p.Name:find("CanopyWild") or p.Name:find("VinesVolume_") or p.Name:find("VineLeafVolume_") then
  table.insert(moving,{part=p,origin=p.CFrame,phase=p.Position.X*.12+p.Position.Z*.07,kind="leaves"})
 elseif p.Name:find("FallStreak") or p.Name:find("Foam_") then
  table.insert(moving,{part=p,origin=p.CFrame,phase=p.Position.Y,kind="water"})
 elseif p.Name:find("Glow_Mushroom") then
  mushroomCount += 1
  if mushroomCount % 5 == 0 then
   local fireflies = particles(p,"Fireflies","rbxasset://textures/particles/sparkles_main.dds",1.3,7,.7,.12,Color3.fromRGB(177,255,169))
   fireflies.LightEmission=1
   fireflies.SpreadAngle=Vector2.new(90,90)
   fireflies.Acceleration=Vector3.new(.05,.08,0)
  end
 elseif p.Name:match("^Foam_") then
  -- Foam meshes are animated above; waterfall mist is attached below.
 end
 if p.Name:match("^Fall_%d") then
  local mist = particles(p,"WaterfallMist","rbxasset://textures/particles/smoke_main.dds",5,2.5,1.8,3,Color3.fromRGB(171,222,214))
  mist.EmissionDirection=Enum.NormalId.Bottom
  mist.Acceleration=Vector3.new(0,-1.5,0)
  mist.Parent.Position=Vector3.new(0,-p.Size.Y/2,0)
 end
 for _,light in p:GetChildren() do
  if light:IsA("PointLight") then table.insert(lights,{light=light,base=light.Brightness,phase=p.Position.X}) end
 end
end
local pool=world:FindFirstChild("WaterNear6__Water") or world:FindFirstChild("Water_Near__Water") or world:FindFirstChild("Water_Pool__Water")
if pool then
 for i,position in {Vector3.new(-61,-15,-22),Vector3.new(-89,-17,-9),Vector3.new(-132,-26,-42),Vector3.new(-43,-5,43),Vector3.new(-24,-5,9),Vector3.new(-145,-13,-45)} do
  local mist=particles(pool,"RavineMist"..i,"rbxasset://textures/particles/smoke_main.dds",1.7,14,.7,28,Color3.fromRGB(204,221,214))
  mist.Parent.Position=pool.CFrame:PointToObjectSpace(position)
  mist.Transparency=NumberSequence.new({NumberSequenceKeypoint.new(0,1),NumberSequenceKeypoint.new(.25,.79),NumberSequenceKeypoint.new(.75,.86),NumberSequenceKeypoint.new(1,1)})
  mist.Rotation=NumberRange.new(-180,180)
  mist.RotSpeed=NumberRange.new(-2,2)
 mist.LightEmission=.15
 end
 -- Soft directional shafts use supported Beams, attached to the modeled pool.
 local sun=game:GetService('Lighting'):GetSunDirection()
 for i,finish in {Vector3.new(-60,-8,-17),Vector3.new(-43,-6,12),Vector3.new(-17,-3,-8),Vector3.new(-77,-14,-40)} do
  local a=Instance.new('Attachment');a.Name='SunShaftTop'..i;a.Parent=pool;a.WorldPosition=finish+sun*90
  local b=Instance.new('Attachment');b.Name='SunShaftBottom'..i;b.Parent=pool;b.WorldPosition=finish
  local beam=Instance.new('Beam');beam.Name='SunShaft'..i;beam.Attachment0=a;beam.Attachment1=b
  beam.Texture='rbxasset://textures/particles/smoke_main.dds';beam.TextureMode=Enum.TextureMode.Stretch;beam.TextureSpeed=0
  beam.Width0=2;beam.Width1=12;beam.FaceCamera=true;beam.Segments=10
  beam.Color=ColorSequence.new(Color3.fromRGB(255,224,163));beam.LightEmission=1;beam.LightInfluence=0
  beam.Transparency=NumberSequence.new({NumberSequenceKeypoint.new(0,1),NumberSequenceKeypoint.new(.3,.68),NumberSequenceKeypoint.new(.65,.62),NumberSequenceKeypoint.new(1,1)})
  beam.Parent=pool
 end
end
-- Layered moving cascades follow Roblox's official waterfall VFX technique.
-- Attachments use existing Blender meshes; no scene geometry is made in Luau.
local cascades={
 {-24,6,10,-.5,-5}, {-38,31,8,2,-5}, {-60,-30,9,8,-29},
 {-117,-22,8,1,-29}, {-146,-43,7,2,-48},
}
for i,f in cascades do
 local part=world:FindFirstChild('Fall_'..(i-1)..'__FallVeil')
 if not part then continue end
 local x,z,w,top,bottom=table.unpack(f)
 for layer=1,2 do
  local a=Instance.new('Attachment');a.Name='CascadeTop'..layer;a.Parent=part
  a.WorldPosition=Vector3.new(x+(layer-1)*.4,top,z+.15)
  local b=Instance.new('Attachment');b.Name='CascadeBottom'..layer;b.Parent=part
  b.WorldPosition=Vector3.new(x,bottom,z+2.3+(layer-1)*.3)
  local beam=Instance.new('Beam');beam.Name='FlowingCascade'..layer
  beam.Attachment0=a;beam.Attachment1=b
  beam.Texture='rbxassetid://16808804567'
  beam.Width0=w*(layer==1 and .9 or .7);beam.Width1=w*(layer==1 and 1.04 or 1.14)
  beam.TextureMode=Enum.TextureMode.Wrap;beam.TextureLength=5+layer*2
  beam.TextureSpeed=layer==1 and 1.3 or .8
  beam.FaceCamera=true;beam.Segments=12
  beam.LightEmission=.12;beam.LightInfluence=.65
  beam.Color=ColorSequence.new(Color3.fromRGB(216,238,231))
  beam.Transparency=NumberSequence.new({NumberSequenceKeypoint.new(0,.85),NumberSequenceKeypoint.new(.1,.36),NumberSequenceKeypoint.new(.78,.45),NumberSequenceKeypoint.new(1,1)})
  beam.Parent=part
 end
end
local t = 0
RunService.Heartbeat:Connect(function(dt)
 t += math.min(dt,.1)
 for _,e in moving do
  if e.kind=="leaves" then
   e.part.CFrame=e.origin*CFrame.Angles(0,0,math.sin(t*.65+e.phase)*.004)
  else
   e.part.CFrame=e.origin+Vector3.new(0,math.sin(t*2.7+e.phase)*.12,0)
  end
 end
 for _,e in lights do e.light.Brightness=e.base*(.95+math.sin(t*1.6+e.phase)*.05) end
 workspace:SetAttribute("EnvironmentTime",t)
end)
