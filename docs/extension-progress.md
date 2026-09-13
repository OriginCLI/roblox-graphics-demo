# Three-hour refinement

## Intermediate movement and geometry checks

The new paving initially lacked the `Walkable` attribute used by the input raycast. Movement testing exposed it; the installer and Edit data model now set the attribute. An actual click moved the traveler from (2.6,0.16,21.7) toward (-0.079,0.16,-8.150), reaching (-0.069,0.16,-8.032). Right-drag changed yaw from 0.610865 to 1.14585 and then 0.18119 radians; scroll changed distance 67 to 62.

The instrumented moving/orbit sample fell to 54.25 average FPS with p99 67.07 ms. This is a failed stable-60 result; it includes active MCP input/capture operations and new views. Cause is not isolated. After returning to the fixed camera and warming a fresh run, 3600 frames averaged 60.0025 FPS, p95 17.7480 ms, p99 18.2360 ms, with 611 draw calls and 1150069 rendered triangles. Moving-camera validation must be repeated before final delivery.

Orbit inspection exposed open seams between cliff strata and distant trees ending above the basin. CliffIntegrity8 replaces open cliff sheets with overlapping closed stone volumes; CanopyGrounded9 is prepared to replace disk-like crowns and extend distant roots to the basin. WaterRuins6 models a continuous riverbed and shallow surface waves, open abbey ruins and another aqueduct. Foreground7 replaces bridge parapets and adds larger mushroom and broad-leaf silhouettes. The water replacement also broke a name-based mist attachment; the synchronized Environment script now finds the new pool mesh.

## Ninety-minute checkpoint

Actual runtime `iterations/03-90min.png`; independent critic **6.0/10** = composition 2.2/3, lighting 1.6/3, materials 1.6/3, details 0.6/1. The broader curved foreground bridge, closed cliff seams, irregular crown outlines, open ruined abbey, and grounded far trees improve correspondence. Remaining gaps: too much open right-hand water, repetitive root and terrain blocks, uniform gray-green haze, and simplistic lantern housings. Camera remains fixed; the critic's proposed camera movement is not adopted because comparison consistency is required.

3600 stationary frames: mean 60.0031 FPS, p95 17.7281 ms, p99 18.2777 ms; snapshot 613 draw calls, 1250439 triangles, 2550.16 MB. Same 1920x1080 virtual viewport, manual quality 10 and Realistic lighting. Earlier movement spikes remain unresolved, not excluded from the performance record.

Editable source is consolidated in `Assets/Blender/Lumenwild_Consolidated90.blend`: all 18 source scenes and 31 packed images. Redundant uncommitted intermediate full-file snapshots were removed after verifying their scenes in the consolidated file when C: ran out of space. Their scripts and GLBs remain. The assembled scene matches all 609 pre-BridgeFlow10 mesh sources; the subsequent Flow10 source scene is also preserved. The saved place includes all patches through BridgeFlow10, opened castle sightline and lantern balance. The missing Walkable attribute on replacement paving was repaired and verified with real click-to-walk and drag/zoom input.

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
