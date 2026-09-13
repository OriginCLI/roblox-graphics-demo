# Drowned Reliquary production record

- Started: 2026-09-13 14:15:11 UTC. Hard deadline: 15:15:11 UTC.
- Save/review/commit/push reserve begins at 15:08 UTC.
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
