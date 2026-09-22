# 📖 دليل التشغيل المفصل — Mt Ai

## المتطلبات
- Python 3.10 أو أحدث
- مفتاح Gemini API مجاني من [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## 1️⃣ تثبيت Python (لو مش متثبت)

حمّل من [python.org/downloads](https://www.python.org/downloads) وعلّم صح ✔️ على **"Add Python to PATH"** أول التثبيت.

## 2️⃣ تثبيت المكتبات

افتح CMD/Terminal في فولدر `backend` ونفّذ:

```bash
pip install -r requirements.txt
```

## 3️⃣ إعداد المفتاح

انسخ `.env.example` وسميه `.env`، وبعدين حط مفتاحك:

```bash
cp .env.example .env
```

أو أنشئ الملف بأمر (Windows CMD):
```cmd
echo GEMINI_API_KEY=مفتاحك_هنا > .env
```

## 4️⃣ تشغيل السيرفر

```bash
python -m uvicorn server:app --reload --port 8000
```

لو الأمر `python` مش شغال جرب `py -m uvicorn ...` بدلًا منه.

## 5️⃣ فتح الموقع

افتح ملف `public/index.html` بأي متصفح — والموقع هيتكلم مع السيرفر تلقائياً.

> ⚠️ خلي الشاشة السودا (السيرفر) مفتوحة طول ما بتستخدم الموقع.

## 6️⃣ التأكد من إن كل حاجة شغالة

افتح في المتصفح: `http://127.0.0.1:8000/api/health`

المفروض يظهر:
```json
{"status":"ok","key_loaded":true,"key_valid_format":...,"client_ready":true}
```

## 7️⃣ واجهة الـ API التفاعلية (Swagger)

افتح: `http://127.0.0.1:8000/docs` — ومنها تقدر تجرب كل الـ endpoints مباشرة.

---

## ❓ حل المشاكل الشائعة

| المشكلة | الحل |
|---|---|
| `pip is not recognized` | Python مش في الـ PATH — أعد تثبيت Python وعلّم "Add to PATH"، أو استخدم `py -m pip ...` |
| السيرفر شغال بس الموقع بيقول "Backend مش شغال" | تأكد إن الرابط `http://127.0.0.1:8000` شغال في المتصفح (افتح `/api/health`) |
| صور بتطلع مش مطابقة | اكتب وصف مفصّل — الموقع بيترجمه تلقائياً، لكن الإنجليزي المباشر أدق |
| `429 RESOURCE_EXHAUSTED` للصور | طبيعي — الباقة المجانية مش شاملة موديل صور Gemini، المشروع بيستخدم بديل مجاني تلقائياً |

## 🔒 الأمان

- ❌ **ممنوع** رفع ملف `.env` على GitHub (موجود في `.gitignore`)
- ❌ ما تعرضش المفتاح في صور أو شاشات عامة
- ✅ لو اتسرب المفتاح: امسحه من صفحة API Keys واعمل واحد جديد
