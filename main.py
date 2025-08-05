import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="HR Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data(file):
    if isinstance(file, str):
        if file.endswith(".csv"):
            return pd.read_csv(file)
        return pd.read_excel(file)
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)


# 사이드바 영역 -----------------------------------------------------------
st.sidebar.title("설문 데이터")
uploaded = st.sidebar.file_uploader("데이터를 업로드하세요", type=["xlsx", "csv"])

if uploaded is not None:
    df = load_data(uploaded)
else:
    df = load_data("퇴직자설문조사1.0.xlsx")

st.sidebar.header("필터")
dept = st.sidebar.multiselect("부서", df["부서"].unique(), default=df["부서"].unique())
gender = st.sidebar.multiselect("성별", df["성별"].unique(), default=df["성별"].unique())
position = st.sidebar.multiselect("직위", df["직위"].unique(), default=df["직위"].unique())

group_var = st.sidebar.radio("분석 기준", ["부서", "성별", "직위"], index=0)

df_filtered = df[
    (df["부서"].isin(dept)) &
    (df["성별"].isin(gender)) &
    (df["직위"].isin(position))
]

# 메인 페이지 --------------------------------------------------------------
st.title(":bar_chart: HR Dashboard")

metrics = [
    "직무경험",
    "재입사여부",
    "지인 입사권유",
    "경영철학",
    "다양성",
    "리더십",
    "커뮤니케이션",
    "성과관리 제도",
    "상사역량",
    "직속상사 관계",
    "동일부서 직원 관계",
    "타부서 직원 관계",
    "역할과 책임",
    "역량개발 기회",
    "보상",
    "복리후생",
    "근무환경",
    "근무시간",
    "회사위치",
]

cols = st.columns(3)
for i, metric in enumerate(metrics):
    grouped = (
        df_filtered.groupby(group_var)[metric]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        grouped,
        x=group_var,
        y=metric,
        title=f"{group_var}별 {metric} 평균",
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="평균",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    with cols[i % 3]:
        st.plotly_chart(fig, use_container_width=True)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

