import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="مؤشرات إنجاز القطاعات والمديريات", layout="wide", page_icon="📊")

# تنسيق العناوين
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1 { color: #1e3a8a; text-align: center; border-bottom: 2px solid #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 لوحة قياس الأداء المؤسسي والقطاعي")
st.markdown("---")

# 1. قاعدة البيانات الشاملة (المديريات من الصورة + الإضافات)
data = {
    "الجهة / المديرية": [
        "مديرية قطاع الإدارة المالية والتخطيط", "مديرية قطاع الإدارة العامة", 
        "مديرية قطاع الدفاع والأمن", "مديرية قطاع القضاء والشؤون الدينية",
        "مديرية قطاع البنية التحتية والتنمية المحلية", "مديرية قطاع الصحة والتنمية الاجتماعية",
        "مديرية قطاع التنمية الزراعية والثروة الطبيعية", "مديرية قطاع التعليم وتنمية الموارد البشرية",
        "مديرية قطاع السياحة وتعزيز البيئة الاستثمارية", "مديرية قطاع الثقافة والشباب والإعلام",
        "وحدة المتابعة والتقييم", "وحدة اللامركزية", 
        "وحدة تطوير الأداء المؤسسي", "وحدة الرقابة الداخلية", 
        "مديرية الدراسات", "مديرية الحاسوب والمعرفة", "مديرية الشؤون الإدارية والمالية"
    ],
    "المستهدف %": [100] * 17,
    "الإنجاز الفعلي %": [92, 85, 95, 78, 88, 72, 65, 90, 82, 77, 94, 80, 89, 91, 75, 98, 87],
    "عدد المهام": [12, 15, 10, 8, 20, 14, 9, 25, 11, 13, 7, 5, 18, 10, 22, 30, 28]
}

df = pd.DataFrame(data)

# 2. ملخص الأداء العام
m1, m2, m3 = st.columns(3)
avg_perf = df["الإنجاز الفعلي %"].mean()
m1.metric("متوسط الإنجاز العام", f"{avg_perf:.1f}%")
m2.metric("عدد الوحدات المنجزة (>90%)", len(df[df["الإنجاز الفعلي %"] >= 90]))
m3.metric("وحدات تحت المتابعة (<70%)", len(df[df["الإنجاز الفعلي %"] < 70]))

st.divider()

# 3. الرسوم البيانية
col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("### 📈 تحليل مقارنة الأداء بين القطاعات والمديريات")
    fig = px.bar(df, x="الجهة / المديرية", y="الإنجاز الفعلي %", 
                 color="الإنجاز الفعلي %", text="الإنجاز الفعلي %",
                 color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"], 
                 range_color=[60, 100])
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.write("### 📋 تفاصيل مؤشرات الأداء")
    
    # دالة تلوين الخلايا (تم تحديثها لتعمل مع الإصدارات الجديدة)
    def color_performance(val):
        if isinstance(val, (int, float)):
            color = '#dcfce7' if val >= 90 else ('#fef3c7' if val >= 75 else '#fee2e2')
            return f'background-color: {color}'
        return ''

    st.dataframe(df.style.map(color_performance, subset=['الإنجاز الفعلي %']), use_container_width=True)

# 4. تحليل مخصص لكل مديرية
st.sidebar.header("🔍 تفاصيل المديرية")
selected = st.sidebar.selectbox("اختر الجهة للمراجعة:", df["الجهة / المديرية"])
dept_data = df[df["الجهة / المديرية"] == selected].iloc[0]
st.sidebar.info(f"المديرية: {selected}\n\nالإنجاز: {dept_data['الإنجاز الفعلي %']}%\n\nالمهام الكلية: {dept_data['عدد المهام']}")

if dept_data['الإنجاز الفعلي %'] < 75:
    st.sidebar.error("⚠️ تنبيه: هذه الجهة تحتاج لخطة تصحيحية فورية.")
