"""Build preparation for the supplied Robbbs3D FiveM map. Original files untouched.
Requires XML exports from CodeWalker and a CLI capable of `compile xml rsc/pso out`.
"""
import copy,hashlib,json,math,os,shutil,subprocess,sys
from pathlib import Path
import xml.etree.ElementTree as E
BASE=Path('/workspace/conversion')
SRC=BASE/'source/extracted/Robbbs3D - freedom_tower/stream'
XML=BASE/'reports/xml'
BUILD=Path(os.environ.get('FREEDOM_TOWER_BUILD_DIR',str(BASE/'rc3')))
BUILD.mkdir(parents=True,exist_ok=True)
STAGE=BUILD/'stage';STAGE.mkdir(exist_ok=True)
PATCH=BUILD/'patched-xml';PATCH.mkdir(exist_ok=True)
REPORTS=BUILD/'reports';REPORTS.mkdir(exist_ok=True)
EXTERNAL_YTYPS={'sf_dlc_int_01_sec'}
CLI=['/workspace/tools/dotnet/dotnet',str(BASE/'auditor/bin/Release/net8.0/Auditor.dll')]
changes=[{'file':'sf_dlc_int_01_sec.ytyp','field':'packaged stock definitions','after':'use installed mpsecurity YTYP; omit duplicate registration and interior manifest'}]
# The stage is generated; remove stale stock copies when rerunning this build.
for stock in EXTERNAL_YTYPS:(STAGE/(stock+'.ytyp')).unlink(missing_ok=True)
def save_xml(root,path):
 E.indent(root,space=' ');E.ElementTree(root).write(path,encoding='UTF-8',xml_declaration=True)
def compile_xml(root,name,fmt='rsc'):
 p=PATCH/(name+'.xml');save_xml(root,p)
 subprocess.run(CLI+['compile',str(p),fmt,str(STAGE/name)],check=True,stdout=subprocess.DEVNULL)
def h(name):
 if name.startswith('hash_'):return int(name[5:],16)
 n=0
 for c in name.lower().encode():
  n=(n+c)&0xffffffff;n=(n+(n<<10))&0xffffffff;n^=n>>6
 n=(n+(n<<3))&0xffffffff;n^=n>>11;n=(n+(n<<15))&0xffffffff;return n
for f in SRC.iterdir():
 if f.stem in EXTERNAL_YTYPS and f.suffix=='.ytyp':continue
 if f.suffix not in ('.cwproj','.ymf','.ymt','.ynd'):shutil.copy2(f,STAGE/f.name.lower())
# Path nodes are registered separately; scenario source is retained separately, not
# installed as a global legacy-1604 manifest over a modern game configuration.
for f in SRC.glob('*.ynd'):shutil.copy2(f,STAGE/f.name)
# These visual drawables have neither an embedded Bound nor a matching YBN.
# The tower/hall retain their separate world/MLO collision files.
DANGLING_CUSTOM_PHYSICS={
 'onewtc', 'robbbs_wtc_lobby_ascensori', 'robbbs_wtc_lobby_mirror',
 'robbbs_wtc_lobby_luci', 'robbbs_wtc_lobby_quadri', 'robbbs_wtc_impexp_roundlights'}
physics={
 'robbbs_wtc_appartment_01_dlc':'robbbs_wtc_appartment_01_dlc',
 'robbbs_wtc_appartment_03_dlc':'robbbs_wtc_appartment_03_dlc',
 'robbbs_wtc_appartment_04_dlc':'robbbs_wtc_appartment_04_dlc',
 'robbbs_wtc_int_office_01a_dlc':'robbbs_wtc_int_office_01a_dlc'}
