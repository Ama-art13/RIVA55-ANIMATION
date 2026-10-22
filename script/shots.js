const {chromium}=require('playwright');
(async()=>{
  const S=require('path').resolve(process.argv[2]||'.');const times=JSON.parse(process.argv[3]);require('fs').mkdirSync(S+'/build/shots',{recursive:true});
  const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
  const b=await chromium.launch({proxy,args:['--ignore-certificate-errors']});
  const p=await b.newPage({viewport:{width:1080,height:1350}});
  p.on('console',m=>console.log('console:',m.text()));p.on('pageerror',e=>console.log('ERR',e.message));
  await p.goto('file://'+S+'/build/local.html#render');await p.evaluate(async()=>{for(const f of ['italic 500 20px Archivo','italic 700 20px Archivo','italic 800 20px Archivo','italic 900 20px Archivo','500 20px Archivo','800 20px Archivo','500 20px "IBM Plex Mono"'])await document.fonts.load(f);await document.fonts.ready});
  console.log(await p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+f.style+f.weight).join(',')));
  for(const [i,t] of times){await p.evaluate(([i,t])=>__seek(i,t),[i,t]);await p.waitForTimeout(60);await p.screenshot({path:`${S}/build/shots/s${i+1}_${t}.png`})}
  await b.close();
})();
