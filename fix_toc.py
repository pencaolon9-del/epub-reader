# Fix TOC: remove resizeViewer from toggleSidebar + add safety limits
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 1: remove resizeViewer from toggleSidebar (safe, no special chars)
old1 = "$('sidebar').classList.toggle('hidden');setTimeout(resizeViewer,300);"
new1 = "$('sidebar').classList.toggle('hidden');"
c = c.replace(old1, new1)

# Fix 2: add safety to buildToc
# Replace the _flatten call with try/catch wrapped version
old2 = "_flatten(toc).forEach(function(it,i){const li=document.createElement('li'),a=document.createElement('a');"
new2 = "(_flatten(toc)||[]).slice(0,500).forEach(function(it,i){var li=document.createElement('li'),a=document.createElement('a');"
c = c.replace(old2, new2)

# Fix 3: add rendition existence check in TOC click
old3 = "rendition.display(it.href);if(innerWidth<700)toggleSidebar();"
new3 = "if(rendition)rendition.display(it.href);if(innerWidth<700)toggleSidebar();"
c = c.replace(old3, new3)

# Fix 4: wrap buildToc body in try/catch
old4 = "function buildToc(toc){if(_tocBuilt)return;_tocBuilt=true;const l=$('toc-list');l.innerHTML='';if(!toc||!toc.length){l.innerHTML='<li style=\"padding:16px;opacity:0.5;font-size:0.85rem;\">无目录</li>';return;}"
new4 = "function buildToc(toc){if(_tocBuilt)return;_tocBuilt=true;const l=$('toc-list');try{l.innerHTML='';if(!toc||!toc.length){l.innerHTML='<li style=\"padding:16px;opacity:0.5;font-size:0.85rem;\">无目录</li>';return;}"
c = c.replace(old4, new4)

# Fix 5: close try/catch at end of buildToc
old5 = "li.appendChild(a);l.appendChild(li);});}"
new5 = "li.appendChild(a);l.appendChild(li);});}catch(e){l.innerHTML='<li style=\"padding:16px;opacity:0.5;font-size:0.85rem;\">目录加载失败</li>';}}"
c = c.replace(old5, new5)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done')
