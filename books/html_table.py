from pathlib import Path
ls=[l for l in Path('README.md').read_text().splitlines() if l.startswith('|')]
hdr=[c.strip().replace('<br>',' ') for c in ls[0].strip('| \t').split('|')]
r=[[c.strip() for c in l.strip('| \t').split('|')] for l in ls[2:]]
h=''.join(f'<th onclick="s(this)">{c}</th>' for c in hdr)
b='\n'.join(f'<tr><td>{x[0]}</td><td class="n">{x[1]}</td><td class="n">{x[2]}</td><td class="n">{x[3]}</td></tr>' for x in r if len(x)>=4)
Path('books.html').write_text(f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{font-family:sans-serif;margin:2em}}table{{border-collapse:collapse;width:100%}}th,td{{padding:8px;text-align:left;border-bottom:1px solid #ddd}}th{{cursor:pointer;background:#f2f2f2}}tr:hover{{background:#f5f5f5}}.n{{text-align:right}}</style></head><body><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table><script>let d=1,t=0;function s(th){{const i=Array.from(th.parentNode.children).indexOf(th),tb=th.closest("table").querySelector("tbody"),tr=Array.from(tb.querySelectorAll("tr"));d=i===t?-d:1;t=i;tr.sort((a,b)=>{{const m=a.children[i].textContent.replace(/,/g,""),n=b.children[i].textContent.replace(/,/g,"");return(isNaN(m)||isNaN(n)?m.localeCompare(n):m-n)*d}});tr.forEach(r=>tb.appendChild(r))}}</script></body></html>''')

