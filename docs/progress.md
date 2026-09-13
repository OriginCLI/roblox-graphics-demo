# Lumenwild production record

- Original start: 14:15:11 UTC. User reset the full hour after selecting enchanted forest. Restart: 2026-09-13 14:27:02 UTC. New hard deadline: 15:27:02 UTC.
- Save/review/commit/push reserve begins at 15:20 UTC.
- Initial Git: clean `dream-loop/demo`, tracking `origin/dream-loop/demo`.
- Existing service folders and `StarterPlayer/INFO.md` inspected. StarterPlayer itself is not synced; its script containers are.
- Native Blender MCP connected, Blender 5.1.2, unsaved default scene. Preserve default scene and build in a dedicated scene.
- Native Studio MCP connected to Place1, version 0.738.0.7381393, unpublished baseplate. LightingStyle exists and was Soft.
- Dream Loop Pro workflow selected from account tier. Original brief requires Blender modeling, overriding external/generated 3D asset sourcing. Image generation supplies target and textures.

## Design

The Drowned Reliquary: bounded wet cathedral terrace with a cloaked knight, broken gothic arch and amber crystal, braziers, ruined towers, layered mist, banners and dead trees. Blue dusk and restrained amber focal lighting. Desktop only, no gameplay.

## Evidence gates

1. Generated target saved in ignored `.dream-loop/target.png`.
2. Editable Blender meshes and exports, bounds and triangle counts inspected.
3. Imported meshes and materials verified in Studio.
4. Actual Play mode screenshot independently critiqued against target.
5. Click movement, drag rotation, scroll zoom and lazy follow verified in Play mode.
6. Desktop frame-time sample and quality/viewport context recorded; 60fps target is unverified until measured.
7. Place saved, readable scripts synchronized, staged diff reviewed, milestones committed, final branch pushed.

## Official references

- https://create.roblox.com/docs/llms.txt (index dated September 11, 2026)
- https://create.roblox.com/docs/en-us/scripting/sync.md
- https://create.roblox.com/docs/en-us/studio/importer.md
- https://create.roblox.com/docs/en-us/environment/lighting.md
- https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md

Importer supports FBX/glTF, PBR, separate named meshes, scene positioning and anchored imports. Script Sync maps `.luau` to ModuleScript and `.local.luau` to LocalScript. Realistic lighting and environment specular are documented and will be verified live. Wet surfaces use supported PBR/specular shading; no claim of arbitrary planar mirror reflections.

## Direction selection
At 14:20 UTC user requested a different world style, then five separate concept images to choose from. Scene modeling is paused pending selection. General controls have been authored and file-to-Studio synchronization verified for all three scripts; runtime behavior is not yet tested. The original cathedral target is superseded.


## Selected direction
At 14:27:02 UTC user selected enchanted forest concept and explicitly reset the one-hour timer. New deadline 15:27:02 UTC. Lumenwild: giant voxel canopies, wet mossy pilgrim paths, a turquoise waterfall and stream, cyan mushrooms, old stone shrine and amber lanterns. The selected generated concept is the visual target; all geometry will be built in Blender.


## First playable and critique
- Blender first pass: 204 mesh objects / 73,656 evaluated triangles. Default Blender scene preserved. GLB import succeeded with uploaded mesh and PBR texture IDs.
- Import Front/Top rotated geometry 180 degrees around Y; verified and corrected. Mesh names came from data blocks under named model wrappers, so setup restores object names and materials.
- Realistic lighting selected through Studio Properties (MCP writes are protected); verified live. PrioritizeLightingQuality is true.
- First Play exposed missing streamed world with custom avatar disabled. Disabled streaming in Edit and made world persistent; subsequent Play verified all 187 environment meshes and 17-part local traveler.
- Actual 1080p viewport sample around 60fps, but full sustained performance acceptance remains open. Console empty. Click movement and wheel zoom verified; drag delta fix authored and awaits retest.
- Independent Dream Loop judge scored runtime-01 2.0/10 (composition0.5 lighting0.7 materials0.6 details0.2). Main gaps: square plaza instead of diagonal bridge, missing giant tree shrine and ravine, rigid waterfall, oversimple canopy, cool flat lighting. Major composition rebuild underway.

