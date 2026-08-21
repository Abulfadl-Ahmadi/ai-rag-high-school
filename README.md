# 🎓 AI High School Tutor (سامانه RAG آموزشی دبیرستان)
> **سامانه تخصصی هوش مصنوعی و بازیابی اطلاعات آموزشی (RAG) منطبق بر کتاب‌های درسی و استانداردهای امتحانات نهایی کشور (پایه دوازدهم)**

---

## 🧭 نقشه راه و دیاگرام جریان داده (End-to-End Data Flow)

جریان پردازش هر پرسش دانش‌آموز از لحظه ارسال در فرانت‌اند تا پاسخ استریم‌شده به صورت زیر انجام می‌پذیرد:

```mermaid
flowchart TD
    User([👨‍🎓 دانش‌آموز / کاربر]) -->|ارسال پیام یا سوال درسی| Frontend[💻 فرانت‌اند Next.js / Single Page]
    
    subgraph Backend [🖥️ بک‌اند جنگو - Django REST & Streaming API]
        Endpoint[🌐 Endpoint: /api/stream/ یا /api/chat/ask/]
        Session[🗂️ مدیریت نشست Conversation & Messages]
        
        subgraph Retrieval [🔍 موتور بازیابی هیبریدی Hybrid Search]
            Dense[🧬 Dense Vector Search\nBGE-M3 Embeddings 1024d\npgvector Cosine Distance]
            Sparse[📚 Sparse BM25 Search\nBM25-IDF + Persian Tokenizer]
            RRF[⚖️ Reciprocal Rank Fusion - RRF\nترکیب و بازرتبه‌بندی نتایج برتر]
        end
        
        ContextEngine[📑 ساخت کانتکست و استنادات ContextBuilder]
        PromptEngine[🎯 موتور سیستم پرامپت پداگوژیک Pedagogical Prompt]
        
        subgraph LLM_Layer [⚡ لایه استنتاج هوش مصنوعی LLM Gateway]
            Factory[🏭 LLMFactory]
            Provider[🌐 OpenAICompatibleProvider\nDeepSeek-V4-Flash / Gemma-4]
        end
    end
    
    subgraph CloudAI [☁️ ArvanCloud AI Gateway]
        LiveLLM[🧠 مدل‌های آنلاین DeepSeek V4 Flash / Gemma 4 31B]
    end
    
    Frontend --> Endpoint
    Endpoint --> Session
    Endpoint --> Retrieval
    Dense --> RRF
    Sparse --> RRF
    RRF --> ContextEngine
    ContextEngine --> PromptEngine
    PromptEngine --> Factory
    Factory --> Provider
    Provider -->|HTTPS POST Stream:True| LiveLLM
    LiveLLM -->|SSE Delta Tokens| Provider
    Provider -->|SSE Event Stream| Endpoint
    Endpoint -->|Server-Sent Events| Frontend
    Frontend -->|رندر بلادرنگ پاسخ + نمایش منبع درس و صفحه| User
```

---

## 🔄 جریان دقیق گام‌به‌گام سامانه (Step-by-Step Execution Lifecycle)

