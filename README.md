# Lumenwild — The Lantern Grove

A desktop Roblox graphics demo: a cloaked traveler on a wet stone bridge leading to an amber shrine in an ancient enchanted tree. Voxel foliage, mossy cliffs, distant arches, turquoise water, mushrooms, fireflies, mist, and subtle environmental motion surround a bounded walking area. There is no gameplay.

## Open and run

1. Check out `dream-loop/demo` and run `git lfs pull` to retrieve the binary assets.
2. Open `Places/Lumenwild.rbxl` in Roblox Studio. This saved place is the easiest way to run the complete scene; reimporting is not required.
3. Press Play. Use desktop mouse controls below. For the tested presentation quality, open Roblox Settings, set Graphics Mode to Manual and Graphics Quality to 10.
4. The place references uploaded Roblox mesh and image assets. A signed-in account and network access may be needed to fetch uncached assets. Asset access from a different account or a published experience has not been validated.

## Controls

| Input | Result |
| --- | --- |
| Left click on bridge paving | Walk toward the selected point |
| Left drag or right drag | Orbit the camera horizontally |
| Mouse wheel | Zoom between 40 and 105 studs |

The camera eases toward the traveler. Walking is limited to X `-4.5…4.5`, Z `-18…28`; surrounding scenery is presentation only. Clicking scenery outside the walkable meshes is ignored. The traveler is a local visual model, not a normal Roblox avatar.

## Project and synchronization

The existing service folder layout is preserved. Studio File Script Sync was already configured and changes were verified in Studio. No Rojo project or replacement sync configuration was introduced.

| Local path | Studio destination |
| --- | --- |
| `ReplicatedStorage/ReliquaryConfig.luau` | ModuleScript `ReplicatedStorage.ReliquaryConfig` |
| `ServerScriptService/World.server.luau` | Script `ServerScriptService.World` |
| `StarterPlayer/StarterPlayerScripts/Demo.local.luau` | LocalScript `StarterPlayer.StarterPlayerScripts.Demo` |
| `StarterPlayer/StarterPlayerScripts/Environment.local.luau` | LocalScript `StarterPlayer.StarterPlayerScripts.Environment` |

`StarterPlayer` itself is not synchronized; its `StarterPlayerScripts` and `StarterCharacterScripts` containers are, as documented in the original `StarterPlayer/INFO.md`. If opening on another machine, connect those existing folders to the corresponding Studio containers with File Script Sync. The saved place also contains the scripts. Keep `Assets`, `Places`, `tools`, and `docs` outside service sync roots.

The server disables automatic character loading and establishes replication focus. Camera, input, traveler animation, foliage motion, water effects, and light flicker run on the client. The world is anchored, persistent, and has streaming disabled for this desktop demo. Original template content and prior scene revisions remain preserved in ServerStorage.

## Editable art and import

- `Assets/Blender/Lumenwild.blend`: editable Blender 5.1 source with packed textures. Active final scene is `Lumenwild_Refined`; the original default scene and earlier production scene are preserved.
- `Assets/Exports/Lumenwild_Refined.glb`: final complete Y-up scene, including traveler and distant forest instances.
- `Assets/Exports/refined-manifest.json`: mesh and evaluated triangle counts.
- `Assets/Textures`: generated albedo/normal sources and constant roughness maps.
- `Assets/Exports/Lumenwild.glb` and `HeroTree_Polish.glb`: earlier iteration/patch exports retained for provenance.

All scene and character geometry was authored through Blender 5.1.2 MCP. Studio placement refinements and distant instances reuse these imported meshes. Image generation supplied the selected reference and surface textures; no generated bitmap is used as a substitute for the running scene.

