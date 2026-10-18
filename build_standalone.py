from pathlib import Path
import re
r=Path(__file__).parent
css=(r/'styles.css').read_text()
engine=re.sub(r'\bexport\s+(?=(?:const|function|class)\b)','',(r/'engine.mjs').read_text())
app=(r/'app.js').read_text()
assert app.startswith('import ')
app=app.split('\n',1)[1]
assert 'export ' not in engine
h=(r/'index.html').read_text()
h=re.sub(r'<link rel="preconnect"[^>]+>','',h)
h=re.sub(r'<link href="https://fonts.googleapis.com[^>]+>','',h)
h=h.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
h=h.replace('<script type="module" src="./app.js"></script>','<script>'+engine+'\n'+app+'</script>')
(r/'snap-automations-standalone.html').write_text(h)
print('Standalone bytes',len(h))
