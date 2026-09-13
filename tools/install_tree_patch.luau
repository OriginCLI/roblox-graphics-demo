-- Only needed when applying HeroTree_Polish.glb to the already imported second pass.
-- The full Lumenwild_Refined.glb already includes this final tree geometry.
local incoming=assert(workspace:FindFirstChild("Lumenwild_Refined"),"Import HeroTree_Polish.glb at scene origin")
local world=assert(workspace:FindFirstChild("DreamWorld"))
incoming:PivotTo(CFrame.Angles(0,math.pi,0))
local archive=Instance.new("Folder")
archive.Name="TreePatch_Archive";archive.Parent=game.ServerStorage
local replaced=0
for _,p in incoming:GetDescendants() do
 if not p:IsA("MeshPart") then continue end
 local name=p.Parent.Name:gsub("%.%d+$","")
 local old=world:FindFirstChild(name)
 if old then old.Parent=archive end
 p.Name=name;p.Parent=world;p.Anchored=true;p.CanCollide=false;p.CanQuery=false;p.CanTouch=false;p.DoubleSided=true
 local sa=p:FindFirstChildOfClass("SurfaceAppearance") or Instance.new("SurfaceAppearance",p)
 sa.ColorMap="rbxassetid://129062666118089";sa.Color=Color3.fromRGB(205,201,170)
 p.Color=Color3.new(1,1,1)
 replaced+=1
end
incoming:Destroy()
return {replaced=replaced}
