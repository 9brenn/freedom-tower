"""Create and verify a standalone OPEN RPF7 DLC using prepared resources."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as E
import rpf7
base=Path('/workspace/conversion');stage=base/'stage'
files={p.name:p.read_bytes() for p in sorted(stage.iterdir())}
inner=rpf7.build(files);read=rpf7.read(inner)
assert read==files
content=Path(__file__).with_name('content.xml').read_bytes();setup=Path(__file__).with_name('setup2.xml').read_bytes()
outerfiles={'content.xml':content,'setup2.xml':setup,'x64/levels/gta5/freedomtower.rpf':inner}
outer=rpf7.build(outerfiles);check=rpf7.read(outer);assert check==outerfiles
registered=E.fromstring(content);setuproot=E.fromstring(setup)
prefix='dlc_freedomtower:/'
for i in registered.findall('./dataFiles/Item'):
 name=i.findtext('filename');assert name.startswith(prefix)
 path=name[len(prefix):]
 if '.rpf/' in path:
  archive,member=path.split('.rpf/',1);assert archive+'.rpf' in check and member in read
 else:assert path in check
refs=[x.text for x in registered.findall('./contentChangeSets/Item/filesToEnable/Item')]
assert set(refs)==set(i.findtext('filename') for i in registered.findall('./dataFiles/Item'))
assert len(registered.findall('./dataFiles/Item'))==16
assert len([n for n in read if n.endswith('.ytyp')])==15
assert '_manifest.ymf' in read
out=base/'package/mods/update/x64/dlcpacks/freedomtower/dlc.rpf';out.write_bytes(outer)
json.dump({'rpf7_open':True,'resources':len(files),'all_members_readback_equal':True,'content_paths_valid':True,'registered_ytyp':15,'bytes':len(outer),'sha256':hashlib.sha256(outer).hexdigest()},open(base/'reports/package_check.json','w'),indent=2)
print(out,len(outer))
