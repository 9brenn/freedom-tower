# Independent DLC mount research after RC1/RC2 crashes

## Evidence and limits

No runtime GTA process is available. Silent crash is confirmed by user on Legacy
1.0.3889.0 with RC1 and RC2, no optional loader; removing DLC list entry restores
Story Mode. These facts identify active DLC as trigger but do not identify one
individual file or explain whether installation or game pools contribute.

The prior archive reader passes do not validate native map activation lifecycle.
CodeWalker parses `contents` in DlcContentFile.cs, but its GameFileCache activates
all registered RPFs as potential map archives and does not enforce the game's
CONTENTS_DLC_MAP_DATA handling.

## Concrete difference from an established map DLC creator

Trusted source reference (read only):
https://github.com/FiftyShadesOfBlue/DlcPackCreator/blob/a12c16b2344894738bfff2594b120668d4be6ecb/DlcCreator_sln/DlcCreator/Utils/GenerateMetaData.cs

This is the 2018 Dlc Pack Creator map template, not a hypothetical newly invented
format. Its code uses:
- two RPFs: assets and `_metadata`;
- RPF_FILE on both; CONTENTS_DLC_MAP_DATA specifically on metadata;
- EXTRACONTENT_LEVEL_PACK and isLevelPack=true;
- GROUP_UPDATE_STREAMING activation with `$level=MO_JIM_L11` condition;
- overlay=false, disabled=false, persistent=false;
- no forced list of DLC_ITYP_REQUESTs in GROUP_STARTUP.

RC1/RC2 instead used vehicle-style EXTRACONTENT_COMPAT_PACK, isLevelPack=false,
GROUP_STARTUP, 14/15 forced persistent YTYP requests, one undifferentiated RPF,
and no CONTENTS_DLC_MAP_DATA. This is a concrete mismatch in supported packaging,
not proof any one field by itself caused the reported crash.

CodeWalker PsoTypes.cs confirms CONTENTS_DLC_MAP_DATA is a recognized native
content category (enum value 8), not an invented XML flag.

Additional independent implementation corroborating metadata allocation:
https://github.com/avrefdev/hane-dlc-pack-creator/blob/main/src-tauri/src/pack.rs
Its README describes itself as a rewrite of skylumz Dlc Pack Creator 1.1 and
explicitly partitions map ymap/ytyp/ymf into metadata and drawables/bounds into
assets. This newer source is corroboration, not a replacement for runtime testing.

## Exact candidate templates

`content-map.xml` and `setup2-map.xml` in this directory follow the established
map structure. Only actual change sets are referenced; empty native groups have
empty ContentChangeSets, avoiding the old tool's dangling INIT/STREAMING/TEXT
placeholder names.

The candidate keeps order=10000 from previous packages to avoid changing resource
priority while testing lifecycle changes. Original 2018 tool uses order=2. Keeping
10000 is a documented deliberate deviation, not part of reference-template proof.

For this exact source, partition the corrected RC2 files as follows:
- freedomtower_metadata.rpf: 41 YMAP + 14 custom YTYP + `_manifest.ymf` = 56 files.
- freedomtower.rpf: 40 YDR + 1 YDD + 14 YBN + 2 YND = 57 files.
- Preserve all 113 files and their bytes; no deletion of interiors is implied.
- Original stock Agency YTYP remains a game dependency, not a local copy.
- `_manifest.ymf` belongs in metadata alongside YMAP/YTYP dependencies; bounds
  referenced by Interiors are streaming assets discoverable by hash in asset RPF.
- No user textures YTD exist; if they existed, their allocation would require
  supported streaming setup but it does not affect this particular source.

Empty MapDataGroups is normal: CodeWalker's own manifest generator emits it empty
while generating YMAP/ityp dependencies and Interiors. Existing source manifests
also have no authored MapDataGroups. Do not invent map groups or extents.

## Specific FiveM-only automatic repairs worth auditing in assets

Authoritative native implementation:
https://github.com/citizenfx/fivem/blob/master/code/components/gta-streaming-five/src/LoadStreamingFile.cpp
Local snapshot: LoadStreamingFile.cpp in this directory.

At fwMapDataStore__FinishLoadingHook, FiveM automatically:
- sets contentFlags bit 8 when CMloInstanceDef exists;
- clamps DistantLODLightsSOA.numStreetLights to positions.Count;
  comments identify native crash signatures in builds 2699 and 2802.

These repairs do not exist in an ordinary Single Player environment. A resource
that starts on FiveM can therefore still have native-crashing metadata in SP.
The existence of those repairs is concrete; they must be checked against this
archive before claiming they caused this crash.

FiveM also has a proxy DLC_ITYP_REQUEST mounter which releases existing slots and
reconciles permanent types and manifest-required YTYPs; blindly copying FiveM
mount calls into native SP startup is not equivalent behavior.

## Installation boundary

OPEN archives require working OpenIV.asi. Successful Git/file-parser checks do
not prove the user's installed ASI works on this particular Legacy build.
The provided asset-free probe remains a useful discriminator before assigning
an asset-specific cause. A probe failure does not identify a model bug.

No evidence establishes missing extrafolderMountData or extraTitleUpdateData as
an error in this standalone DLC namespace. Neither established map template
requires them. Do not add arbitrary base mounts as a speculative workaround.
