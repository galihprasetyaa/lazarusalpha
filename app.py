import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# Konfigurasi halaman
st.set_page_config(page_title="Data Processing App", layout="wide")

# Fungsi untuk konversi dataframe ke excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.read()

# Fungsi untuk membuat link download
def get_table_download_link(df, filename, text):
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">{text}</a>'

# Header aplikasi
st.title("Data Processing Application")
st.markdown("Upload your CSV file and process your data with ease!")

# Sidebar untuk upload file
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

# Main content
if uploaded_file is not None:
    try:
        # Membaca file CSV dengan fallback encoding
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='latin1')
        
        # Menampilkan data awal
        st.subheader("Original Data")
        st.write(f"Shape: {df.shape}")
        st.dataframe(df.head())

        # Tab untuk berbagai proses
        tab1, tab2, tab3 = st.tabs(["Data Cleaning", "Data Analysis", "Visualization"])

        with tab1:
            st.subheader("Data Cleaning Options")

            col1, col2 = st.columns(2)

            with col1:
                remove_duplicates = st.checkbox("Remove duplicates")
                drop_na = st.checkbox("Drop missing values")

            with col2:
                numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
                fill_na_column = st.selectbox("Fill NA for column", ['None'] + numeric_columns)
                fill_method = st.selectbox("Fill method", ['mean', 'median', 'mode'])

            cleaned_df = df.copy()
            if remove_duplicates:
                cleaned_df = cleaned_df.drop_duplicates()
            if drop_na:
                cleaned_df = cleaned_df.dropna()
            if fill_na_column != 'None':
                if fill_method == 'mean':
                    cleaned_df[fill_na_column] = cleaned_df[fill_na_column].fillna(cleaned_df[fill_na_column].mean())
                elif fill_method == 'median':
                    cleaned_df[fill_na_column] = cleaned_df[fill_na_column].fillna(cleaned_df[fill_na_column].median())
                else:
                    cleaned_df[fill_na_column] = cleaned_df[fill_na_column].fillna(cleaned_df[fill_na_column].mode().iloc[0])

            st.write("Cleaned Data Preview")
            st.dataframe(cleaned_df.head())
            st.markdown(get_table_download_link(cleaned_df, 'cleaned_data.xlsx', '📥 Download cleaned data'), unsafe_allow_html=True)

        with tab2:
            st.subheader("Data Analysis")
            st.write("Descriptive Statistics")
            st.dataframe(cleaned_df.describe())

            if len(numeric_columns) > 1:
                st.write("Correlation Matrix")
                corr = cleaned_df[numeric_columns].corr()
                fig, ax = plt.subplots()
                sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)
            else:
                st.info("Not enough numeric columns for correlation analysis.")

        with tab3:
            st.subheader("Data Visualization")

            if len(numeric_columns) == 0:
                st.warning("No numeric columns available for plotting.")
            else:
                plot_type = st.selectbox("Select plot type", ['Histogram', 'Box Plot', 'Scatter Plot'])
                column_to_plot = st.selectbox("Select column", numeric_columns)

                if plot_type == 'Histogram':
                    fig, ax = plt.subplots()
                    cleaned_df[column_to_plot].hist(bins=30, ax=ax)
                    plt.title(f'Histogram of {column_to_plot}')
                    plt.xlabel(column_to_plot)
                    plt.ylabel('Count')
                    st.pyplot(fig)

                elif plot_type == 'Box Plot':
                    fig, ax = plt.subplots()
                    sns.boxplot(y=cleaned_df[column_to_plot], ax=ax)
                    plt.title(f'Box Plot of {column_to_plot}')
                    st.pyplot(fig)

                elif plot_type == 'Scatter Plot' and len(numeric_columns) > 1:
                    x_col = st.selectbox("Select X column", numeric_columns)
                    y_options = [col for col in numeric_columns if col != x_col]
                    y_col = st.selectbox("Select Y column", y_options)
                    fig, ax = plt.subplots()
                    ax.scatter(cleaned_df[x_col], cleaned_df[y_col])
                    ax.set_title(f'Scatter Plot: {x_col} vs {y_col}')
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
else:
    st.info("📂 Please upload a CSV file to begin.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Deployable to Streamlit Cloud")