roots={};archindex={};mlos=[]
for f in sorted(XML.glob('*.ytyp.xml')):
 root=E.parse(f).getroot();name=f.name[:-4];changed=False
 # A copied CMapTypes name must not collide with a stock YTYP or another local file.
 expected=name[:-5]
 if root.findtext('name')!=expected and name!='sf_dlc_int_01_sec.ytyp':
  changes.append({'file':name,'field':'CMapTypes.name','before':root.findtext('name'),'after':expected})
  root.find('name').text=expected;changed=True
 for a in list(root.findall('./archetypes/Item')):
  an=a.findtext('name')
  # Same shell is already defined in hall_mlo; keep one canonical definition.
  if name=='robbbs_wtc_hall_prop.ytyp' and an=='robbbs_wtc_hall_shell':
   root.find('archetypes').remove(a);changed=True
   changes.append({'file':name,'field':'duplicate archetype','removed':an});continue
  if an in DANGLING_CUSTOM_PHYSICS:
   assert a.findtext('physicsDictionary')==an
   assert not (SRC/(an+'.ybn')).exists()
   a.find('physicsDictionary').text=None;changed=True
   changes.append({'file':name,'field':an+'.physicsDictionary','before':an,'after':None,'reason':'no matching YBN or embedded Bound; separate world/MLO collisions retained'})
  archindex[h(an)]=(name[:-5],a)
  if a.get('type')=='CMloArchetypeDef':
   if an in physics:
    old=a.findtext('physicsDictionary');a.find('physicsDictionary').text=physics[an];changed=True
    changes.append({'file':name,'field':an+'.physicsDictionary','before':old,'after':physics[an]})
   if name!='sf_dlc_int_01_sec.ytyp':
    # Union of authored finite room bounds; skip empty inverted garage limbo.
    bounds=[]
    for r in a.findall('./rooms/Item'):
     lo=[float(r.find('bbMin').get(k)) for k in 'xyz'];hi=[float(r.find('bbMax').get(k)) for k in 'xyz']
     if all(math.isfinite(v) and abs(v)<1e6 for v in lo+hi) and all(x<=y for x,y in zip(lo,hi)):bounds.append((lo,hi))
    assert bounds
    lo=[min(b[0][i] for b in bounds)-0.5 for i in range(3)];hi=[max(b[1][i] for b in bounds)+0.5 for i in range(3)]
    centre=[(x+y)/2 for x,y in zip(lo,hi)];rad=math.sqrt(sum((y-x)**2 for x,y in zip(lo,hi)))/2
    for tag,vec in [('bbMin',lo),('bbMax',hi),('bsCentre',centre)]:
     a.find(tag).attrib={k:format(v,'.9g') for k,v in zip('xyz',vec)}
    a.find('bsRadius').set('value',format(rad,'.9g'));changed=True
    changes.append({'file':name,'field':an+'.bounds','reason':'replace zero culling bounds with finite room union'})
   if name[:-5] not in EXTERNAL_YTYPS:mlos.append((name[:-5],a))
 roots[name[:-5]]=root
 if changed:compile_xml(root,name)
# Merge existing real game YTYP dependencies, including original DLC props.
manifest=E.Element('CPackFileMetaData')
for tag,typ in [('MapDataGroups','CMapDataGroup'),('HDTxdBindingArray','CHDTxdAssetBinding'),('imapDependencies','CImapDependency'),('imapDependencies_2','CImapDependencies'),('itypDependencies_2','CItypDependencies'),('Interiors','CInteriorBoundsFiles')]:
 E.SubElement(manifest,tag,{'itemType':typ})
merged={'imapDependencies_2':{},'itypDependencies_2':{}}
for f in sorted(XML.glob('*.ymf.xml')):
 root=E.parse(f).getroot()
 for tag,key in [('imapDependencies_2','imapName'),('itypDependencies_2','itypName')]:
  for item in root.findall('./'+tag+'/Item'):
   k=item.findtext(key)
   if tag=='itypDependencies_2' and k in EXTERNAL_YTYPS:continue
   if k not in merged[tag]:merged[tag][k]=copy.deepcopy(item)
   else:
    a=merged[tag][k].find('itypDepArray');existing={h(i.text) for i in a}
    for i in item.findall('./itypDepArray/Item'):
     if h(i.text) not in existing:a.append(copy.deepcopy(i));existing.add(h(i.text))
