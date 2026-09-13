-- This is a presentation demo: each client owns its local visual traveler.
-- The imported, anchored world is shared through the saved place.
local Players = game:GetService("Players")
Players.CharacterAutoLoads = false
local world = workspace:WaitForChild("DreamWorld")
world.ModelStreamingMode = Enum.ModelStreamingMode.Persistent
local function focus(player)
 for _,part in world:GetDescendants() do
  if part:IsA("BasePart") and part:GetAttribute("Walkable") then
   player.ReplicationFocus = part
   break
  end
 end
end
Players.PlayerAdded:Connect(focus)
for _,player in Players:GetPlayers() do focus(player) end
