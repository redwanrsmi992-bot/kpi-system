import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="مؤشرات إنجاز المديريات", layout="wide")

st.title("📊 لوحة قياس أداء المديريات والوحدات")
st.markdown("---")

# 1. قاعدة بيانات المديريات (بيانات افتراضية يمكنك تعديلها)
data = {
    "المديرية": ["مديرية الشؤون المالية", "مديرية تكنولوجيا المعلومات", "مديرية المشاريع", "وحدة الرقابة الداحلية"],
    "المؤشر المستهدف %": [100, 100, 100, 100],
    "الإنجاز الفعلي %": [95, 88, 65, 92],
    "عدد المهام": [20, 15, 30, 10]
}

df = pd.DataFrame(data)

# 2. ملخص الأداء العام (Metrics)
avg_performance = df["الإنجاز الفعلي %"].mean()
c1, c2, c3 = st.columns(3)
c1.metric("متوسط أداء الدائرة", f"{avg_performance:.1f}%", delta="2.5% ▲")
c2.metric("أعلى مديرية إنجازاً", df.iloc[df['الإنجاز الفعلي %'].idxmax()]['المديرية'])
c3.metric("مديريات قيد المتابعة", len(df[df['الإنجاز الفعلي %'] < 70]))

st.divider()

# 3. الرسوم البيانية
col_left, col_right = st.columns(2)

with col_left:
    st.write("### 📈 مقارنة نسبة الإنجاز بين المديريات")
    fig = px.bar(df, x="المديرية", y="الإنجاز الفعلي %", color="الإنجاز الفعلي %",
                 color_continuous_scale=["red", "yellow", "green"], range_color=[50, 100])
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.write("### 📋 تفاصيل مؤشرات الأداء")
    # تلوين الجدول بناءً على الأداء
    def color_performance(val):
        color = 'red' if val < 70 else ('orange' if val < 90 else 'green')
        return f'color: {color}; font-weight: bold'
    
    st.dataframe(df.style.applymap(color_performance, subset=['الإنجاز الفعلي %']))

# 4. قسم تحليل المعيقات
st.sidebar.header("⚙️ إعدادات التقارير")
selected_dept = st.sidebar.selectbox("اختر المديرية للتفاصيل", df['المديرية'])
st.sidebar.write(f"تقرير الأداء المفصل لـ {selected_dept} جاهز للتحميل.")
st.sidebar.button("تحميل تقرير PDF")