"""Build a map-level DLC with separate assets and CONTENTS_DLC_MAP_DATA archives."""
from pathlib import Path
import hashlib,json,os,xml.etree.ElementTree as E
import rpf7
base=Path(os.environ.get('FREEDOM_TOWER_BUILD_DIR','/workspace/conversion/rc3'));stage=base/'stage'
files={p.name:p.read_bytes() for p in sorted(stage.iterdir())}
map_exts={'.ymap','.ytyp','.ymf'}
metadata={n:b for n,b in files.items() if Path(n).suffix in map_exts}
assets={n:b for n,b in files.items() if Path(n).suffix not in map_exts}
assert set(metadata).isdisjoint(assets) and metadata|assets==files
assert all(Path(n).suffix in {'.ydr','.ydd','.ybn','.ynd'} for n in assets)
assert len([n for n in metadata if n.endswith('.ytyp')])==14
assert len([n for n in metadata if n.endswith('.ymap')])==41
assert '_manifest.ymf' in metadata and 'sf_dlc_int_01_sec.ytyp' not in metadata
inners={'x64/levels/gta5/freedomtower.rpf':rpf7.build(assets),
        'x64/levels/gta5/freedomtower_metadata.rpf':rpf7.build(metadata)}
assert rpf7.read(inners['x64/levels/gta5/freedomtower.rpf'])==assets
assert rpf7.read(inners['x64/levels/gta5/freedomtower_metadata.rpf'])==metadata
content=Path(__file__).with_name('content.xml').read_bytes();setup=Path(__file__).with_name('setup2.xml').read_bytes()
outerfiles={'content.xml':content,'setup2.xml':setup,**inners}
outer=rpf7.build(outerfiles);check=rpf7.read(outer);assert check==outerfiles
registered=E.fromstring(content);setuproot=E.fromstring(setup)
assert setuproot.findtext('type')=='EXTRACONTENT_LEVEL_PACK'
assert setuproot.find('isLevelPack').get('value')=='true'
assert not registered.findall('./dataFiles/Item[fileType="DLC_ITYP_REQUEST"]')
items=registered.findall('./dataFiles/Item');assert len(items)==2
for i in items:
 name=i.findtext('filename');assert name.startswith('dlc_freedomtower:/')
 path=name.removeprefix('dlc_freedomtower:/').replace('%PLATFORM%','x64')
 assert path in check and i.findtext('fileType')=='RPF_FILE'
 if path.endswith('_metadata.rpf'):assert i.findtext('contents')=='CONTENTS_DLC_MAP_DATA'
refs=[x.text for x in registered.findall('./contentChangeSets/Item/filesToEnable/Item')]
assert set(refs)=={i.findtext('filename') for i in items}
changeset=registered.findtext('./contentChangeSets/Item/changeSetName')
streaming=setuproot.find('./contentChangeSetGroups/Item[NameHash="GROUP_UPDATE_STREAMING"]/ContentChangeSets')
assert streaming is not None and changeset in [i.text for i in streaming]
assert not list(setuproot.find('./contentChangeSetGroups/Item[NameHash="GROUP_STARTUP"]/ContentChangeSets'))
out=base/'package/mods/update/x64/dlcpacks/freedomtower/dlc.rpf';out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(outer)
report={'layout':'map-level DLC','metadata_resources':len(metadata),'asset_resources':len(assets),
        'all_members_readback_equal':True,'content_paths_valid':True,'explicit_ytyp_requests':0,
        'streamed_ytyp':14,'ymap':41,'bytes':len(outer),'sha256':hashlib.sha256(outer).hexdigest()}
(base/'reports').mkdir(exist_ok=True)
json.dump(report,open(base/'reports/package_check.json','w'),indent=2)
print(out,report)
