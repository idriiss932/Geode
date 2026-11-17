const acorn=require('/opt/npm-tools/node_modules/acorn');
const fs=require('fs');
const html=fs.readFileSync('/home/claude/geode_src.html','utf8');
const js=html.match(/<script>([\s\S]*)<\/script>/)[1];
const ast=acorn.parse(js,{ecmaVersion:2022,locations:false});
const out=[];
function walk(n,parent,key){
  if(!n||typeof n.type!=='string'){return;}
  if(n.type==='Literal'&&typeof n.value==='string'){
    if(!(parent&&parent.type==='Property'&&key==='key'&&!parent.computed)&&!(parent&&parent.type==='ExpressionStatement'&&parent.directive))out.push({t:'s',v:n.value,s:n.start,e:n.end});
  }
  if(n.type==='TemplateLiteral'){
    const tagged=parent&&parent.type==='TaggedTemplateExpression'&&key==='quasi';
    if(!tagged)out.push({t:'t',v:n.quasis.map(q=>q.value.cooked).join('§'),s:n.start,e:n.end,q:n.quasis.map(q=>[q.start,q.end]),ex:n.expressions.map(x=>[x.start,x.end])});
  }
  for(const k in n){if(k==='type'||k==='start'||k==='end')continue;const c=n[k];if(Array.isArray(c))c.forEach(x=>walk(x,n,k));else if(c&&typeof c.type==='string')walk(c,n,k);}
}
walk(ast,null,null);
fs.writeFileSync('/tmp/lits.json',JSON.stringify(out));
console.log(out.length);