# Correct/complete custom YMAP -> local YTYP links. Preserve original stock deps.
exterior_deps=set()
for item in merged['imapDependencies_2'].values():
 if item.findtext('manifestFlags')!='INTERIOR_DATA':
  exterior_deps.update(i.text for i in item.findall('./itypDepArray/Item'))
for f in sorted(XML.glob('*.ymap.xml')):
 name=f.name[:-9]
 if name.startswith(('hei_','vw_')):continue # stock dependency manifests remain authoritative
 root=E.parse(f).getroot();is_mlo=bool(root.findall('./entities/Item[@type="CMloInstanceDef"]'))
 if name not in merged['imapDependencies_2']:
  item=E.Element('Item');E.SubElement(item,'imapName').text=name
  E.SubElement(item,'manifestFlags').text='INTERIOR_DATA' if is_mlo else None
  E.SubElement(item,'itypDepArray');merged['imapDependencies_2'][name]=item
 item=merged['imapDependencies_2'][name];arr=item.find('itypDepArray');existing={h(i.text) for i in arr}
 deps=set()
 for e in root.findall('./entities/Item'):
  a=archindex.get(h(e.findtext('archetypeName')))
  if a:deps.add(a[0])
 if name=='one_wtc_pali':deps.update(exterior_deps)
 for dep in sorted(deps):
  if h(dep) not in existing:E.SubElement(arr,'Item').text=dep;existing.add(h(dep))
# Add all local references inside MLOs, keeping existing stock dependency lists.
for name,a in mlos:
 if name not in merged['itypDependencies_2']:
  item=E.Element('Item');E.SubElement(item,'itypName').text=name
  E.SubElement(item,'manifestFlags').text='INTERIOR_DATA';E.SubElement(item,'itypDepArray')
  merged['itypDependencies_2'][name]=item
 item=merged['itypDependencies_2'][name];arr=item.find('itypDepArray');existing={h(i.text) for i in arr}
 for e in a.findall('.//entities/Item'):
  an=e.findtext('archetypeName');dep=archindex.get(h(an)) if an else None
  if dep and dep[0]!=name and h(dep[0]) not in existing:E.SubElement(arr,'Item').text=dep[0];existing.add(h(dep[0]))
 interior=E.SubElement(manifest.find('Interiors'),'Item');E.SubElement(interior,'Name').text=a.findtext('name')
 E.SubElement(E.SubElement(interior,'Bounds'),'Item').text=a.findtext('physicsDictionary')
for tag in merged:
 for name,item in sorted(merged[tag].items()):manifest.find(tag).append(item)
compile_xml(manifest,'_manifest.ymf','pso')
# Explicitly enable useful, mutually compatible furniture/decoration sets.
for mapname,selections in {
 'robbbs_wtc_office':['office_chairs'],
 'robbs_wtc_office_03':['office_chairs'],
 'robbbs_wtc_office_02':['entity_set_standard_office','entity_set_wpaper_1','entity_set_art_1','entity_set_tint_ag']}.items():
 r=E.parse(XML/(mapname+'.ymap.xml')).getroot()
 for ent in r.findall('./entities/Item[@type="CMloInstanceDef"]'):
  _,a=archindex[h(ent.findtext('archetypeName'))]
  sets={s.findtext('name'):i for i,s in enumerate(a.findall('./entitySets/Item'))}
  assert all(s in sets for s in selections)
  arr=ent.find('defaultEntitySets');arr.clear()
  for selection in selections:E.SubElement(arr,'Item').text=selection
 compile_xml(r,mapname+'.ymap')
 changes.append({'file':mapname+'.ymap','field':'defaultEntitySets','after':selections})
json.dump(changes,open(REPORTS/'conversion_changes.json','w'),indent=2)
# A complete input inventory permits proof that no models or interiors were dropped.
json.dump([{ 'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(SRC.iterdir())],open(REPORTS/'source_inventory.json','w'),indent=2)
print('Prepared',len(list(STAGE.iterdir())),'files;',len(changes),'changes; MLOs',len(mlos))
