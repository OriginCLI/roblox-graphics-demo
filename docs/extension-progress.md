# Three-hour refinement

## Sixty-minute checkpoint

Actual runtime capture `iterations/02-60min.png`, metrics `iterations/02-60min-metrics.json`. Independent critic: **5.1/10** = composition 1.9/3, lighting 1.2/3, materials 1.4/3, detail 0.6/1. Improved rooted tree, wet paving, clustered planting and atmospheric separation. Remaining major gaps are planar water, repeated vertical cliff shapes, regular material patterns, and missing warm directional haze.

3600 frames: mean 60.0024 FPS, p95 17.7425 ms, p99 18.2556 ms. Quality 10, Realistic. User adjusted Studio window bounds; virtual viewport is now 1920x1080, one pixel wider than baseline. Camera transform and FOV remain unchanged. Snapshot 541 draw calls, 761683 rendered triangles, 2611.21 MB memory. These are Studio desktop measurements, not a published client benchmark or proof of every-frame 60 FPS.

Editable incremental Blender scenes: TreePatch2, Landscape3, DepthGarden4, Paving5. `Assets/Blender/Lumenwild_Working60.blend` preserves all working scenes and an adjusted copy of DepthGarden4. Native importer patches and material/lighting settings are recorded under `tools/extension`. New 512px roughness maps loaded successfully in the actual client: WaterGloss_v3 ID 116759003152394; StoneGloss_v3 ID 126979061121564. Earlier rejected/failed swatches remain historical source assets.

Started 2026-09-13 15:42:59 UTC. Hard finish 18:42:59 UTC; final verification reserve starts 18:27:59 UTC. Comparison checkpoints approximately 16:13, 16:43, 17:13, 17:43, 18:13 UTC. Two-hour report due 17:43 UTC.

Original target remains `.dream-loop/target.png`, SHA256 DE9324B5ADAAFB321F5FBDFDBCD702ED5CD3327631BBA397FCB2DEC7BD296F94. Fixed rubric: composition 3, lighting 3, materials 3, details 1. No target regeneration.

Fixed comparison: camera position (29.1072044,35.4113541,58.1382866), focus (-6,8.15999985,8), yaw 35 degrees, pitch 24 degrees, distance 67, FOV 48. Desktop manual quality 10, Realistic lighting, PrioritizeLightingQuality enabled. Initial viewport 1919x1080; MCP evidence capture 1264x711.

## Baseline

Actual Play screenshot: `iterations/00-baseline.png`. Independent critic: **3.8/10** = composition 1.6/3, lighting 0.8/3, materials 1.0/3, details 0.4/1. Prioritize ravine depth, curved root architecture, foreground bridge extent, warm/cool lighting separation, and ragged canopy framing.

Initial measured sample: 2008 frames, mean 60.0034 FPS, p95 frame time 17.834 ms, p99 18.416 ms. This is an average near 60 FPS, not proof that every frame meets 16.67 ms.

Material inspection found all five existing roughness PNGs are black. Correct authoring data and verify saved pixels before importing replacements. Albedo-only imported materials use MeshPart.TextureID; adding an empty SurfaceAppearance hides these textures.

## Thirty-minute checkpoint

Actual screenshot `iterations/01-30min.png`, metrics `iterations/01-30min-metrics.json`. Independent score **4.0/10** = composition 1.7/3, lighting 0.9/3, materials 1.0/3, details 0.4/1. An earlier structural test scored 3.3/10 (1.4, 0.7, 0.8, 0.4); the straight canyon approach was replaced with staggered ledges. The modest improvement over baseline is not a claim of target fidelity.

At 16:13 UTC: 3600 frames, mean 60.0021 FPS, p95 17.6817 ms, p99 18.1551 ms. Camera components match baseline; tiny focus rounding differences are below 0.000002 studs. Quality 10, Realistic, 1919x1080. Snapshot 425 draw calls and 493677 rendered triangles. Console empty after material retry.

Remaining priorities: cliff sides still extruded and uniform; roots resemble airborne fins; bridge glare too continuous; canopy too thin; broad pale background haze; mushroom glow loses cap shape. A grounded unified voxel tree is modeled but not yet imported at this checkpoint.

New packed roughness IDs intermittently fail with `Asset is not approved for the requester`. A temporary verified-visible fallback uses the stone color image as a spatially varying roughness input. Separate albedo-path data swatches are prepared to test reliable explicit roughness and normal image IDs. Official waterfall texture 16808804567 failed Edit preload but succeeded in the running Client; evaluate asset availability in runtime.

Traveler shifted to (2.6,0.16,21.7) with compensating focus offset (-8.6,8,-13.7), preserving the original camera while improving character placement. Scene layout adjustments are mirrored in `tools/extension/stage2_layout.py` and `.luau`.
