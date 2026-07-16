from flask import Flask, request, render_template, send_from_directory
import uuid
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
from PIL import Image
from gtts import gTTS
from googletrans import Translator
import os
from pyngrok import ngrok

# تحميل متغيرات البيئة من ملف .env إن وجد
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

# تعيين مفتاح ngrok الخاص بك
ngrok_token = os.environ.get("NGROK_AUTH_TOKEN")
if ngrok_token:
    ngrok.set_auth_token(ngrok_token)
else:
    print("Warning: NGROK_AUTH_TOKEN is not set in environment or .env file.")

# تحقق من وجود المجلدات
if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")
if not os.path.exists("static/audio"):
    os.makedirs("static/audio")

# تحميل النموذج (BLIP-2 مع Flan-T5-XL)
processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl").to("cuda" if torch.cuda.is_available() else "cpu")

def predict_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_length=60,  # تحسين طول النص
        num_beams=5,  # زيادة عدد الحزم لتحسين جودة التوليد
        temperature=0.7,  # تحسين التوليد بمرونة
        top_k=50,
        top_p=0.95
    )
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption.strip()

# دالة لتحويل النص إلى صوت
def text_to_audio(text, language, output_file):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)

# إعداد Flask
app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            unique_id = str(uuid.uuid4())
            image_path = os.path.join("static/uploads", f"image_{unique_id}.jpg")
            file.save(image_path)

            # توليد النصوص
            caption = predict_caption(image_path)

            # ترجمة النصوص إلى العربية
            translator = Translator()
            caption_ar = translator.translate(caption, dest='ar').text

            # إنشاء ملفات الصوت
            en_audio_path = os.path.join("static/audio", f"output_en_{unique_id}.mp3")
            ar_audio_path = os.path.join("static/audio", f"output_ar_{unique_id}.mp3")
            text_to_audio(caption, "en", en_audio_path)
            text_to_audio(caption_ar, "ar", ar_audio_path)

            return render_template(
                "index.html",
                caption=caption,
                caption_ar=caption_ar,
                en_audio_path=en_audio_path.replace("static/", ""),
                ar_audio_path=ar_audio_path.replace("static/", "")
            )
    return render_template("index.html", caption=None, caption_ar=None)

# لتقديم ملفات الصوت
@app.route('/static/<path:filename>')
def send_static(filename):
    return send_from_directory('static', filename)

# تشغيل التطبيق
if __name__ == "__main__":
    public_url = ngrok.connect(5000).public_url
    print(f"Public URL: {public_url}")
    app.run(port=5000)
