-- Run once in Studio Edit mode after importing Lumenwild.glb at scene origin.
-- No geometry is constructed here: every visible mesh comes from Blender.
local ChangeHistoryService = game:GetService("ChangeHistoryService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local Lighting = game:GetService("Lighting")
ChangeHistoryService:SetWaypoint("Before Lumenwild setup")
local world = workspace:FindFirstChild("DreamWorld") or workspace:FindFirstChild("Lumenwild_Production")
assert(world, "Import Assets/Exports/Lumenwild.glb first")
world.Name = "DreamWorld"
world.ModelStreamingMode=Enum.ModelStreamingMode.Persistent
-- Studio's Front/Top glTF import rotates Y-up exports 180 degrees around Y.
-- Apply the verified correction exactly once, before extracting the traveler.
if not world:GetAttribute("AuthoredCoordinates") then
 world:PivotTo(CFrame.Angles(0,math.pi,0))
 world.WorldPivot=CFrame.identity
 world:SetAttribute("AuthoredCoordinates",true)
end
local traveler = ReplicatedStorage:FindFirstChild("Traveler") or Instance.new("Model")
traveler.Name="Traveler"
traveler.Parent=ReplicatedStorage
local preserved=ServerStorage:FindFirstChild("OriginalTemplate") or Instance.new("Folder")
preserved.Name="OriginalTemplate"; preserved.Parent=ServerStorage
for _,name in {"Baseplate","SpawnLocation"} do
 local original=workspace:FindFirstChild(name)
 if original then original.Parent=preserved end
end
local palette={
 Stone={99,123,116}, StoneLight={140,158,142}, WetSlate={75,103,103}, WetSlateLight={94,117,111},
 Earth={60,78,65}, Moss={84,117,55}, MossLight={115,142,68}, Bark={73,87,59}, BarkLight={111,124,76},
 LeafDark={43,95,62}, LeafMid={63,123,72}, LeafLight={96,151,82}, Grass={90,145,80}, Fern={60,131,88},
 Water={34,117,118},Waterfall={77,173,167},Foam={157,218,201},GlowCyan={80,226,222},Stem={95,157,145},
 Brass={169,128,60},GlowAmber={255,165,60},Roof={69,114,104},Cloth={46,74,72},Armor={105,125,128},Leather={84,68,50},Face={177,153,127}
}
local meshCount=0
for _,p in world:GetDescendants() do
 if not p:IsA("BasePart") then continue end
 if p.Parent.Name:find("__") then p.Name=p.Parent.Name; p.Parent=world end
 meshCount+=1
 p.Anchored=true; p.CanCollide=false; p.CanTouch=false
 p.CanQuery=p.Name:find("Walkable_")~=nil
 p:SetAttribute("Walkable",p.CanQuery)
 local mat=p.Name:match("__(%w+)$")
 if mat and palette[mat] then
  local c=Color3.fromRGB(table.unpack(palette[mat])); p.Color=c
  local sa=p:FindFirstChildWhichIsA("SurfaceAppearance")
  if sa then
   sa.Color=c
   -- glTF scalar metalness was ignored by this importer; empty map is dielectric.
   if mat=="WetSlate" or mat=="WetSlateLight" or mat=="Water" then sa.MetalnessMap="" end
  end
 end
 p.Material=Enum.Material.SmoothPlastic
 if p:IsA("MeshPart") then p.DoubleSided=true; p.RenderFidelity=Enum.RenderFidelity.Automatic end
 if mat=="Stone" or mat=="StoneLight" or mat=="Bark" or mat=="BarkLight" then p.Material=Enum.Material.Slate end
 if mat=="Moss" or mat=="MossLight" then p.Material=Enum.Material.Grass end
 if mat=="WetSlate" or mat=="WetSlateLight" then p.Reflectance=.16 end
 if mat=="Water" then p.Material=Enum.Material.Glass; p.Transparency=.18; p.Reflectance=.22; p.CastShadow=false end
 if mat=="Waterfall" then p.Material=Enum.Material.Glass; p.Transparency=.24; p.CastShadow=false end
 if mat=="Foam" then p.Material=Enum.Material.Neon; p.Transparency=.43; p.CastShadow=false end
 if mat=="GlowCyan" or mat=="GlowAmber" then
  p.Material=Enum.Material.Neon; p.CastShadow=false
  if p.Name:find("Shrine") or p.Name:find("Lantern") or p.Name:find("Mushroom_0[048]") or p.Name:find("Mushroom_[123]0") then
   local l=p:FindFirstChild("ForestGlow") or Instance.new("PointLight")
   l.Name="ForestGlow"; l.Color=p.Color; l.Range=mat=="GlowAmber" and 13 or 10
   l.Brightness=mat=="GlowAmber" and 1.4 or .7; l.Shadows=false; l.Parent=p
  end
 end
 if p.Name:find("Actor_")==1 then p.Parent=traveler; p.CanQuery=false end
end
for _,wrapper in world:GetChildren() do
 if wrapper:IsA("Model") and #wrapper:GetChildren()==0 then wrapper:Destroy() end
end
traveler.WorldPivot=CFrame.identity
world.WorldPivot=CFrame.identity
-- These two Studio settings require the Properties UI on this Studio version.
local styleSet=pcall(function() Lighting.LightingStyle=Enum.LightingStyle.Realistic end)
local prioritySet=pcall(function() Lighting.PrioritizeLightingQuality=true end)
Lighting.GlobalShadows=true
Lighting.ClockTime=16.3
Lighting.GeographicLatitude=35
Lighting.Brightness=2.8
Lighting.ExposureCompensation=-.15
Lighting.Ambient=Color3.fromRGB(53,76,73)
Lighting.OutdoorAmbient=Color3.fromRGB(89,112,105)
Lighting.EnvironmentDiffuseScale=.65
Lighting.EnvironmentSpecularScale=1
Lighting.ShadowSoftness=.3
local atmosphere=Lighting:FindFirstChildOfClass("Atmosphere") or Instance.new("Atmosphere",Lighting)
atmosphere.Density=.32; atmosphere.Offset=.15; atmosphere.Color=Color3.fromRGB(175,205,188); atmosphere.Decay=Color3.fromRGB(80,113,106)
atmosphere.Haze=1.35; atmosphere.Glare=.15
local bloom=Lighting:FindFirstChildOfClass("BloomEffect") or Instance.new("BloomEffect",Lighting)
bloom.Intensity=.3; bloom.Size=30; bloom.Threshold=1.2
local sun=Lighting:FindFirstChildOfClass("SunRaysEffect") or Instance.new("SunRaysEffect",Lighting)
sun.Intensity=.065; sun.Spread=.75
local dof=Lighting:FindFirstChildOfClass("DepthOfFieldEffect")
if dof then dof.Enabled=false end
local grade=Lighting:FindFirstChild("ForestGrade") or Instance.new("ColorCorrectionEffect")
grade.Name="ForestGrade";grade.Saturation=.08;grade.Contrast=.08;grade.TintColor=Color3.fromRGB(240,255,242);grade.Parent=Lighting
workspace.CurrentCamera.CFrame=CFrame.lookAt(Vector3.new(43,60,69),Vector3.new(0,5,0))
workspace.CurrentCamera.FieldOfView=35
ChangeHistoryService:SetWaypoint("Lumenwild imported and configured")
return {meshes=meshCount,travelerParts=#traveler:GetChildren(),lighting=tostring(Lighting.LightingStyle),styleSet=styleSet,prioritySet=prioritySet}
