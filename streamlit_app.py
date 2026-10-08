import streamlit as st
import json
import requests

# ----------------------------------------------------
# 0. إعدادات الصفحة والتنسيق
# ----------------------------------------------------
st.set_page_config(page_title="حاسبة النجم السابع الفلكية", page_icon="🌟", layout="centered")

SECRET_PASSCODE = "1234"

# ----------------------------------------------------
# 1. نظام الحماية ورمز الدخول (Passcode)
# ----------------------------------------------------
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

    if not GEMINI_API_KEY:
        st.warning("⚠️ تنبيه: لم يتم ضبط مفتاح `GEMINI_API_KEY` في إعدادات الأسرار (Secrets) على المنصة.")

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

        if not GEMINI_API_KEY:
            error_msg = "عذراً، مفتاح الـ API غير متوفر. يرجى إضافته في إعدادات التطبيق (Secrets)."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.write(error_msg)
        else:
            try:
                # استخدام النموذج المعتمد والمحدث gemini-2.5-flash
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
                
                context = f"قواعد ونصوص النجم السابع الفلكية:\n{json.dumps(lilly_data, ensure_ascii=False)}"
                full_prompt = f"أنت مساعد فلكي خبير ومتخصص في نظام 'النجم السابع' للتنجيم التقليدي.\nالسياق:\n{context}\n\nسؤال الزائر: {user_query}"

                payload = {
                    "contents": [{
                        "parts": [{"text": full_prompt}]
                    }]
                }

                with st.spinner("جاري التفكير وتحليل الخارطة..."):
                    response = requests.post(url, json=payload)
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        answer = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        error_details = res_json.get('error', {}).get('message', 'خطأ غير معروف')
                        answer = f"خطأ من الخادم: {error_details}"

                st.session_state.messages.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.write(answer)
                    
            except Exception as e:
                error_msg = f"حدث خطأ أثناء الاتصال بالمساعد: {e}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                with st.chat_message("assistant"):
                    st.error(error_msg)
