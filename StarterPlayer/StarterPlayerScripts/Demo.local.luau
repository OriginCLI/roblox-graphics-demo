local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local GuiService = game:GetService("GuiService")
local StarterGui = game:GetService("StarterGui")
local Config = require(ReplicatedStorage:WaitForChild("ReliquaryConfig"))
local player = Players.LocalPlayer
local world = workspace:WaitForChild("DreamWorld", 60)
local template = ReplicatedStorage:WaitForChild("Traveler", 60)
if not world or not template then warn("Import DreamWorld and Traveler before playing.") return end

pcall(function() StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.All, false) end)
local actor = template:Clone()
actor.Name = "LocalTraveler"
actor.Parent = workspace
local parts = {}
local origin = actor:GetPivot()
for _,part in actor:GetDescendants() do
 if part:IsA("BasePart") then
  part.Anchored = true
  part.CanCollide = false
  part.CanQuery = false
  table.insert(parts, { part = part, localCF = origin:ToObjectSpace(part.CFrame) })
 end
end

local camera = workspace.CurrentCamera
camera.CameraType = Enum.CameraType.Scriptable
camera.FieldOfView = Config.FieldOfView
local position = Config.Spawn
local destination = position
local focus = position + Vector3.new(0, 3, 0)
local yaw, desiredYaw = Config.CameraYaw, Config.CameraYaw
local distance, desiredDistance = Config.CameraDistance, Config.CameraDistance
local heading = 0
local dragging, moved, pressPosition = false, false, Vector2.zero
local phase = 0
local frameTimes = {}
local totalTime = 0
local warmup = 5

local gui = Instance.new("ScreenGui")
gui.Name = "DreamHUD"
gui.IgnoreGuiInset = true
gui.ResetOnSpawn = false
gui.Parent = player:WaitForChild("PlayerGui")
local function label(name, text, position2, size, font, color)
 local l = Instance.new("TextLabel")
 l.Name = name
 l.BackgroundTransparency = 1
 l.Position = position2
 l.Size = size
 l.Font = font
 l.Text = text
 l.TextSize = 14
 l.TextColor3 = color
 l.TextXAlignment = Enum.TextXAlignment.Left
 l.TextStrokeTransparency = 0.65
 l.Parent = gui
 return l
end
local title = label("Title", Config.Title, UDim2.new(0,32,0,26), UDim2.fromOffset(700,34), Enum.Font.Garamond, Color3.fromRGB(230,221,198))
title.TextSize = 28
label("Subtitle", Config.Subtitle, UDim2.new(0,34,0,61), UDim2.fromOffset(650,24), Enum.Font.Gotham, Color3.fromRGB(151,174,179)).TextSize = 11
label("Controls", "CLICK TO WALK     ·     DRAG TO ORBIT     ·     SCROLL TO ZOOM", UDim2.new(0,32,1,-47), UDim2.fromOffset(700,24), Enum.Font.Gotham, Color3.fromRGB(205,213,210)).TextSize = 11
local perf = label("Performance", "", UDim2.new(1,-225,1,-47), UDim2.fromOffset(200,24), Enum.Font.Code, Color3.fromRGB(155,178,181))
perf.TextXAlignment = Enum.TextXAlignment.Right

local rayParams = RaycastParams.new()
rayParams.FilterType = Enum.RaycastFilterType.Include
rayParams.FilterDescendantsInstances = {world}
local function chooseDestination(screenPoint)
 local inset = GuiService:GetGuiInset()
 local ray = camera:ViewportPointToRay(screenPoint.X-inset.X, screenPoint.Y-inset.Y)
 local hit = workspace:Raycast(ray.Origin, ray.Direction * 1000, rayParams)
 if not hit or not hit.Instance:GetAttribute("Walkable") then return end
 destination = Vector3.new(math.clamp(hit.Position.X,Config.WalkMin.X,Config.WalkMax.X),Config.Spawn.Y,math.clamp(hit.Position.Z,Config.WalkMin.Y,Config.WalkMax.Y))
 workspace:SetAttribute("DemoDestination", destination)
