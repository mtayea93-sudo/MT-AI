"""
Mt Ai - Backend (FastAPI)
بيربط موقعك بـ Google Gemini API (سكريبتات + صور)
التشغيل: py -m uvicorn server:app --reload --port 8000
"""
import os, base64
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---- تحميل المفتاح: من متغير البيئة الأول، وبعدين من ملف .env ----
def load_key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if k:
        return k
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip().lstrip("\ufeff")  # شيل BOM لو موجود
            if line and not line.startswith("#") and "=" in line:
                name, val = line.split("=", 1)
                if name.strip() == "GEMINI_API_KEY":
                    return val.strip().strip('"').strip("'")
    return ""

GEMINI_KEY = load_key()
client = None
if GEMINI_KEY:
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_KEY)
    except Exception:
        client = None

app = FastAPI(title="Mt Ai API")

# السماح لأي origin محلي بالنداء علينا (للتطوير فقط)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def ensure_client():
    if not GEMINI_KEY:
        raise HTTPException(500, "المفتاح مش متظبط: عدّل ملف .env واكتب فيه GEMINI_API_KEY=مفتاحك")
    if client is None:
        raise HTTPException(500, "مكتبة google-genai مش متثبتة: نفّذ py -m pip install -r requirements.txt")


# ---------- Models ----------
class ScriptRequest(BaseModel):
    topic: str
    lang: str = "العربية"
    type: str = "فيديو يوتيوب"
    tone: str = "احترافي"
    duration: str = "دقيقة"


class ImageRequest(BaseModel):
    prompt: str
    style: str = "واقعي فائق"
    ratio: str = "1024x1024"
    count: int = 1


# ---------- Endpoints ----------
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "key_loaded": bool(GEMINI_KEY),
        "key_valid_format": GEMINI_KEY.startswith("AIza"),
        "client_ready": client is not None,
    }


@app.post("/api/script")
def generate_script(req: ScriptRequest):
    """توليد سكريبت حقيقي بـ Gemini"""
    ensure_client()
    prompt = f"""أنت كاتب سكريبتات محتوى محترف.
اكتب سكريبت كامل باللغة: {req.lang}
نوع المحتوى: {req.type}
الأسلوب: {req.tone}
المدة التقريبية: {req.duration}
الموضوع: {req.topic}

الصيغة المطلوبة:
🎬 عنوان مقترح
── المشهد الافتتاحي (Hook) ──
── المحتوى الرئيسي ── (نقاط واضحة مرقمة)
── الخاتمة (Call to Action) ──

اكتب السكريبت جاهز للتصوير مباشرة، بدون مقدمات أو شرح."""
    try:
        r = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
        return {"text": r.text or "لم يتم إرجاع نص"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/image")
def generate_image(req: ImageRequest):
    """توليد صور حقيقية بـ Nano Banana (gemini image)"""
    ensure_client()
    size_map = {
        "1024x1024": ("1K", "square"),
        "1920x1080": ("2K", "landscape 16:9"),
        "1080x1920": ("2K", "portrait 9:16"),
        "2048x2048": ("2K", "square"),
        "4096x4096": ("4K", "square"),
    }
    size, aspect = size_map.get(req.ratio, ("1K", "square"))
    style_en = {
        "واقعي فائق": "ultra realistic photography, 8k, highly detailed",
        "سينمائي": "cinematic lighting, film still, dramatic atmosphere",
        "أنمي": "anime style, studio ghibli inspired, vibrant",
        "زيتي كلاسيكي": "classical oil painting, canvas texture, renaissance style",
        "ثلاثي الأبعاد": "3d render, octane render, soft studio lighting",
        "بيكسل آرت": "pixel art, retro 16-bit game style",
    }
    style_prompt = style_en.get(req.style.split(" ")[0], style_en["واقعي فائق"])

    w, h = req.ratio.split("x")[0], req.ratio.split("x")[1]

    # ترجمة الوصف العربي لإنجليزي مفصّل (مجاناً عبر Gemini) — مولدات الصور أدق مع الإنجليزية
    full_prompt = f"{req.prompt}, {style_prompt}, {aspect} aspect ratio"
    try:
        tr = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=(
                "Rewrite this image description as ONE detailed English image-generation prompt "
                "(rich visual details: subject, environment, lighting, mood, camera style). "
                "Output ONLY the prompt text, nothing else.\n"
                f"Description: {req.prompt}\nStyle: {style_prompt}"
            ),
        )
        if tr.text and len(tr.text.strip()) > 10:
            full_prompt = tr.text.strip()
    except Exception:
        pass  # لو الترجمة فشلت، نكمل بالوصف الأصلي
    try:
        images = []
        for _ in range(min(req.count, 4)):
            # الطريقة الجديدة: generate_content مع موديل الصور + طلب صراحةً رد صوري
            r = client.models.generate_content(
                model="gemini-3.1-flash-lite-image",
                contents=[full_prompt],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
            )
            cand = r.candidates[0]
            for part in cand.content.parts:
                inline = getattr(part, "inline_data", None)
                if inline and getattr(inline, "data", None):
                    images.append(base64.b64encode(inline.data).decode())
        if not images:
            raise Exception("الموديل ما رجّعش صورة")
        return {"images": images, "width": w, "height": h}
    except Exception as e:
        # لو الباقة المجانية مش شاملة موديل الصور (429 limit: 0) → بديل مجاني Pollinations
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower():
            try:
                import urllib.request, urllib.parse
                images = []
                for _ in range(min(req.count, 4)):
                    p = urllib.parse.quote(full_prompt)
                    u = f"https://image.pollinations.ai/prompt/{p}?width={w}&height={h}&nologo=true&seed={os.urandom(3).hex()}"
                    with urllib.request.urlopen(u, timeout=180) as resp:
                        images.append(base64.b64encode(resp.read()).decode())
                return {"images": images, "width": w, "height": h, "engine": "pollinations (مجاني)"}
            except Exception as e2:
                raise HTTPException(500, detail=f"جوجل رفضت (الباقة المجانية مش شاملة صور) والبديل المجاني فشل: {e2}")
        raise HTTPException(status_code=500, detail=msg)
