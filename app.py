import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PSET4 Arhai Batsuuri", layout="wide")
st.title("Arhai Batsuuri")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    df = df.drop_duplicates().fillna(0)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    all_cols = df.columns.tolist()

    if len(numeric_cols) >= 1:
        st.subheader("Select Columns for Visualization")

        chart_type = st.selectbox(
            "Chart Type",
            [
                "Scatter",
                "Line",
                "Bar",
                "Histogram",
                "Box",
                "Area",
                "Pie",
                "Heatmap"
            ]
        )

        if chart_type in ["Scatter", "Line", "Bar", "Area"]:
            x_col = st.selectbox("X-Axis", numeric_cols)
            y_col = st.selectbox("Y-Axis", numeric_cols)

        if chart_type == "Pie":
            cat_col = st.selectbox("Category Column", all_cols)
            val_col = st.selectbox("Value Column", numeric_cols)

        if chart_type == "Box":
            box_col = st.selectbox("Column", numeric_cols)

        if chart_type == "Histogram":
            hist_col = st.selectbox("Column", numeric_cols)

        if chart_type == "Heatmap":
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        else:
            if chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col)
            elif chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col)
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col)
            elif chart_type == "Area":
                fig = px.area(df, x=x_col, y=y_col)
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=hist_col)
            elif chart_type == "Box":
                fig = px.box(df, y=box_col)
            elif chart_type == "Pie":
                fig = px.pie(df, names=cat_col, values=val_col)

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric columns found.")
else:
    st.info("Upload a CSV file to start.")
