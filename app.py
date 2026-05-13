import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration
st.set_page_config(page_title="Bank Churn Executive Dashboard", layout="wide")

# 2. Title & Introduction
st.title("🏦 European Banking Churn Executive Dashboard")
st.markdown("This dashboard provides real-time insights into customer attrition across European regions, focusing on demographic and financial risk factors.")

# 3. Data Loading
@st.cache_data
def load_data():
    # Loading the dataset from your local directory
    df = pd.read_csv('bank_churn_analysis.csv')
    
    # Pre-processing: Create groups 'on the fly' to prevent KeyErrors
    if 'Credit_Score_Group' not in df.columns:
        df['Credit_Score_Group'] = pd.cut(df['CreditScore'], 
                                         bins=[300, 500, 600, 700, 850], 
                                         labels=['Low', 'Fair', 'Good', 'Excellent'])
    return df

df_raw = load_data()

# Professional Radiant Red Palette
radiant_reds = ["#b23b3b", "#d35d5d", "#e89696", "#f2c2c2"]
dark_red = "#b23b3b"
neutral_gray = "#d3d3d3"

# 4. Sidebar Global Filters
st.sidebar.header("Global Filters")
all_countries = sorted(df_raw['Geography'].unique())
selected_geography = st.sidebar.multiselect("Select Regions", options=all_countries, default=all_countries)

# Filter Logic
if not selected_geography:
    st.warning("Please select at least one region to view data analysis.")
    st.stop()
else:
    df = df_raw[df_raw['Geography'].isin(selected_geography)]

# 5. Key Performance Indicators (KPIs)
total_customers = len(df)
churn_count = df['Exited'].sum()
churn_rate = (churn_count / total_customers) * 100
baseline_diff = churn_rate - 20.37

st.subheader(f"Key Performance Indicators: {', '.join(selected_geography)}")
c1, c2, c3 = st.columns(3)
c1.metric("Churn Rate", f"{churn_rate:.2f}%", delta=f"{baseline_diff:.2f}% vs Avg", delta_color="inverse")
c2.metric("Total Customer Base", f"{total_customers:,}")
c3.metric("Total Customers Lost", f"{churn_count:,}")

st.divider()

# 6. Behavioral Analysis (Charts Row 1)
st.header("🔍 Behavioral Analysis")
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Regional Risk (Geography)")
    geo_churn = df.groupby('Geography')['Exited'].mean().sort_values(ascending=False) * 100
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=geo_churn.index, y=geo_churn.values, palette=radiant_reds, ax=ax1) 
    ax1.set_ylabel("Rate (%)")
    sns.despine()
    st.pyplot(fig1) 

with col_b:
    st.subheader("Age Group Risk")
    age_churn = df.groupby('Age_Group')['Exited'].mean() * 100
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=age_churn.index, y=age_churn.values, palette=radiant_reds, ax=ax2)
    ax2.set_ylabel("Rate (%)")
    sns.despine()
    st.pyplot(fig2)

# 7. Financial & Loyalty Analysis (Charts Row 2)
st.divider()
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Credit Score Impact")
    credit_data = df.groupby('Credit_Score_Group')['Exited'].mean() * 100
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=credit_data.index, y=credit_data.values, hue=credit_data.index, palette=radiant_reds, legend=False, ax=ax3)
    ax3.set_ylabel("Exit Rate (%)")
    sns.despine()
    st.pyplot(fig3)

with col_d:
    st.subheader("Tenure vs. Loyalty")
    tenure_data = df.groupby('Tenure')['Exited'].mean() * 100
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    # Line chart using the dark radiant red for professional consistency
    sns.lineplot(x=tenure_data.index, y=tenure_data.values, marker='o', color=dark_red, ax=ax4)
    ax4.set_ylabel("Exit Rate (%)")
    ax4.set_ylim(0, 30)
    sns.despine()
    st.pyplot(fig4)

# 8. Financial Deep Dive (Charts Row 3)
st.divider()
st.header("💰 Financial Deep Dive")
col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Churn Rate by Number of Products")
    prod_data = df.groupby('NumOfProducts')['Exited'].mean() * 100
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=prod_data.index, y=prod_data.values, palette=radiant_reds, ax=ax5) 
    ax5.set_ylabel("Exit Rate (%)")
    sns.despine()
    st.pyplot(fig5)

with col_f:
    st.subheader("Balance: Churned vs. Retained")
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    # Grey for Retained (0) and Radiant Red for Churned (1) to create focus
    sns.kdeplot(data=df, x='Balance', hue='Exited', fill=True, palette=[neutral_gray, dark_red], ax=ax6)
    sns.despine()
    st.pyplot(fig6)

st.divider()

# 9. Business Recommendations & Findings
st.header("📋 Executive Summary & Findings")
if churn_rate > 25:
    st.error(f"CRITICAL ALERT: Current churn rate ({churn_rate:.2f}%) is significantly above safety threshold.")
else:
    st.success("STABLE: Churn levels are currently within the expected historical range.")

st.info("""
**Data-Driven Insights:**
* **Regional Risk:** Germany exhibits a unique churn profile (approx. 32%) compared to France and Spain.
* **Demographic Target:** The 46–60 age group shows a consistent peak in attrition.
* **Financial Health:** Customers in the 'Low' credit score bracket show higher churn, indicating high financial sensitivity.
* **Product Saturation:** Customers with 3 or 4 products have extremely high churn rates, suggesting service complexity issues.
""")

with st.expander("View Raw Data Snippet"):
    st.dataframe(df.head(20))