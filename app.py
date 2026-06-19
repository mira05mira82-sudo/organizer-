import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="منظم المسلسلات", page_icon="🎬", layout="wide")
st.title("🎬 برنامج تنظيم وترتيب المسلسلات")
st.write("تابع مسلسلاتك المفضلة وسجل تقدمك في المشاهدة بسهولة!")

# إنشاء قاعدة بيانات وهمية في الجلسة لحفظ البيانات مؤقتاً
if 'series_db' not in st.session_state:
    st.session_state.series_db = pd.DataFrame(columns=[
        "اسم المسلسل", "إجمالي الحلقات", "الحلقة الحالية", "حالة المشاهدة"
    ])

# قسم إضافة مسلسل جديد
st.subheader("➕ إضافة مسلسل جديد")
col1, col2, col3, col4 = st.columns(4)

with col1:
    name = st.text_input("اسم المسلسل")
with col2:
    total_episodes = st.number_input("عدد الحلقات الإجمالي", min_value=1, value=12)
with col3:
    current_episode = st.number_input("الحلقة التي توقفت عندها", min_value=0, value=0)
with col4:
    status = st.selectbox("هل شاهدته؟", ["لم أبدأ بعد", "جاري المشاهدة", "تمت المشاهدة بالكامل"])

if st.button("إضافة إلى القائمة"):
    if name:
        if name in st.session_state.series_db["اسم المسلسل"].values:
            st.warning("هذا المسلسل موجود بالفعل في القائمة!")
        else:
            new_data = pd.DataFrame([{
                "اسم المسلسل": name,
                "إجمالي الحلقات": total_episodes,
                "الحلقة الحالية": current_episode,
                "حالة المشاهدة": status
            }])
            st.session_state.series_db = pd.concat([st.session_state.series_db, new_data], ignore_index=True)
            st.success(f"تمت إضافة {name} بنجاح!")
    else:
        st.error("الرجاء إدخال اسم المسلسل.")

# قسم عرض وإدارة المسلسلات
st.subheader("📋 قائمة مسلسلاتك")

if not st.session_state.series_db.empty:
    edited_df = st.data_editor(
        st.session_state.series_db,
        num_rows="dynamic",
        column_config={
            "حالة المشاهدة": st.column_config.SelectboxColumn(
                options=["لم أبدأ بعد", "جاري المشاهدة", "تمت المشاهدة بالكامل"]
            )
        },
        use_container_width=True
    )
    st.session_state.series_db = edited_df
    st.info("💡 يمكنك تعديل الحلقات أو الحالة مباشرة من الجدول أعلاه، أو تحديد الصف والضغط على Delete لحذفه.")
else:
    st.write("قائمتك فارغة حالياً. أضف مسلسلك الأول في الأعلى! 🍿")
