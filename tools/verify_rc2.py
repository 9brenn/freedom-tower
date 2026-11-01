"""Check the isolated RC2 compatibility change against the published RC1 ZIP."""
from pathlib import Path
import json,sys,xml.etree.ElementTree as E,zipfile
import rpf7

def h(value):
 if value.startswith('hash_'):return int(value[5:],16)
 n=0
 for c in value.lower().encode():
  n=(n+c)&0xffffffff;n=(n+(n<<10))&0xffffffff;n^=n>>6
 n=(n+(n<<3))&0xffffffff;n^=n>>11;return (n+(n<<15))&0xffffffff

old=Path(sys.argv[1]);new=Path(sys.argv[2]);manifest=Path(sys.argv[3])
with zipfile.ZipFile(old) as z:old_outer=rpf7.read(z.read('mods/update/x64/dlcpacks/freedomtower/dlc.rpf'))
new_outer=rpf7.read(new.read_bytes());key='x64/levels/gta5/freedomtower.rpf'
a=rpf7.read(old_outer[key]);b=rpf7.read(new_outer[key])
assert set(a)-set(b)=={'sf_dlc_int_01_sec.ytyp'}
assert not set(b)-set(a)
assert {k for k in a.keys()&b.keys() if a[k]!=b[k]}=={'_manifest.ymf'}
assert old_outer['setup2.xml']==new_outer['setup2.xml']
old_content=E.fromstring(old_outer['content.xml']);new_content=E.fromstring(new_outer['content.xml'])
for parent,tag in [(old_content.find('dataFiles'),'filename'),(old_content.find('./contentChangeSets/Item/filesToEnable'),None)]:
 for item in list(parent):
  value=item.findtext(tag) if tag else item.text
  if value and value.endswith('/sf_dlc_int_01_sec.ytyp'):parent.remove(item)
def tree(e):return (e.tag,tuple(sorted(e.attrib.items())),(e.text or '').strip(),tuple(tree(c) for c in e))
assert tree(old_content)==tree(new_content)
r=E.parse(manifest).getroot();sf=h('sf_dlc_int_01_sec')
assert len(r.findall('./Interiors/Item'))==8
assert all(h(i.findtext('itypName'))!=sf for i in r.findall('./itypDependencies_2/Item'))
assert all(h(i.findtext('Name'))!=h('sf_dlc_office_sec') for i in r.findall('./Interiors/Item'))
office=next(i for i in r.findall('./imapDependencies_2/Item') if h(i.findtext('imapName'))==h('robbbs_wtc_office_02'))
assert any(h(i.text)==sf for i in office.findall('./itypDepArray/Item'))
assert len([n for n in b if n.endswith('.ytyp')])==14
print('RC2_REGRESSION_OK: 9 placement maps and all models retained; only stock copy/registrations removed')
