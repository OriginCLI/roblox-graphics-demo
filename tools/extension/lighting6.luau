local l=game:GetService('Lighting')
l.ColorShift_Top=Color3.fromRGB(255,202,117)
local a=l:FindFirstChildOfClass('Atmosphere')
a.Color=Color3.fromRGB(232,223,203);a.Decay=Color3.fromRGB(153,183,175);a.Haze=1.3;a.Glare=.6
return 'Refined warm atmosphere without full-scene yellow wash'
