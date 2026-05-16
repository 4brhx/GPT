"""
ChatGPT Agent - OpenRouter API
إيجنت شات جي بي تي باستخدام OpenRouter
(يستخدم urllib المدمجة - لا يحتاج مكتبات خارجية)
"""

import urllib.request
import urllib.error
import json
import ssl
from config import API_KEY, BASE_URL, MODELS, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, SYSTEM_PROMPT


class ChatGPTAgent:
    """إيجنت ChatGPT يدعم جميع النماذج عبر OpenRouter"""

    def __init__(self, model_id=None, system_prompt=None):
        self.api_key = API_KEY
        self.base_url = BASE_URL
        self.model = model_id or "openai/gpt-4o"
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.temperature = DEFAULT_TEMPERATURE
        self.max_tokens = DEFAULT_MAX_TOKENS
        self.conversation_history = []
        
        # إعداد SSL
        self.ssl_context = ssl.create_default_context()
        
        # إضافة system prompt للمحادثة
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })

    def set_model(self, model_id):
        """تغيير النموذج المستخدم"""
        self.model = model_id
        print(f"✅ تم تغيير النموذج إلى: {model_id}")

    def set_temperature(self, temp):
        """تغيير درجة الإبداع"""
        self.temperature = max(0.0, min(2.0, temp))
        print(f"🌡️ درجة الإبداع: {self.temperature}")

    def clear_history(self):
        """مسح سجل المحادثة"""
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]
        print("🗑️ تم مسح سجل المحادثة")

    def chat(self, user_message):
        """إرسال رسالة والحصول على رد"""
        
        # إضافة رسالة المستخدم للسجل
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # تجهيز الطلب
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/chatgpt-agent",
            "X-Title": "ChatGPT Agent"
        }

        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.base_url,
                data=data,
                headers=headers,
                method='POST'
            )

            with urllib.request.urlopen(req, context=self.ssl_context, timeout=120) as response:
                response_data = json.loads(response.read().decode('utf-8'))
            
            assistant_message = response_data["choices"][0]["message"]["content"]
            
            # إضافة رد المساعد للسجل
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # معلومات الاستخدام
            usage = response_data.get("usage", {})
            tokens_used = usage.get("total_tokens", "N/A")
            
            return {
                "success": True,
                "message": assistant_message,
                "model": response_data.get("model", self.model),
                "tokens": tokens_used
            }

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_data = json.loads(error_body)
                error_msg = error_data.get("error", {}).get("message", error_body)
            except:
                error_msg = error_body
            
            # إزالة الرسالة الفاشلة من السجل
            self.conversation_history.pop()
            return {
                "success": False,
                "message": f"❌ خطأ ({e.code}): {error_msg}",
                "model": self.model,
                "tokens": 0
            }

        except urllib.error.URLError as e:
            self.conversation_history.pop()
            return {
                "success": False,
                "message": f"🔌 خطأ في الاتصال: {str(e.reason)}",
                "model": self.model,
                "tokens": 0
            }

        except TimeoutError:
            self.conversation_history.pop()
            return {
                "success": False,
                "message": "⏱️ انتهت مهلة الاتصال - حاول مرة أخرى",
                "model": self.model,
                "tokens": 0
            }

        except Exception as e:
            self.conversation_history.pop()
            return {
                "success": False,
                "message": f"❌ خطأ غير متوقع: {str(e)}",
                "model": self.model,
                "tokens": 0
            }

    def get_available_models(self):
        """عرض النماذج المتاحة"""
        return MODELS

    def get_current_model(self):
        """الحصول على النموذج الحالي"""
        return self.model

    def get_conversation_length(self):
        """عدد الرسائل في المحادثة"""
        return len(self.conversation_history) - 1  # بدون system prompt
