# Image Captioning & Audio Synthesis App (مستخرج وصانع الأوصاف الصوتية للصور)

An interactive web application built with **Flask** that generates detailed captions for uploaded images using a state-of-the-art vision-language model, translates them, and converts the descriptions into spoken audio in both English and Arabic.

تطبيق ويب تفاعلي مبني باستخدام **Flask** لتحليل محتوى الصور وتوليد وصف نصي وصوتي مفصل باللغتين العربية والإنجليزية باستخدام نماذج الذكاء الاصطناعي.

---

## 🚀 Features (المميزات)

* **Image Captioning (توليد أوصاف الصور)**: Uses the advanced **BLIP-2 (Flan-T5-XL)** model to analyze and generate accurate English descriptions for uploaded images.
* **Translation (ترجمة فورية)**: Automatically translates the generated English description into Arabic.
* **Text-to-Speech (تحويل النص إلى كلام)**: Converts both English and Arabic descriptions into high-quality MP3 audio files using Google Text-to-Speech (`gTTS`).
* **Interactive UI (واجهة تفاعلية)**: Clean, responsive user interface built with Bootstrap 5.
* **Ngrok Integration (مشاركة الخدمة)**: Built-in support for `pyngrok` to automatically expose the local server to a secure public URL.

---

## 🛠️ Project Structure (بنية المشروع)

* `app.py`: The main Flask server script containing ML inference, translation, and audio generation pipelines.
* `templates/index.html`: The frontend user interface template.
* `static/`: Contains static assets:
  * `uploads/`: Temporary directory for uploaded images (ignored in git).
  * `audio/`: Temporary directory for generated MP3 files (ignored in git).
* `.env.example`: Template for environment variables.
* `.gitignore`: Configured to exclude sensitive credentials, the python virtual environment, and user data.

---

## 💻 Tech Stack (التقنيات المستخدمة)

* **Backend**: Flask
* **Machine Learning**: `transformers` (Hugging Face), `torch` (PyTorch), `Pillow` (PIL)
* **APIs & Translation**: `googletrans` (Google Translate API)
* **Speech Synthesis**: `gTTS` (Google Text-to-Speech)
* **Tunnels**: `pyngrok` (Ngrok wrapper)
* **Frontend**: Bootstrap 5

---

## ⚙️ Installation & Setup (التثبيت والتشغيل)

### Prerequisites (المتطلبات الأساسية)
* Python 3.11 or 3.12 installed on your machine.
* Ngrok account and an Auth Token (free).

### Setup Steps (خطوات الإعداد)

1. **Clone the repository (نسخ المشروع)**:
   ```bash
   git clone <your-repository-url>
   cd FlaskProject
   ```

2. **Create and Activate Virtual Environment (إنشاء وتفعيل البيئة الافتراضية)**:
   * **Windows**:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * **macOS/Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies (تثبيت الحزم المطلوبة)**:
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is not available, install them manually)*:
   ```bash
   pip install flask transformers torch pillow gTTS googletrans==4.0.0rc1 pyngrok
   ```

4. **Configure Environment Variables (إعداد متغيرات البيئة)**:
   * Create a file named `.env` in the root directory (based on `.env.example`).
   * Add your Ngrok auth token inside it:
     ```env
     NGROK_AUTH_TOKEN=your_actual_ngrok_auth_token
     ```

5. **Run the Application (تشغيل التطبيق)**:
   ```bash
   python app.py
   ```
   * The app will start locally at `http://127.0.0.1:5000` and automatically output a public Ngrok tunnel URL (e.g. `https://xxxx.ngrok-free.app`) in the terminal.

---

## 🔒 Security (الأمان والحساسية)

* **No Credentials in Code**: All sensitive credentials (such as `NGROK_AUTH_TOKEN`) are loaded dynamically from the `.env` file, which is excluded from version control via `.gitignore`.
* **No User Data Uploaded**: User uploaded images and generated audio files in the `static/` folder are ignored by git, ensuring user privacy and keeping the repository clean.
