-- Execute in the running client. Frame percentiles come from the rolling 3600-frame
-- RenderStep sample, after the five-second startup warmup. Stats values are snapshots.
local camera=workspace.CurrentCamera
local lighting=game:GetService('Lighting')
local stats=game:GetService('Stats')
local result={
 utc=os.date('!%Y-%m-%dT%H:%M:%SZ'),
 camera={camera.CFrame:GetComponents()},focus={camera.Focus.Position.X,camera.Focus.Position.Y,camera.Focus.Position.Z},
 fieldOfView=camera.FieldOfView,viewport={camera.ViewportSize.X,camera.ViewportSize.Y},
 quality=tostring(UserSettings():GetService('UserGameSettings').SavedQualityLevel),
 lightingStyle=tostring(lighting.LightingStyle),prioritizeLighting=lighting.PrioritizeLightingQuality,
 attributes=workspace:GetAttributes(),
 statsSnapshot={frameTimeSeconds=stats.FrameTime,renderCPURaw=stats.RenderCPUFrameTime,renderGPURaw=stats.RenderGPUFrameTime,drawCalls=stats.SceneDrawcallCount,triangles=stats.SceneTriangleCount,memoryMB=stats:GetTotalMemoryUsageMb()},
}
return result
