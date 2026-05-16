#!/usr/bin/env python3
"""
🤖 ChatGPT Agent - واجهة تفاعلية
إيجنت شات جي بي تي مع جميع النماذج عبر OpenRouter
(لا يحتاج مكتبات خارجية - يعمل مباشرة)
"""

import os
import sys

from agent import ChatGPTAgent
from config import MODELS


def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')


def print_banner():
    """عرض البانر الترحيبي"""
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║       🤖 ChatGPT Agent - OpenRouter             ║")
    print("║       جميع نماذج الشات (Plus + العادي)          ║")
    print("╚══════════════════════════════════════════════════╝")
    print()


def show_models():
    """عرض قائمة النماذج المتاحة"""
    print("\n📋 النماذج المتاحة:")
    print("─" * 60)
    print(f"  {'#':<4} {'النموذج':<22} {'الوصف'}")
    print("─" * 60)
    for key, model in MODELS.items():
        print(f"  [{key:<2}] {model['name']:<20} {model['description']}")
    print("─" * 60)


def show_help():
    """عرض قائمة الأوامر"""
    print("""
📌 الأوامر المتاحة:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /models     - عرض النماذج المتاحة
  /switch     - تغيير النموذج
  /clear      - مسح سجل المحادثة
  /temp       - تغيير درجة الإبداع (0.0 - 2.0)
  /info       - معلومات الجلسة الحالية
  /help       - عرض هذه القائمة
  /quit       - الخروج
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💡 اكتب أي شيء للدردشة مع الإيجنت
""")


def select_model():
    """اختيار نموذج من القائمة"""
    show_models()
    print()
    choice = input("🔢 اختر رقم النموذج: ").strip()
    
    if choice in MODELS:
        return MODELS[choice]["id"], MODELS[choice]["name"]
    else:
        print("❌ اختيار غير صحيح")
        return None, None


def main():
    """الدالة الرئيسية"""
    clear_screen()
    print_banner()
    
    # اختيار النموذج الابتدائي
    print("🚀 اختر النموذج للبدء:\n")
    show_models()
    print()
    
    choice = input("🔢 اختر رقم النموذج (أو Enter لـ GPT-4o): ").strip()
    
    if choice in MODELS:
        selected_model = MODELS[choice]["id"]
        model_name = MODELS[choice]["name"]
    else:
        selected_model = "openai/gpt-4o"
        model_name = "GPT-4o"
    
    # إنشاء الإيجنت
    agent = ChatGPTAgent(model_id=selected_model)
    
    clear_screen()
    print_banner()
    print(f"✅ النموذج الحالي: {model_name}")
    print("💬 اكتب /help لعرض الأوامر\n")
    print("─" * 50)
    
    # حلقة المحادثة الرئيسية
    while True:
        try:
            user_input = input("\n👤 أنت: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 مع السلامة!")
            break
        
        if not user_input:
            continue
        
        # معالجة الأوامر
        if user_input.startswith("/"):
            command = user_input.lower().split()[0]
            
            if command in ("/quit", "/exit"):
                print("\n👋 مع السلامة!")
                break
            
            elif command == "/models":
                show_models()
            
            elif command == "/switch":
                new_model, new_name = select_model()
                if new_model:
                    agent.set_model(new_model)
                    model_name = new_name
            
            elif command == "/clear":
                agent.clear_history()
            
            elif command == "/temp":
                try:
                    parts = user_input.split()
                    if len(parts) > 1:
                        temp = float(parts[1])
                    else:
                        temp = float(input("🌡️ أدخل درجة الإبداع (0.0 - 2.0): "))
                    agent.set_temperature(temp)
                except ValueError:
                    print("❌ أدخل رقم صحيح")
            
            elif command == "/info":
                print(f"""
📊 معلومات الجلسة:
  🤖 النموذج: {model_name} ({agent.get_current_model()})
  🌡️ الإبداع: {agent.temperature}
  💬 الرسائل: {agent.get_conversation_length()}
  📏 الحد الأقصى: {agent.max_tokens} tokens
""")
            
            elif command == "/help":
                show_help()
            
            else:
                print("❌ أمر غير معروف - اكتب /help")
            
            continue
        
        # إرسال الرسالة للإيجنت
        print("\n⏳ جاري التفكير...", end="", flush=True)
        
        result = agent.chat(user_input)
        
        # مسح سطر "جاري التفكير"
        print("\r" + " " * 30 + "\r", end="")
        
        if result["success"]:
            print(f"\n🤖 {model_name}:")
            print(f"{result['message']}")
            print(f"\n  📊 Tokens: {result['tokens']}")
        else:
            print(f"\n{result['message']}")
        
        print("\n" + "─" * 50)


if __name__ == "__main__":
    main()