end
UserInputService.InputBegan:Connect(function(input, processed)
 if processed then return end
 if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.MouseButton2 then
  dragging = true
  moved = input.UserInputType == Enum.UserInputType.MouseButton2
  pressPosition = UserInputService:GetMouseLocation()
 end
end)
UserInputService.InputChanged:Connect(function(input, processed)
 if input.UserInputType == Enum.UserInputType.MouseMovement and dragging then
  if (UserInputService:GetMouseLocation()-pressPosition).Magnitude > 5 then moved = true end
  if moved then desiredYaw -= input.Delta.X * 0.006 end
 elseif input.UserInputType == Enum.UserInputType.MouseWheel and not processed then
  desiredDistance = math.clamp(desiredDistance-input.Position.Z*5, Config.MinDistance, Config.MaxDistance)
 end
end)
UserInputService.InputEnded:Connect(function(input)
 if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.MouseButton2 then
  if dragging and not moved and input.UserInputType == Enum.UserInputType.MouseButton1 then chooseDestination(UserInputService:GetMouseLocation()) end
  dragging = false
 end
end)
UserInputService.WindowFocusReleased:Connect(function() dragging = false end)

local function angleLerp(a,b,t)
 return a + math.atan2(math.sin(b-a), math.cos(b-a))*t
end
local updateClock = 0
RunService:BindToRenderStep("DreamPresentation", Enum.RenderPriority.Camera.Value+1, function(dt)
 totalTime += dt
 local step = math.min(dt,0.1)
 local delta = destination-position
 local walking = delta.Magnitude > 0.12
 if walking then
  position += delta.Unit*math.min(delta.Magnitude,Config.WalkSpeed*step)
  heading = angleLerp(heading, math.atan2(-delta.X,-delta.Z), 1-math.exp(-12*step))
 end
 phase += step*(walking and 9 or 1.6)
 local bob = walking and math.abs(math.sin(phase))*0.09 or math.sin(phase)*0.025
 local root = CFrame.new(position+Vector3.new(0,bob,0))*CFrame.Angles(0,heading,0)
 for _,entry in parts do
  local name = entry.part.Name
  local sway = CFrame.identity
  if name:find("LegL") or name:find("ArmR") then
   sway = CFrame.Angles(walking and math.sin(phase)*0.35 or 0,0,0)
  elseif name:find("LegR") or name:find("ArmL") then
   sway = CFrame.Angles(walking and -math.sin(phase)*0.35 or 0,0,0)
  elseif name:find("Cloak") then
   sway = CFrame.Angles(math.sin(phase*0.7)*0.04,0,math.sin(phase*0.5)*0.025)
  end
  entry.part.CFrame = root*entry.localCF*sway
 end
 focus = focus:Lerp(position+Vector3.new(0,3,0),1-math.exp(-3*step))
 yaw += (desiredYaw-yaw)*(1-math.exp(-10*step))
 distance += (desiredDistance-distance)*(1-math.exp(-9*step))
 local offset = Vector3.new(math.sin(yaw)*math.cos(Config.CameraPitch),math.sin(Config.CameraPitch),math.cos(yaw)*math.cos(Config.CameraPitch))*distance
 camera.CFrame = CFrame.lookAt(focus+offset,focus)
 camera.Focus = CFrame.new(focus)
 if totalTime > warmup then table.insert(frameTimes,dt) if #frameTimes>3600 then table.remove(frameTimes,1) end end
 updateClock += dt
 if updateClock >= 1 then
  updateClock = 0
  local sum = 0 for _,v in frameTimes do sum += v end
  local fps = #frameTimes/math.max(sum,0.001)
  perf.Text = string.format("%.0f FPS  /  DESKTOP",fps)
  workspace:SetAttribute("DemoPosition",position)
  workspace:SetAttribute("DemoCameraYaw",yaw)
  workspace:SetAttribute("DemoCameraDistance",distance)
  workspace:SetAttribute("DemoFrameCount",#frameTimes)
  workspace:SetAttribute("DemoMeanFPS",fps)
  if #frameTimes > 120 then
   local sorted = table.clone(frameTimes) table.sort(sorted)
   workspace:SetAttribute("DemoP95FrameMs",sorted[math.ceil(#sorted*0.95)]*1000)
   workspace:SetAttribute("DemoP99FrameMs",sorted[math.ceil(#sorted*0.99)]*1000)
  end
 end
end)
