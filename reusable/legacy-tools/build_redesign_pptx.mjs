import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const ROOT = process.cwd();
const P = path.join(ROOT,'paper','information-set-redesign-20261117');
const B = path.join(P,'build-pptx');
const O = path.join(ROOT,'output','information-set-redesign-20261117');
const SKILL = 'C:/Users/Purple_Born/.codex/plugins/cache/openai-primary-runtime/presentations/26.1112.11011/skills/presentations';
const PYTHON = 'C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1112-611-0_26.1112.611.0_x64__3k8sg7r9htsxt/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1112-611-0_26.1112.611.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules';
const data = JSON.parse(await fs.readFile(path.join(P,'pptx_content.json'),'utf8'));
await fs.mkdir(B,{recursive:true});await fs.mkdir(O,{recursive:true});
const ppt = Presentation.create({slideSize:{width:960,height:720}});
const WINE='#971f30', DARK='#4c1018';
const sections=[...new Set(data.map(s=>s.section))];
function box(slide,txt,x,y,w,h,size=28,color='#111111',bold=false,align='left',face='KaiTi') {
  const obj=slide.shapes.add({geometry:'textbox',name:txt.slice(0,35),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  obj.text=txt;obj.text.style={typeface:face,fontSize:size,color,bold,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:0};
  return obj;
}
function rect(slide,x,y,w,h,fill){return slide.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});}
function lines(slide,texts,x,y,w,size=27,gap=22){
  let pos=y;
  for(const t of texts){const weighted=[...t].reduce((a,c)=>a+(/[\u0000-\u00ff]/.test(c)?0.52:1),0);const nr=Math.max(1,Math.ceil(weighted*size/w));const h=nr*(size*1.30)+10;box(slide,t,x,pos,w,h,size);pos+=h+gap;}
  if(pos-gap>627)console.log(`CONTENT BOTTOM ${pos-gap}: ${texts.join(' / ')}`);
  return pos;
}
for(const s of data){
  const slide=ppt.slides.add();slide.background.fill='#ffffff';
  slide.speakerNotes.text=s.speech+'\n\n核对出处：'+s.source+(s.speaker_note?'\n备讲说明：'+s.speaker_note:'');
  if(s.kind==='cover'){
    rect(slide,52,198,856,148,WINE);
    box(slide,s.title,76,204,808,134,39,'#ffffff',false,'center','Arial');
    box(slide,'Toomas Laarits   Jeffrey Wurgler',60,391,840,45,29,'#111111',false,'center','Arial');
    box(slide,'NYU Stern School of Business',60,449,840,40,26,'#111111',false,'center','Arial');
    box(slide,'2026年4月27日工作稿',60,513,840,40,28,'#111111',false,'center');
    continue;
  }
  rect(slide,0,0,960,32,DARK);
  for(let i=0;i<sections.length;i++)box(slide,sections[i],i*192+4,0,184,31,16,s.section===sections[i]?'#ffffff':'#d8bdc1',false,'center');
  rect(slide,0,32,960,84,WINE);
  box(slide,s.title,52,39,856,70,34,'#ffffff');
  rect(slide,0,675,960,22,WINE);rect(slide,0,697,960,23,DARK);
  box(slide,'Laarits & Wurgler',28,676,600,20,14,'#ffffff',false,'left','Arial');
  box(slide,'NYU Stern',720,676,212,20,14,'#ffffff',false,'right','Arial');
  box(slide,'个体投资者的信息集',28,698,700,20,14,'#ffffff');
  box(slide,`${s.page} / 45`,820,698,112,20,14,'#ffffff',false,'right','Arial');
  if(s.source)box(slide,s.source,52,629,856,38,15,'#646464');
  let y=156;
  if(s.formula){
    box(slide,s.formula.plain,54,161,852,s.page===15?118:94,29,WINE,false,'center',s.page===5?'Cambria Math':'KaiTi');
    y=s.page===15?308:285;
  }
  if(s.table){
    const n=s.table.length;
    const fontSize=s.page===35?23:24;
    const cws=s.column_widths.map(w=>w*856);
    const rowHeights=s.table.map(row=>Math.max(45,...row.map((t,c)=>{
      const units=[...String(t)].reduce((a,k)=>a+(/[\u0000-\u00ff]/.test(k)?0.57:1),0);
      return Math.ceil(units*fontSize/(cws[c]-24))*(fontSize*1.28)+16;
    })));
    const h=rowHeights.reduce((a,b)=>a+b,0);
    if(y+h>620)console.log(`TABLE BOTTOM ${s.page}: ${y+h}`);
    const table=slide.tables.add({rows:n,columns:s.table[0].length,left:52,top:y,width:856,height:h,columnWidths:cws,values:s.table});
    for(let r=0;r<n;r++)table.rows[r].height=rowHeights[r];
    table.borders.assign({style:'solid',fill:'#c1b3b5',width:0.7});
    for(let r=0;r<n;r++)for(let c=0;c<s.table[r].length;c++){
      const cell=table.getCell(r,c);cell.fill='#ffffff';
      cell.text.style={typeface:'KaiTi',fontSize,color:r===0?WINE:'#111111',bold:r===0,verticalAlignment:'middle',alignment:'left',wrap:'square',insets:{left:10,right:8,top:6,bottom:6}};
    }
    y+=h+19;
  }
  if(s.asset){
    const img=path.join(P,'assets',s.asset+'.png');
    const imgBytes=await fs.readFile(img);
    if(s.asset.startsWith('timing_')){
      slide.images.add({blob:imgBytes,contentType:'image/png',alt:s.title,fit:'contain',position:{left:65,top:147,width:430,height:466}});
      lines(slide,s.lines,535,262,360,27,30);
    }else{
      const pos=s.asset==='event_msft'?{left:190,top:147,width:580,height:397}:{left:62,top:142,width:836,height:s.asset==='web_compare'?395:399};
      slide.images.add({blob:imgBytes,contentType:'image/png',alt:s.title,fit:'contain',position:pos});
      lines(slide,s.lines,52,548,856,22,1);
    }
  }else if(s.kind==='chain'){
    let yy=147;
    for(let i=0;i<s.lines.length;i++){
      box(slide,s.lines[i],62,yy,836,49,27,i===1?WINE:'#111111',i===1);
      if(i<4)box(slide,'↓',62,yy+48,40,34,28,WINE);
      yy+=91;
    }
  }else if(s.lines.length){lines(slide,s.lines,52,y,856,s.table?24:27,s.table?9:21);}
}
const candidate=path.join(B,'candidate.pptx');
await (await PresentationFile.exportPptx(ppt)).save(candidate);
await fs.writeFile(path.join(B,'presentation.json'),JSON.stringify(ppt.toProto()));
if(process.argv.includes('--draft-only')){console.log(candidate);process.exit(0);}
const previewDir=path.join(B,'render');await fs.mkdir(previewDir,{recursive:true});
for(const [i,slide] of ppt.slides.items.entries()){
  const png=await ppt.export({slide,format:'png',scale:1.5});
  await fs.writeFile(path.join(previewDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
  if((i+1)%10===0)console.log(`rendered ${i+1}`);
}
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools','artifact_tool_utils.mjs')).href);
const finalPath=path.join(O,'01_45页报告.pptx');
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,pythonExecutable:PYTHON,
  integrityValidatorPath:path.join(SKILL,'container_tools','inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL,'container_tools','inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','9144000,6858000','--validate-heading-fit',...data.filter(s=>s.table).flatMap(s=>['--require-native-table-slide',String(s.page)])],
  explicitTotalSlideCount:45,requiredNativeTableOwnerSlides:data.filter(s=>s.table).map(s=>s.page),requiredNativeChartOwnerSlides:[],
  verifyArtifactToolImport:true,receiptPath:path.join(B,'validation-final.json')});
console.log(JSON.stringify(result));
