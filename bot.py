from flask import Flask, request

app = Flask(__name__)

# لتخزين التحذيرات
warnings = {}

# كلمات ممنوعة (روابط)
LINK_WORDS = ["https://", "http://", "www.", "t.me/", "chat.whatsapp.com", "wa.me/"]

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)

    # هذا مثال للواتساب - لو تستخدم مكتبة معينة غيره قول لي
    try:
        # 1- الترحيب بعضو جديد
        if data.get("action") == "add":
            group_id = data.get("group_id")
            new_member = data.get("participant")
            # هنا ترسل رسالة ترحيب
            print(f"مرحبا {new_member} نورت المجموعة! ممنوع الروابط ❄️")

        # 2- منع الروابط
        if "message" in data:
            message_text = data["message"].get("text", "")
            sender = data["message"].get("from")
            group_id = data["message"].get("group_id")

            # هل الرسالة فيها رابط؟
            if any(link in message_text for link in LINK_WORDS):
                print(f"رابط محذوف من {sender}: {message_text}")

                # عداد التحذيرات
                warnings[sender] = warnings.get(sender, 0) + 1

                if warnings[sender] >= 3:
                    # طرد بعد 3 مرات - تحتاج تربطه ب API الواتساب حقك
                    print(f"طرد {sender} بسبب تكرار الروابط")
                    warnings[sender] = 0
                    return f"تم طرد {sender} بسبب الروابط 🚫", 200
                else:
                    return f"تحذير {warnings[sender]}/3 لـ {sender}: ممنوع الروابط ⚠️", 200

    except Exception as e:
        print(f"خطأ: {e}")

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
