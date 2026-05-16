"""
إعدادات الإيجنت - OpenRouter API Configuration
"""

import os

# تحميل ملف .env إذا موجود
def _load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

_load_env()

# OpenRouter API Key
# ضع المفتاح في ملف .env أو متغير بيئة
# OPENROUTER_API_KEY=your-key-here
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# OpenRouter Base URL
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# جميع نماذج ChatGPT المتاحة (العادي و Plus)
MODELS = {
    # === نماذج GPT-4o (Plus) ===
    "1": {
        "id": "openai/gpt-4o",
        "name": "GPT-4o",
        "description": "أقوى نموذج - سريع وذكي (Plus)"
    },
    "2": {
        "id": "openai/gpt-4o-mini",
        "name": "GPT-4o Mini",
        "description": "نسخة مصغرة من GPT-4o - سريع واقتصادي"
    },
    "3": {
        "id": "openai/gpt-4-turbo",
        "name": "GPT-4 Turbo",
        "description": "GPT-4 المحسّن - قوي جداً (Plus)"
    },
    "4": {
        "id": "openai/gpt-4",
        "name": "GPT-4",
        "description": "النموذج الأساسي القوي (Plus)"
    },
    # === نماذج GPT-3.5 (العادي) ===
    "5": {
        "id": "openai/gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo",
        "description": "سريع واقتصادي - النموذج العادي"
    },
    "6": {
        "id": "openai/gpt-3.5-turbo-16k",
        "name": "GPT-3.5 Turbo 16K",
        "description": "نافذة سياق كبيرة - 16K tokens"
    },
    # === نماذج o1 (التفكير العميق) ===
    "7": {
        "id": "openai/o1-preview",
        "name": "o1 Preview",
        "description": "نموذج التفكير العميق - للمسائل المعقدة (Plus)"
    },
    "8": {
        "id": "openai/o1-mini",
        "name": "o1 Mini",
        "description": "نسخة مصغرة من o1 - تفكير سريع (Plus)"
    },
    # === نماذج ChatGPT الأحدث ===
    "9": {
        "id": "openai/chatgpt-4o-latest",
        "name": "ChatGPT-4o Latest",
        "description": "أحدث إصدار من ChatGPT-4o"
    },
    "10": {
        "id": "openai/gpt-4o-2024-11-20",
        "name": "GPT-4o (Nov 2024)",
        "description": "إصدار نوفمبر 2024 من GPT-4o"
    },
}

# إعدادات افتراضية
DEFAULT_MODEL = "openai/gpt-4o"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096

# System Prompt
SYSTEM_PROMPT = "أنت مساعد ذكي ومفيد. أجب بشكل واضح ومفصل. يمكنك الإجابة بالعربية أو الإنجليزية حسب لغة السؤال."
