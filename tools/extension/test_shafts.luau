-- Temporary client experiment. Uses supported Beams attached to existing Blender mesh.
local world=workspace.DreamWorld
local part=world:FindFirstChild('WaterNear6__Water')
local sun=game:GetService('Lighting'):GetSunDirection()
for i,finish in {Vector3.new(-60,-8,-17),Vector3.new(-43,-6,12),Vector3.new(-17,-3,-8),Vector3.new(-77,-14,-40)} do
 local a=Instance.new('Attachment');a.Name='ShaftTop';a.Parent=part;a.WorldPosition=finish+sun*90
 local b=Instance.new('Attachment');b.Name='ShaftBottom';b.Parent=part;b.WorldPosition=finish
 local beam=Instance.new('Beam');beam.Name='SunShaftTest';beam.Attachment0=a;beam.Attachment1=b
 beam.Texture='rbxasset://textures/particles/smoke_main.dds';beam.TextureMode=Enum.TextureMode.Stretch;beam.TextureSpeed=0
 beam.Width0=2;beam.Width1=12;beam.FaceCamera=true;beam.Segments=10
 beam.Color=ColorSequence.new(Color3.fromRGB(255,224,163));beam.LightEmission=1;beam.LightInfluence=0
 beam.Transparency=NumberSequence.new({NumberSequenceKeypoint.new(0,1),NumberSequenceKeypoint.new(.3,.92),NumberSequenceKeypoint.new(.65,.90),NumberSequenceKeypoint.new(1,1)})
 beam.Parent=part
end
return 'Four soft directional shaft experiments'
