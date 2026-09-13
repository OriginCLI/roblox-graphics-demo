for _,p in workspace.DreamWorld:GetChildren() do
 if not p:IsA('MeshPart') then continue end
 for _,l in p:GetChildren() do
  if l:IsA('PointLight') and not p.Name:find('Mushroom') then
   l.Range=14;l.Brightness=2.1;l.Color=Color3.fromRGB(255,196,116)
  end
 end
end
return 'Lantern range and color balanced against directional light'
