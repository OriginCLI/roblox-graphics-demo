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


## Enchanted forest refinement
- Rebuilt the plaza as a narrow diagonal bridge to a giant arched tree shrine. Added curved editable trunk/root meshes, distant arches, five aligned waterfall groups, purple plants, textured wet paving, packed bark/water/foliage maps, and ten additional cliff/tree groups.
- Final Blender scene: 357 mesh objects and 270,046 evaluated triangles. All visible geometry originates in Blender 5.1.2. Earlier scenes and Studio imports are preserved.
- Independent second judge: 3.5/10 (composition 1.5, lighting 0.8, materials 0.9, details 0.3), versus 2.0/10 initially. Main remaining gap was isolated platforms on open water; the final depth pass adds layered forest cliffs. This score predates final textures and depth refinement.
- At manual graphics quality 10, Realistic lighting, 1919x1080 Play viewport, the pre-final-texture forest measured 60.0013 mean FPS over 3,600 frames; p95 17.8061ms, p99 18.3568ms. This supports an approximately 60fps average, not a perfectly stable 16.67ms budget.
- Test desktop: Intel Core i5-12600KF, NVIDIA GeForce RTX 3080, driver 32.0.15.9649, 34,117,980,160 bytes installed physical memory reported by Windows.
- Boundary click tested against world point (5.2,0.16,0): destination clamped to (4.5,0.16,-0.000655), arrived within the 0.12-stud stopping tolerance. Drag orbit fixed to use pointer displacement and verified from yaw 0.610865 to 0.251089 radians. Scroll and lazy follow were also observed in Play.
- Final full GLB is being reimported with material-linked UVs; final saved-place results follow in validation.json. Initial two milestone commits were successfully pushed to origin/dream-loop/demo at about 15:13 UTC.

## Final verification and delivery checkpoint
- Final independent judge: 3.8/10 (composition 1.6, lighting 0.8, materials 1.0, details 0.4). Visual target fidelity is NOT accepted. Final actual Play screenshot: docs/Lumenwild-runtime.png.
- Resolved blank/white textures by preserving importer MeshPart.TextureID for albedo-only bark/foliage, instead of adding a SurfaceAppearance that hid them. Bark and foliage asset loads then returned Success. PBR map IDs are retained from the importer; separate normal-map preload probes returned Failure, so individual normal-map delivery remains unverified.
- Final runtime: 340 environment MeshParts, 17 local traveler MeshParts. Realistic lighting, PrioritizeLightingQuality true, streaming false. Source GLB: 357 mesh nodes, 287 mesh definitions, all 287 primitives with UVs, 26 materials and 10 embedded images.
- Final 3600-frame sample: mean 60.0013 FPS, p95 17.7047ms, p99 18.2369ms at Manual10 and 1919x1080. Final control tests verified arrival at the clamped boundary, non-bridge click rejection, orbit and zoom. Console output empty.
- Latest place saved at 15:19:03 UTC, 2,308,571 bytes; Studio reported the exact local path. Asset manifest records all357 mesh entries and6 distinct PBR surface sets.
- Source files and packed art are being reviewed and committed for the final push. Remaining limitations are documented in README and validation.json, including visual fidelity, individual PBR map loading, camera occlusion, and untested published/cross-account behavior.

## Saved-file verification
- Delivery commit 3b1b4b8 was pushed successfully with 66MB of LFS assets. Local HEAD matched origin/dream-loop/demo, worktree was clean, and git lfs fsck passed.
- At 15:22:42 UTC, verified a real disk reopen: closed the place to Studio Home, opened Places/Lumenwild.rbxl, and entered Play. All340 environment meshes and17 traveler meshes persisted, as did the texture bindings, Realistic lighting, streaming settings and FocusOffset(-6,8,-10). Traveler and environmental motion ran; console empty. Reopened viewport was1920x1078 at Manual10.
- Visual fidelity remains below target at3.8/10; the completed delivery is a timeboxed playable graphics prototype, not a claim that the generated target was matched.
