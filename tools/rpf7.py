"""Unencrypted GTA V RPF7 writer/readback, based on CodeWalker RpfFile.cs.
Accepts a mapping of slash-delimited archive paths to bytes. Nested .rpf payloads
must already be built. Resource data must include its full RSC7 header.
"""
from pathlib import PurePosixPath
import struct,zlib

MAGIC=0x52504637
OPEN=0x4e45504f

def pad(n,alignment): return (n+alignment-1)//alignment*alignment

def build(files):
    root={'name':'','children':{}}
    for path,data in files.items():
        parts=PurePosixPath(path).parts
        if not parts or any(p in ('','..','.') for p in parts) or path.startswith('/'):
            raise ValueError('invalid RPF path '+path)
        node=root
        for p in parts[:-1]:
            node=node['children'].setdefault(p,{'name':p,'children':{}})
            if 'children' not in node:raise ValueError('file/directory collision')
        name=parts[-1]
        if name in node['children']:raise ValueError('duplicate path '+path)
        node['children'][name]={'name':name,'data':data}
    entries=[root];stack=[root]
    while stack:
        d=stack.pop();cs=[d['children'][k] for k in sorted(d['children'])]
        d['start']=len(entries);d['count']=len(cs);entries+=cs
        for c in cs:
            if 'children' in c:stack.append(c)
    names=bytearray();offsets={}
    for e in entries:
        name=e['name']
        if name not in offsets:
            offsets[name]=len(names);names.extend(name.encode('ascii')+b'\0')
        e['no']=offsets[name]
        if e['no']>0xffff:raise ValueError('names table overflow')
    names.extend(b'\0'*(pad(len(names),16)-len(names)))
    headsz=pad(16+16*len(entries)+len(names),512)
    payload=bytearray();table=bytearray()
    for e in entries:
        if 'children' in e:
            table.extend(struct.pack('<4I',e['no'],0x7fffff00,e['start'],e['count']))
            continue
        data=e['data'];block=(headsz+len(payload))//512
        resource=data[:4]==b'RSC7'
        if resource:
            if len(data)>=0xffffff:raise ValueError('oversized resource not supported')
            _,version,sf,gf=struct.unpack_from('<4I',data)
            packed=e['no'] | (len(data)<<16) | ((block|0x800000)<<40)
            table.extend(struct.pack('<QII',packed,sf,gf));out=data
        else:
            # Keep nested archives directly readable. Compress normal binary files.
            if e['name'].lower().endswith(('.rpf','.awc')):
                out=data;cs=0
            else:
                compressor=zlib.compressobj(9,zlib.DEFLATED,-15)
                out=compressor.compress(data)+compressor.flush();cs=len(out)
                if cs>0xffffff:out=data;cs=0
            packed=e['no'] | (cs<<16) | (block<<40)
            table.extend(struct.pack('<QII',packed,len(data),0))
        payload.extend(out);payload.extend(b'\0'*(pad(len(payload),512)-len(payload)))
    header=struct.pack('<4I',MAGIC,len(entries),len(names),OPEN)+table+names
    return header+b'\0'*(headsz-len(header))+payload

def read(data):
    magic,count,nn,enc=struct.unpack_from('<4I',data)
    assert magic==MAGIC and enc in (0,OPEN),'not an unencrypted RPF7'
    assert len(data)%512==0
    names=data[16+count*16:16+count*16+nn];es=[]
    for i in range(count):
        b=data[16+i*16:32+i*16];q,a,c=struct.unpack('<QII',b)
        h1,h2=struct.unpack('<II',b[:8]);directory=h2==0x7fffff00
        no=h1 if directory else q&0xffff
        assert no<len(names)
        end=names.index(0,no);name=names[no:end].decode('ascii')
        if directory:e={'name':name,'start':a,'count':c,'dir':True}
        else:
            size=(q>>16)&0xffffff;block=(q>>40)&0x7fffff;res=bool(q>>63)
            n=size if res or size else a
            out=data[block*512:block*512+n];assert len(out)==n
            if res:assert out[:4]==b'RSC7' and struct.unpack_from('<II',out,8)==(a,c)
            elif size:out=zlib.decompress(out,-15);assert len(out)==a
            e={'name':name,'data':out,'dir':False}
        es.append(e)
    assert es[0]['dir'] and es[0]['name']==''
    result={};seen=set()
    def walk(i,path):
        assert i not in seen;seen.add(i);e=es[i]
        if not e['dir']:result[path]=e['data'];return
        ch=range(e['start'],e['start']+e['count'])
        assert e['start']+e['count']<=len(es)
        assert [es[x]['name'] for x in ch]==sorted(es[x]['name'] for x in ch)
        for j in ch:walk(j,(path+'/' if path else '')+es[j]['name'])
    walk(0,'');assert len(seen)==len(es)
    return result

if __name__=='__main__':
    import sys,pathlib
    root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);files={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
    data=build(files);assert read(data)==files;out.write_bytes(data)
    print('RPF7 wrote and round-trip verified',len(files),'entries;',len(data),'bytes')
