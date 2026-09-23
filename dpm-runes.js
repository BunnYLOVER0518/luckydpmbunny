(() => {
  'use strict';
  const data=window.RUNE_DATA, $=id=>document.getElementById(id);
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmt=n=>Number(n).toLocaleString('ko-KR',{maximumFractionDigits:3});
  let selected=0;
  window.renderRunes=caseId=>{
    selected=caseId;
    const base=window.DPM_DATA.summary[caseId], grade=$('rune-grade').value;
    $('rune-context').textContent=`${base.hero} · Lv.${base.level} · ${base.rune.replace(/^없음·?/,'')||'기본'} · 무룬 ${fmt(base.dpmB)} B DPM`;
    let rows=data.cases[caseId].filter(r=>(grade==='all'||data.catalog[r[0]].grade===grade)&&($('rune-theory').checked||r[3]));
    const sort=$('rune-sort').value;
    rows.sort((a,b)=>sort==='name'?data.catalog[a[0]].name.localeCompare(data.catalog[b[0]].name,'ko'):(sort==='asc'?a[1]-b[1]:b[1]-a[1]));
    $('rune-count').textContent=`${rows.length}개 결과`;
    $('rune-rows').innerHTML=rows.map((r,i)=>{
      const c=data.catalog[r[0]],gain=r[1]-100;
      return `<tr><td>${i+1}</td><td><strong>${esc(c.name)}</strong><small class="rune-effect">${esc(c.description)}</small></td><td>${esc(c.grade)}</td><td class="number">${fmt(r[1])}</td><td class="number ${gain<0?'rune-negative':'rune-positive'}">${gain>=0?'+':''}${fmt(gain)}%</td><td class="number">${fmt(r[2])}</td><td><small>${esc(data.conditions[r[4]])}${r[3]?'':' · 실전 순위 제외'}</small></td></tr>`;
    }).join('');
  };
  for(const id of ['rune-grade','rune-sort','rune-theory'])$(id).addEventListener('change',()=>window.renderRunes(selected));
})();
