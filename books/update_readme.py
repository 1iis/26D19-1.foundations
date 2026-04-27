from pathlib import Path
import subprocess
rm = Path('README.md')
old = {}
if rm.exists():
    for l in rm.read_text().splitlines():
        if not l.startswith('|') or '---' in l or 'Title' in l: continue
        c = [x.strip() for x in l.split('|')[1:-1]]
        try: old[c[0]] = [int(x.replace(',','')) for x in c[1:4]]
        except: pass
def tok(p): return int(subprocess.check_output(['python','token_counter_qwen.py',str(p)], text=True).strip())
rows = []
for p in sorted(Path('.').glob('*.txt')):
    t = p.read_text(); o = old.get(p.name)
    rows.append((p.name,*o) if o and o[0]==len(t) else (p.name,len(t),len(t.split()),tok(p)))
tbl = '\n'.join(f"| {n} | {c:,} | {w:,} | {t:,} |" for n,c,w,t in rows)
hdr = '| Title | Chars | Words | Tokens<br>(Qwen3)\n| --- | --- | --- | ---'
if not rm.exists(): rm.write_text(f'# Books\n\n{hdr}\n{tbl}\n')
else:
    ls = rm.read_text().splitlines()
    i = next((i for i,l in enumerate(ls) if l.startswith('| Title')), None)
    if i is None: rm.write_text('\n'.join(ls).rstrip() + f'\n\n{hdr}\n{tbl}\n')
    else:
        j = next((j for j in range(i+2,len(ls)) if not ls[j].startswith('|')), len(ls))
        pre,post = '\n'.join(ls[:i]), '\n'.join(ls[j:]) if j < len(ls) else ''
        rm.write_text((pre+'\n' if pre else '') + hdr + '\n' + tbl + '\n' + (post+'\n' if post else ''))
