const {chromium}=require('playwright');
const {execFileSync}=require('child_process');const fs=require('fs');
(async()=>{
  const S=require('path').resolve(process.argv[2]||'.'),FPS=30;
  const b=await chromium.launch({proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined,args:['--ignore-certificate-errors']});
  const p=await b.newPage({viewport:{width:1080,height:1350}});
  p.on('pageerror',e=>console.log('ERR',e.message));
  await p.goto('file://'+S+'/build/local.html#render');
  await p.evaluate(async()=>{for(const f of ['italic 500 20px Archivo','italic 700 20px Archivo','italic 800 20px Archivo','italic 900 20px Archivo','500 20px Archivo','800 20px Archivo','500 20px "IBM Plex Mono"'])await document.fonts.load(f);await document.fonts.ready});
  const durs=await p.evaluate(()=>__durs);fs.mkdirSync(S+'/video',{recursive:true});
  for(let i=0;i<durs.length;i++){
    const dir=S+'/build/frames/'+i;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir,{recursive:true});
    const n=Math.round(durs[i]*FPS);
    for(let f=0;f<n;f++){await p.evaluate(([i,t])=>__seek(i,t),[i,f/FPS]);await p.screenshot({path:`${dir}/${String(f).padStart(4,'0')}.png`})}
    const out=`${S}/video/crivel-${String(i+1).padStart(2,'0')}.mp4`;
    execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(FPS),'-i',`${dir}/%04d.png`,'-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',out]);
    fs.rmSync(dir,{recursive:true,force:true});console.log('done',out,n);
  }
  await b.close();
})();
