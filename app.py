import streamlit as st
import json
import urllib.request

# ----------------------------------------------------
# 0. إعدادات الصفحة والتنسيق لشاشات الموبايل
# ----------------------------------------------------
st.set_page_config(
    page_title="حاسبة النجم السابع الفلكية",
    page_icon="🌟",
    layout="centered"
)

# ----------------------------------------------------
# 1. نظام الحماية ورمز الدخول (Passcode)
# ----------------------------------------------------
SECRET_PASSCODE = "1234"  # يمكنك تغيير كلمة السر هنا

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 دخول الأعضاء")
    st.subheader("يرجى إدخال رمز الدخول لفتح حاسبة النجم السابع الفلكية")
    
    passcode_input = st.text_input("رمز الدخول:", type="password")
    if st.button("تسجيل الدخول"):
        if passcode_input == SECRET_PASSCODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("رمز الدخول غير صحيح!")
    st.stop()

# ----------------------------------------------------
# 2. تحميل ملف قواعد وتفسيرات النجم السابع
# ----------------------------------------------------
@st.cache_data
def load_lilly_data():
    try:
        with open("lilly_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"خطأ في تحميل ملف lilly_data.json: {e}")
        return None

lilly_data = load_lilly_data()

# ----------------------------------------------------
# 3. الواجهة الرئيسية واستخراج البيانات
# ----------------------------------------------------
st.title("🌟 حاسبة الخارطة التقليدية (النجم السابع)")
st.write("أدخل بيانات الميلاد لاستخراج القواعد والتفسيرات الفلكية.")

col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input("تاريخ الميلاد")
    lat = st.number_input("خط العرض (Latitude)", value=33.5138, format="%.4f")
with col2:
    birth_time = st.time_input("وقت الميلاد")
    lon = st.number_input("خط الطول (Longitude)", value=36.2765, format="%.4f")

if st.button("🚀 استخراج الخارطة وتحليلها"):
    st.session_state.chart_generated = True

if st.session_state.get("chart_generated", False):
    st.markdown("---")
    st.header("📊 نتائج القواعد والتفسيرات")

    if lilly_data and "planets_in_houses" in lilly_data:
        st.subheader("✨ زحل (Saturn)")
        st.info(lilly_data["planets_in_houses"].get("Saturn", {}).get("1", "لا يوجد نص متاح لهذا البيت."))
        
        st.subheader("✨ المشتري (Jupiter)")
        st.success(lilly_data["planets_in_houses"].get("Jupiter", {}).get("1", "لا يوجد نص متاح لهذا البيت."))
    else:
        st.warning("يرجى التأكد من ملء وتنسيق ملف lilly_data.json بشكل صحيح.")

    st.markdown("---")
    st.subheader("💬 مساعد النجم السابع الذكي (Gemini)")

    # 🔑 مفتاح API الخاص بك:
    GEMINI_API_KEY = "AQ.Ab8RN6LP_zMbZNpaH709rDM2s5wF8KzZGpX-qzSwszI_9iEcUA"

    # تهيئة سجل المحادثة في الجلسة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض سجل الرسائل السابقة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # استقبال سؤال الزائر من مربع الدردشة
    user_query = st.chat_input("اسأل مساعد النجم السابع عن أي تفصيل في خريطتك...")
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # تجهيز سياق أمر النظام الموجه للذكاء الاصطناعي
        context = f"قواعد ونصوص النجم السابع المتاحة في الملف: {json.dumps(lilly_data, ensure_ascii=False)}"
        prompt_data = {
            "contents": [{
                "parts": [{
                    "text": f"أنت مساعد فلكي متخصص في برنامج 'النجم السابع' للتحليل الفلكي والتنجيم التقليدي.\nالسياق المتاح:\n{context}\n\nسؤال الزائر: {user_query}"
                }]
            }]
        }

        # إرسال الطلب مباشرة لـ Gemini REST API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        req = urllib.request.Request(
            url,
            data=json.dumps(prompt_data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with st.spinner("جاري التفكير والإجابة من مساعد النجم السابع..."):
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    answer = res_data["candidates"][0]["content"]["parts"][0]["text"]

            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)
        except Exception as e:
            st.error(f"حدث خطأ أثناء التواصل مع مساعد النجم السابع: {e}")