<div align="center">

# 🎬 Mt Ai

**منصة عربية لتوليد السكريبتات والصور (وفيديوهات قريباً) بالذكاء الاصطناعي**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini_API-4285F4?logo=google)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ المميزات

| الأداة | المحرك | الحالة |
|---|---|---|
| ✍️ توليد سكريبتات (40+ لغة) | Google Gemini Flash Lite | ✅ شغال — مجاني |
| 🖼️ توليد صور (جودة عالية) | Pollinations AI (مع ترجمة تلقائية للوصف عبر Gemini) | ✅ شغال — مجاني |
| 🖼️ صور Nano Banana (جودة أعلى) | Google Gemini Image | ⏳ جاهز — يحتاج تفعيل فوترة |
| 🎥 توليد فيديوهات | Veo / Kling | 🔜 قريباً |

## 🗂️ هيكل المشروع

```
mtai/
├── backend/
│   ├── server.py          # الـ API (FastAPI)
│   ├── requirements.txt   # المكتبات المطلوبة
│   └── .env.example       # مثال لملف المفاتيح (انسخه لـ .env)
├── public/
│   └── index.html         # واجهة الموقع (متصلة بالـ API)
├── docs/
│   └── SETUP.md           # دليل التشغيل المفصل
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 التشغيل السريع (محلياً)

```bash
# 1) ثبّت المكتبات
cd backend
pip install -r requirements.txt

# 2) جهّز المفتاح
cp .env.example .env
# افتح .env وحط مفتاح Gemini API Key بتاعك

# 3) شغّل السيرفر
python -m uvicorn server:app --reload --port 8000
```

**4)** افتح `public/index.html` في المتصفح وابدأ التوليد! 🎉

> 🔑 احصل على مفتاح مجاني من: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## 📡 الـ API Endpoints

| Method | Endpoint | الوصف |
|---|---|---|
| `GET` | `/api/health` | فحص حالة السيرفر والمفتاح |
| `POST` | `/api/script` | توليد سكريبت `{topic, lang, type, tone, duration}` |
| `POST` | `/api/image` | توليد صور `{prompt, style, ratio, count}` |

وثائق تفاعلية (Swagger) متاحة على: `http://127.0.0.1:8000/docs`

## 🧠 كيف يعمل توليد الصور؟

```
وصف عربي من المستخدم
        │
        ▼
Gemini Flash Lite (مجاني) ──► يترجم ويفصّل الوصف لإنجليزي احترافي
        │
        ▼
Pollinations AI (مجاني) ────► يولّد الصورة بالوصف المفصّل
        │
        ▼
صورة مطابقة للوصف بنسبة عالية ✅
```

## ⚠️ ملاحظات مهمة

- **موديل الصور من Gemini (Nano Banana)** غير متاح في الباقة المجانية (quota = 0)، لذلك يستخدم المشروع Pollinations كبديل مجاني تلقائياً. عند تفعيل الفوترة في Google Cloud سيستخدم Nano Banana تلقائياً.
- **لا ترفع ملف `.env` على GitHub أبداً** — المفتاح سرّي. (موجود في `.gitignore`)
- السكريبتات بتكلفة شبه معدومة: ألف سكريبت ≈ $0.01

## 🗺️ خارطة الطريق (Roadmap)

- [x] توليد سكريبتات متعددة اللغات
- [x] توليد صور مجاني مع ترجمة تلقائية
- [x] واجهة عربية RTL كاملة
- [ ] توليد فيديوهات (Veo / Kling)
- [ ] نظام مستخدمين وحفظ النتائج
- [ ] نشر سحابي (Render / Railway)
- [ ] تعديل الصور (Inpainting)
- [ ] نظام اشتراكات مدفوعة

## 📄 الرخصة

هذا المشروع مرخّص تحت رخصة [MIT](LICENSE) — استخدمه وعدّله بحرية.

---

<div align="center">
صُنع بـ ❤️ — Mt Ai © 2026
</div>
