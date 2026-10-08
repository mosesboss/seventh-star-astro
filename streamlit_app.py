import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="حاسبة النجم السابع الفلكية", page_icon="🌟", layout="centered")

SECRET_PASSCODE = "1234"

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

@st.cache_data
def load_lilly_data():
    try:
        with open("lilly_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return None

lilly_data = load_lilly_data()

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

    if lilly_data and "planet_in_houses" in lilly_data:
        st.subheader("✨ زحل (Saturn)")
        st.info(lilly_data["planet_in_houses"].get("Saturn", {}).get("1", "لا يوجد نص متاح."))
        
        st.subheader("✨ المشتري (Jupiter)")
        st.success(lilly_data["planet_in_houses"].get("Jupiter", {}).get("1", "لا يوجد نص متاح."))
    else:
        st.warning("يرجى التحقق من محتوى ملف lilly_data.json في المستودع.")

    st.markdown("---")
    st.subheader("💬 مساعد النجم السابع الذكي (Gemini)")
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_query = st.chat_input("اسأل مساعد النجم السابع عن تفاصيل خريطتك...")
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        if GEMINI_API_KEY:
            context = f"قواعد النجم السابع: {json.dumps(lilly_data, ensure_ascii=False)}"
            prompt_data = {
                "contents": [{
                    "parts": [{"text": f"أنت مساعد فلكي لنظام النجم السابع.\nالسياق:\n{context}\n\nسؤال المستخدم: {user_query}"}]
                }]
            }
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
            req = urllib.request.Request(url, data=json.dumps(prompt_data).encode("utf-8"), headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    answer = res_data["candidates"][0]["content"]["parts"][0]["text"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.write(answer)
            except Exception as e:
                st.error(f"خطأ في الاتصال: {e}")