To rebuild the final scene in a fresh place, import `Lumenwild_Refined.glb` through Studio's 3D Importer with separate objects, scene positioning, anchored meshes, and textures enabled. The tested importer used Front/Top orientation and produced a 180-degree Y rotation; `tools/configure_studio.luau` corrects that once, restores object names from model wrappers, extracts the traveler, and applies material defaults. Run it in Edit mode, followed by `tools/finish_materials.luau` and `tools/final_lighting.luau`. Set LightingStyle to Realistic and PrioritizeLightingQuality to true through Properties; those writes are protected from MCP in the tested Studio version. Preserve the service scripts and sync connections.

The final full GLB already contains waterfall placement, the curved hero tree, and the distant forest. Do not apply the incremental `align_waterfalls`, `install_tree_patch`, or `forest_depth` Luau patches to a fresh final import. They document how the earlier imported revision was updated.

Blender authoring scripts in `tools` record the production sequence: `build_forest.py`, `refine_forest.py`, `polish_tree.py`, `align_waterfalls.py`, `forest_depth.py`, `final_textures.py`. They are intended to run through Blender MCP, in that order, from a clean working copy of the source. They use this workspace's absolute path. Re-running early generators in a populated file creates additional scenes; use the saved final source for ordinary editing.

## Asset IDs

`Assets/roblox-asset-manifest.json` records the actual saved mesh and SurfaceAppearance IDs. Key detail maps:

| Texture | Roblox asset ID |
| --- | --- |
| Wet basalt color | `91629842365012` |
| Wet basalt normal | `76678769460493` |
| Ancient bark color (MeshPart.TextureID) | `104380993895241` |
| Water normal | `98564679456510` |
| Forest leaves color (MeshPart.TextureID) | `107640576041100` |

Reimporting can create different mesh/image IDs. The saved place and manifest are authoritative for this delivery. Wet floors use supported SurfaceAppearance roughness, normals, environment specular, and lighting; this is not a custom planar-reflection renderer.

## Validation and limits

Testing was performed only on this desktop in Roblox Studio 0.738.0.7381393. The target viewport was 1919 × 1080, Realistic lighting, manual graphics quality 10. Frame times are measured with the client's render-step delta after a five-second warmup, over at most 3,600 frames. They measure Studio Play behavior, not a standalone published-client benchmark.

Observed controls include click movement and arrival, clamping a click beyond X=4.5 to the bridge boundary, drag orbit, scroll zoom, and lazy camera follow. The traveler has procedural walking/idle motion; foliage, mist, foam, fireflies, and lantern flicker are client effects. Final measured frame-time and visual-critique results are recorded in `docs/validation.json` and `docs/progress.md`.

The final 3,600-frame sample averaged **60.00 FPS**, with **17.70 ms p95** and **18.24 ms p99**, on an **i5-12600KF / RTX 3080** desktop. The final independent visual match was **3.8/10**, improved from 2.0/10 but below the Dream Loop acceptance threshold. The actual Play screenshot is `docs/Lumenwild-runtime.png`.

Texture recovery preserved the importer's `MeshPart.TextureID` for albedo-only bark/foliage and `SurfaceAppearance` for PBR materials. Bark and foliage returned successful asset loads and displayed in Play. Individual PBR normal-map preload probes returned failure; the saved bindings and visible wet response do not independently prove every normal map loaded. Cross-account asset access is unverified.

The generated target remains more intricate than this timeboxed implementation. Remaining gaps include natural waterfall silhouettes, dense irregular roots and foliage, castle detail, atmospheric depth, and a closer material/lighting match. A 60 FPS average does not establish a perfectly stable 16.67 ms frame budget. Mobile, console, VR, other computers, and published-client behavior were outside scope.

The user selected the enchanted forest and restarted the one-hour budget at 2026-09-13 14:27:02 UTC; the final stop time is 15:27:02 UTC. Earlier cathedral planning is superseded.

## Official references used

- [Roblox documentation index](https://create.roblox.com/docs/llms.txt)
- [File Script Sync](https://create.roblox.com/docs/en-us/scripting/sync)
- [3D Importer](https://create.roblox.com/docs/en-us/studio/importer)
- [Lighting](https://create.roblox.com/docs/en-us/environment/lighting)
- [SurfaceAppearance](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance)
