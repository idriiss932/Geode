import sys,json,re
sys.path.insert(0,'/home/claude/geode/tools/i18n')
import en_a,en_b
D={**en_a.A,**en_b.B}
for k in ["Vaincre § cristal§ géant§","Attraper § comète§ dorée§","Ouvrir § coffre§","Posséder § relique§"]:D.pop(k,None)
D.update({
"Vaincre § cristal géant":"Defeat {0} giant crystal","Attraper § comète dorée":"Catch {0} golden comet","Ouvrir § coffre":"Open {0} chest","Réussir § défi du jour":"Complete {0} daily challenge",
"Posséder § relique":"Own {0} relic","Posséder § reliques":"Own {0} relics",
" ◆ et ":" ◆ and "," déjà actif (":" already active ("," s) : retouche pour prolonger":" s): tap again to extend"," gemmes ◆ pour ":" gems ◆ for "," activé ! ":" activated! ","verte":"green","jaune":"yellow","rouge":"red","violette":"purple","bleue":"blue"," %":"%"," et 1 ◆":" and 1 ◆","gemmes":"gems","gemme":"gem"," pour ascensionner (record actuel : ":" to ascend (current best: "," en recharge : ":" cooling down: ",
})
s=open('/home/claude/geode_src.html').read()
m=re.search(r'<script>([\s\S]*)</script>',s)
js=m.group(1);off=m.start(1)
lits=json.load(open('/tmp/lits.json'))
ins=[];used=set()
for x in lits:
    v=x['v']
    if v in D:
        used.add(v)
        if x['t']=='s':
            ins.append((x['s'],'_T('));ins.append((x['e'],')'))
        else:
            ins.append((x['s'],'_tt'))
ins.sort(key=lambda p:p[0],reverse=True)
ob=js.encode('utf-16-le')
for pos,txt in ins:ob=ob[:pos*2]+txt.encode('utf-16-le')+ob[pos*2:]
out=ob.decode('utf-16-le')
static=["Passer le tuto","Géode — le jeu qui creuse tout seul","Profondeur 1","Journal","Réglages","Langue","Touche pour frapper","Tape sur les cristaux : un coup de pouce en plus des comètes.","Son","Nova"]
EN={k:v for k,v in D.items() if k in used or k in static}
unused=[k for k in D if k not in used and k not in static]
print('wrapped',len(used),'unused',len(unused))
for k in unused:print('  unused:',repr(k)[:100])
out=out.replace('const EN=__EN__;','const EN='+json.dumps(EN,ensure_ascii=False,separators=(',',':'))+';',1)
s2=s[:off]+out+s[m.end(1):]
open('/home/claude/geode.html','w').write(s2)
open('/tmp/geo.js','w').write(out)
