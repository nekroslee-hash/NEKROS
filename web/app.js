const statusEl=document.getElementById("status");
const healthEl=document.getElementById("health");
const sendButton=document.getElementById("send");
async function checkHealth(){
  try{const response=await fetch("/api/health");if(!response.ok)throw Error();const data=await response.json();statusEl.textContent="آنلاین";healthEl.textContent=data.name+" آماده پاسخ‌گویی پایه است.";}
  catch{statusEl.textContent="آفلاین";healthEl.textContent="اتصال به سرور برقرار نشد.";}
}
sendButton.addEventListener("click",async()=>{
  const prompt=document.getElementById("prompt").value.trim();
  const token=document.getElementById("token").value.trim();
  const output=document.getElementById("reply");
  if(!prompt||!token){output.textContent="پیام و توکن API را وارد کنید.";return;}
  sendButton.disabled=true;output.textContent="در حال پردازش...";
  try{
    const response=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},body:JSON.stringify({content:prompt})});
    const data=await response.json();if(!response.ok)throw Error(data.detail||"خطا");
    output.textContent=data.reply;
  }catch(error){output.textContent="خطا: "+error.message;}
  finally{sendButton.disabled=false;}
});
checkHealth();