### ۱. دریافت پرسش و مدیریت نشست (Request Ingestion & Session Management)
* دانش‌آموز پرسش درسی، شبهه مفهومی یا سوال تستی/تشریحی خود را از طریق فرانت‌اند مدرن ارسال می‌کند.
* کنترلر [`views.py`](file:///f:/ai_rag_high_school/backend/knowledge/views.py) شناسه گفتگوی فعال (`Conversation`) را بازیابی یا ایجاد کرده و پیام کاربر را در پایگاه داده ثبت می‌کند.
* شماره درس هدف به‌صورت خودکار از فیلتر انتخابی یا از طریق آنالیز متن پرسش شناسایی می‌شود.

---

### ۲. موتور جستجوی هیبریدی ترکیبی (Hybrid Retrieval: Dense + Sparse BM25)
برای دستیابی به بالاترین دقت بازیابی متون درسی، فرآیند جستجو به صورت ۲ مسیره موازی در [`hybrid_search.py`](file:///f:/ai_rag_high_school/backend/knowledge/retrieval/hybrid_search.py) اجرا می‌شود:
1. **جستجوی برداری متراکم (Dense Vector Search):**
   * تبدیل سوال به بردار ۱۰۲۴ بعدی با مدل `BAAI/bge-m3`.
   * مقایسه کسینوسی با بردارهای چانک‌های کتاب درسی در پایگاه داده PostgreSQL مجهز به اکستنشن `pgvector`.
2. **جستجوی متنی تنک (Sparse BM25 Search):**
   * توکنایز و نرمال‌سازی فارسی عبارات، حذف کلمات ایستای غیرآموزشی و وزن‌دهی BM25-IDF.
3. **ادغام رتبه‌ها با Reciprocal Rank Fusion (RRF):**
   * ادغام نتایج دو روش جستجو بر اساس فرمول:
     $$RRF(d) = \sum_{m \in \{Dense, BM25\}} \frac{1}{60 + rank_m(d)}$$
   * انتخاب $K$ قطعه با بالاترین امتیاز ارتباط آموزشی.

---

### ۳. استخراج کانتکست و استنادات آموزشی (Context & Citation Extraction)
* کلاس [`ContextBuilder`](file:///f:/ai_rag_high_school/backend/knowledge/retrieval/context_builder.py) قطعات برتر را به همراه متاداده‌های ساختاریافته (شماره درس، عنوان درس، شماره صفحات، شناسه چانک) جمع‌آوری می‌کند.
* فرمت مشخصی از مستندات بازیابی‌شده کتاب درسی تشکیل می‌شود تا مدل بتواند عینا به صفحات کتاب ارجاع دهد.

---

### ۴. موتور سیستم پرامپت پداگوژیک (Pedagogical Prompt Engine)
* ماژول [`pedagogy.py`](file:///f:/ai_rag_high_school/backend/knowledge/ai/pedagogy.py) وظیفه ساخت پرامپت نهایی را بر عهده دارد:
  * **System Prompt:** تعریف پرسونا به عنوان دبیر و متخصص آموزش رسمی کتاب دین و زندگی ۳ پایه دوازدهم.
  * **قوانین پاسخ‌دهی:** التزام ۱۰۰٪ به محتوای بازیابی‌شده کتاب درسی، رعایت ادبیات تصحیح امتحانات نهایی، تفکیک متن و پیام آیات، و پاسخ محترمانه به سلام و مکالمات عمومی.
  * **Context Injection:** تزریق قطعات استخراج‌شده در بخش `محتوای معتبر بازیابی‌شده از کتاب درسی`.

---

### ۵. استنتاج و استریم زنده مدل زبانی (Pure Live LLM & SSE Streaming)
* ماژول [`providers.py`](file:///f:/ai_rag_high_school/backend/knowledge/ai/providers.py) با پروتکل استاندارد `OpenAICompatibleProvider` به گیت‌وی ابری (مانند ArvanCloud AI) متصل است:
  * مدل‌های فعال: **`DeepSeek-V4-Flash`** و **`Gemma-4-31B-IT`**.
  * استریم واقعی و بلادرنگ (Native Server-Sent Events): توکن‌ها به محض تولید توسط هوش مصنوعی از طریق بستر SSE بدون تاخیر به سمت کلاینت پمپاژ می‌شوند.
  * **فاقد هرگونه پاسخ آفلاین یا شبیه‌ساز ساختگی:** کل پاسخ‌ها به‌صورت ۱۰۰٪ زنده از مدل هوش مصنوعی تولید می‌شوند.

---

### ۶. رندر زنده و بازرسی منبع در فرانت‌اند (Real-Time UI & Citations)
* فرانت‌اند داده‌های دریافتی را به صورت توکن‌به‌توکن نمایش می‌دهد.
* ارجاعات رسمی `[درس X، صفحه Y]` به عنوان برچسب‌های تعاملی دراور منبع (Source Inspector) در دسترس دانش‌آموز قرار می‌گیرند.

---

## 📊 دیاگرام توالی تعاملات (Interaction Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor Student as 👨‍🎓 دانش‌آموز
    participant UI as 💻 فرانت‌اند
    participant API as 🌐 جنگو API
    participant Hybrid as 🔍 موتور جستجو (HybridSearch)
    participant PG as 🗄️ PostgreSQL (pgvector)
    participant Prompt as 🎯 PromptEngine
    participant LLM as 🧠 ArvanCloud AI (DeepSeek/Gemma)

    Student->>UI: تایپ سوال (مثال: "پیام آیه ۱۵ سوره فاطر چیست؟")
    UI->>API: POST /api/stream/ (یا SSE EventSource)
    API->>Hybrid: search(query, top_k=4)
    Hybrid->>PG: جستجوی BM25 + شباهت کسینوسی برداری (BGE-M3)
    PG-->>Hybrid: بازگرداندن قطعات درسی مرتبط
    Hybrid-->>API: رتبه‌بندی نهایی قطعات (RRF)
    API->>Prompt: assemble_prompt(question, context_text)
    Prompt-->>API: System Prompt + Context Chunks + User Message
    API->>LLM: POST /chat/completions (stream=True)
    LLM-->>API: استریم خط‌به‌خط توکن‌ها (SSE chunks)
    API-->>UI: ارسال داده‌های بلادرنگ (event: delta)
    UI-->>Student: نمایش کلمه به کلمه پاسخ + کارت‌های استناد درس و صفحه
```

---

## 🛠️ پشته فناوری (Tech Stack)

| لایه | تکنولوژی‌های به‌کار رفته | وظیفه اصلی |
| :--- | :--- | :--- |
| **Backend** | Python 3.12, Django 5.x, Django REST Framework | هسته مرکزی سامانه، منطق RAG و API |
| **Database & Vector** | PostgreSQL 16+ / SQLite, pgvector extension | پایگاه داده و ذخیره‌سازی بردارهای ۱۰۲۴ بعدی |
| **Embeddings** | BAAI/bge-m3 (Dense 1024-dim) | تعبیه‌سازی معنایی متن کتب درسی و پرسش‌ها |
| **Retrieval** | BM25-IDF + Dense Vector Search + RRF | بازیابی ترکیبی کلمات کلیدی و مفاهیم معنایی |
| **LLM Inference** | DeepSeek-V4-Flash / Gemma-4-31B-IT (ArvanCloud Gateway) | استنتاج زنده، تولید محتوای آموزشی و استریم |
| **Frontend** | Next.js 14+, Tailwind CSS, assistant-ui, RTL Support | رابط کاربری چت، بازرس منبع و تعامل دروس |

---

## 🚀 راهنمای گام‌به‌گام راه‌اندازی و اجرای مجدد پروژه (Step-by-Step Setup Guide)

اگر قصد دارید این پروژه را از ابتدا بر روی یک سیستم جدید راه‌اندازی کنید، مراحل زیر را به ترتیب انجام دهید:

### 📋 پیش‌نیازها (Prerequisites)
1. **Python 3.10+** (پیشنهادی: پایتون ۳.۱۲)
2. **Node.js 18+** و **npm** (برای فرانت‌اند Next.js)
3. **Git**
4. **Docker & Docker Compose** *(اختیاری - برای اجرای PostgreSQL مجهز به pgvector)*

---

### گام ۱: دریافت سورس پروژه (Clone Repository)
ابتدا مخزن را از گیت‌هاب کلون کرده و وارد پوشه پروژه شوید:
```bash
git clone https://github.com/Abulfadl-Ahmadi/ai-rag-high-school.git
cd ai-rag-high-school
```

---

### گام ۲: راه‌اندازی پایگاه داده (Database Setup)

#### روش اول: اجرای خودکار با داکر (پیشنهادی برای pgvector)
دستور زیر کانتینر پایگاه داده PostgreSQL مجهز به اکستنشن `pgvector` را بالا می‌آورد:
```bash
docker-compose up -d
```

#### روش دوم: اجرای لوکال با SQLite (بدون نیاز به داکر)
سامانه به‌صورت خودکار در حالت پیش‌فرض برای توسعه محلی سبک از SQLite3 با پشتیبانی از جستجوی متنی و برداری استفاده می‌کند و بدون هیچ پیش‌نیاز دیتابیسی اجرا خواهد شد.

---

### گام ۳: راه‌اندازی محیط و بک‌اند جنگو (Backend Setup)

1. **ساخت و فعال‌سازی محیط مجازی پایتون:**
   * **ویندوز (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **لینوکس / مک (Bash):**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

2. **نصب وابستگی‌های پایتون:**
   ```bash
   pip install -r requirements.txt
   ```

3. **اعمال ساختار پایگاه داده (Migrations):**
   ```bash
   python backend/manage.py migrate
   ```

4. **تزریق و اینجِست داده‌های کتاب درسی و سوالات امتحان نهایی:**
   ```bash
   python backend/manage.py ingest_curriculum
   ```
   *(این دستور متن کامل دروس کتاب دین و زندگی ۳، آیات، واژگان و سوالات امتحانی را با بردارهای معنایی در دیتابیس بارگذاری می‌کند).*

5. **اجرای سرور بک‌اند جنگو:**
   ```bash
   python backend/manage.py runserver 127.0.0.1:8000
   ```
   اکنون API بک‌اند در آدرس `http://127.0.0.1:8000/` آماده دریافت درخواست‌ها است.

---

### گام ۴: راه‌اندازی فرانت‌اند Next.js (Frontend Setup)

در یک پنجره ترمینال جدید وارد پوشه فرانت‌اند شوید:

1. **ورود به پوشه فرانت‌اند:**
   ```bash
   cd frontend-next
   ```

2. **نصب پکیج‌های جاوااسکریپت:**
   ```bash
   npm install
   ```

3. **اجرای سرور توسعه فرانت‌اند:**
   ```bash
   npm run dev
   ```

4. **مشاهده در مرورگر:**
   آدرس زیر را در مرورگر خود باز کنید:
   👉 **`http://localhost:3000`**

---

### گام ۵: اجرای ارزیابی کیفی و تست‌های خودکار (Evaluation & Testing)

* **اجرای ارزیابی ۵۰ سوال استاندارد امتحانات نهایی (Benchmark Evaluation):**
  ```bash
  python backend/manage.py run_evaluation
  ```
  *(خروجی معیارهای Recall@5, MRR و دقت استناد آموزشی را اعتبارسنجی می‌کند).*

* **اجرای تست‌های واحد بک‌اند (Unit Tests):**
  ```bash
  python backend/manage.py test knowledge
  ```

---

## ⚙️ متغیرهای محیطی اختیاری (Environment Variables)

در صورت تمایل به تغییر کلیدها یا گیت‌وی مدل‌های هوش مصنوعی می‌توانید فایل `.env` را در ریشه بک‌اند تنظیم کنید:

| نام متغیر | مقدار پیش‌فرض | توضیحات |
| :--- | :--- | :--- |
| `ARVAN_API_KEY` | کلید پیش‌فرض سامانه | توکن دسترسی به گیت‌وی ابری آروان |
| `DEEPSEEK_GATEWAY_URL` | گیت‌وی اختصاصی DeepSeek | آدرس Endpoint مدل DeepSeek-V4-Flash |
| `GEMMA_GATEWAY_URL` | گیت‌وی اختصاصی Gemma | آدرس Endpoint مدل Gemma-4-31B-IT |

---
⭐ **توسعه‌یافته به صورت کاملاً فارسی، استاندارد و هماهنگ با اهداف برنامه درسی ملی ایران.**


