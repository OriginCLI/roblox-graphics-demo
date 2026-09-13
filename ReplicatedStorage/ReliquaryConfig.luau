-- Shared presentation settings. World coordinates use studs, Y up.
return {
 Title = "L U M E N W I L D",
 Subtitle = "THE LANTERN GROVE",
 Spawn = Vector3.new(2.6, 0.16, 21.7),
 WalkMin = Vector2.new(-4.5, -18),
 WalkMax = Vector2.new(4.5, 28),
 WalkSpeed = 9,
 ActorScale = 1.6,
 CameraYaw = math.rad(35),
 CameraPitch = math.rad(24),
 CameraDistance = 67,
 MinDistance = 40,
 MaxDistance = 105,
 FieldOfView = 48,
 -- Shift the traveler lower in frame while preserving the exact comparison camera.
 FocusOffset = Vector3.new(-8.6, 8, -13.7),
}
