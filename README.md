# 🤖 ChatGPT Agent - OpenRouter

إيجنت تفاعلي للدردشة مع جميع نماذج ChatGPT (Plus والعادي) عبر OpenRouter API.

## النماذج المدعومة

| # | النموذج | الوصف |
|---|---------|-------|
| 1 | GPT-4o | أقوى نموذج - سريع وذكي (Plus) |
| 2 | GPT-4o Mini | نسخة مصغرة اقتصادية |
| 3 | GPT-4 Turbo | GPT-4 المحسّن (Plus) |
| 4 | GPT-4 | النموذج الأساسي القوي (Plus) |
| 5 | GPT-3.5 Turbo | سريع واقتصادي (العادي) |
| 6 | GPT-3.5 Turbo 16K | نافذة سياق كبيرة |
| 7 | o1 Preview | التفكير العميق (Plus) |
| 8 | o1 Mini | تفكير سريع (Plus) |
| 9 | ChatGPT-4o Latest | أحدث إصدار |
| 10 | GPT-4o (Nov 2024) | إصدار نوفمبر 2024 |

## التشغيل

1. ضع مفتاح API في ملف `.env`:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

2. شغّل الإيجنت:
```bash
python3 main.py
```

## الأوامر

| الأمر | الوصف |
|-------|-------|
| `/models` | عرض النماذج المتاحة |
| `/switch` | تغيير النموذج |
| `/clear` | مسح سجل المحادثة |
| `/temp 0.9` | تغيير درجة الإبداع |
| `/info` | معلومات الجلسة |
| `/help` | عرض الأوامر |
| `/quit` | الخروج |

## المتطلبات

- Python 3.7+
- لا يحتاج مكتبات خارجية (يستخدم `urllib` المدمجة)

## الحصول على مفتاح API

1. سجل في [OpenRouter](https://openrouter.ai)
2. اذهب إلى [Keys](https://openrouter.ai/keys)
3. أنشئ مفتاح جديد
