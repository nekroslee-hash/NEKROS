const statusEl=document.getElementById("status");
const healthEl=document.getElementById("health");
const sendButton=document.getElementById("send");

async function checkHealth(){
  try{
    const response=await fetch("/api/health");
    if(!response.ok)throw Error();
    const data=await response.json();
    statusEl.textContent="آنلاین";
    healthEl.textContent=data.name+" آماده است؛ مسیریابی خودکار و بودجه رایگان فعال است.";
  }catch{
    statusEl.textContent="آفلاین";
    healthEl.textContent="اتصال به سرور برقرار نشد.";
  }
}

async function checkCapabilities(){
  const token=document.getElementById("token").value.trim();
  if(!token)return;
  const headers={Authorization:"Bearer "+token};
  try{
    const [aiResponse,mediaResponse]=await Promise.all([
      fetch("/api/ai/status",{headers}),
      fetch("/api/media/capabilities",{headers})
    ]);
    if(aiResponse.ok){
      const ai=await aiResponse.json();
      document.getElementById("ai-status").textContent=ai.message+" مدل‌های مجاز: "+ai.available_models.length;
    }
    if(mediaResponse.ok){
      const media=await mediaResponse.json();
      document.getElementById("media-status").textContent=media.note;
    }
  }catch{
    document.getElementById("ai-status").textContent="برای مشاهده وضعیت، توکن معتبر وارد کنید.";
  }
}

document.getElementById("token").addEventListener("change",checkCapabilities);
sendButton.addEventListener("click",async()=>{
  const prompt=document.getElementById("prompt").value.trim();
  const token=document.getElementById("token").value.trim();
  const output=document.getElementById("reply");
  if(!prompt||!token){output.textContent="پیام و توکن API سرور را وارد کنید.";return;}
  sendButton.disabled=true;output.textContent="در حال پردازش...";
  try{
    const response=await fetch("/api/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},
      body:JSON.stringify({content:prompt})
    });
    const data=await response.json();
    if(!response.ok)throw Error(data.detail||"خطا");
    output.textContent=data.reply;
  }catch(error){output.textContent="خطا: "+error.message;}
  finally{sendButton.disabled=false;}
});
checkHealth();
