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
 if p.Name:find("Canopy_") or p.Name:find("Vines_") then
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
