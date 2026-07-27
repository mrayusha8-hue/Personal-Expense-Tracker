# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page configuration
st.set_page_config(
    page_title = "Personal_Expense_Tracker",
    layout = "wide"
)

# Dashboard Title
st.title("💰 Personal Expense Tracker")

# Project Overview
st.divider()
st.subheader("Project Overview")
st.markdown("This dashboard helps analyze expenses through interactive visualizations.")
st.divider()

# Load Data
df = pd.read_csv("cleaned_expense.csv")
#Creating month column
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month_name()

#Add sidebar
st.sidebar.title("Filters")

#Create category,month column
categories = sorted(df["Category"].unique())
months = sorted(df["Month"].unique())

#Create selectbox
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)
selected_month = st.sidebar.selectbox("Select Month", ["All"] + months)

#Apply filters
filtered_df = df.copy()  #.copy()=> we never modify original dataframe

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == selected_month]

# Dashboard Summary
st.header("📊  Dashboard Summary")

# Calculate KPI values
total_expense = filtered_df["Amount"].sum()
average_expense = filtered_df["Amount"].mean()
highest_expense = filtered_df["Amount"].max()
lowest_expense = filtered_df["Amount"].min()
total_transactions = filtered_df.shape[0]  #len(df) can be used

# Create 4 columns
col1, col2, col3, col4, col5 = st.columns(5)
    
# Adding KPI card within respective column
with col1:
    st.metric(
        label = "💰 Total Expense",
        value = f" ₹{total_expense:,.2f}"
    )
    
    
with col2:
    st.metric(
        label = "📊 Average Expense",
        value = f" ₹{average_expense:,.2f}"
    )

with col3:
    st.metric(
        label = "💸 Highest Expense",
        value = f" ₹{highest_expense:,.2f}"
    )

with col4:
    st.metric(
        label = "📉 Lowest Expense",
        value = f" ₹{lowest_expense:,.2f}"
)
    
with col5:
    st.metric(
        label = "🧾 Total Transactions",
        value = total_transactions,
        delta = "Total records"
)
st.divider()

# Side-by-side comparison section
st.header("📊 Expense Comparison")

if not filtered_df.empty:
    # Monthly Expense
    monthly_expense = filtered_df.groupby("Month")["Amount"].sum()
    fig1, ax1 = plt.subplots(figsize=(7,5))
    ax1.bar(monthly_expense.index, monthly_expense.values, color="steelblue")
    ax1.set_title("Monthly Expenses")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Amount (₹)")
    plt.xticks(rotation=45)
    ax1.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Category-wise Expense
    category_expense = filtered_df.groupby("Category")["Amount"].sum()
    fig2, ax2 = plt.subplots(figsize=(7,5))
    ax2.bar(category_expense.index, category_expense.values, color="seagreen")
    ax2.set_title("Category-wise Expenses")
    ax2.set_xlabel("Category")
    ax2.set_ylabel("Amount (₹)")
    ax2.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display both charts side by side
    colA, colB = st.columns(2)
    with colA:
        st.pyplot(fig1)
    with colB:
        st.pyplot(fig2)

else:
    st.warning("No data available.")


# Pie Chart Section

st.header("🥧 Expense Distribution")
if not filtered_df.empty:
    # Create pie chart
    #Group by category and calculate total expense
    category_wise_expense = filtered_df.groupby("Category")["Amount"].sum()

    # Create the plot
    fig, ax = plt.subplots(figsize=(4,3))
    ax.pie( category_wise_expense, labels=category_wise_expense.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize':4})
    plt.tight_layout()
   
    ax.set_title("Percentage of Spending Category", fontsize=6)
    #Show plot
    st.pyplot(fig)
else:
    st.warning("No data available.")

 
#Key insights 
st.subheader("💡 Smart Insights")
if filtered_df.empty:
    st.warning("No data available for the selected filters")
else:
   # Spending level
   total_expense = filtered_df["Amount"].sum()
   if total_expense > 10000:
        st.warning(f"⚠️ Total spending is ₹{total_expense:,.2f}. Your expenses are relatively high for the selected filters.")
   elif total_expense > 5000:
        st.info(f"ℹ️ Total spending is ₹{total_expense:,.2f}. Spending is within a moderate range.")
   else:
     st.success( f"✅ Total spending is ₹{total_expense:,.2f}. Spending is relatively low.")
   #Category dominance
   total_expense = filtered_df["Amount"].sum()
   if total_expense > 10000:
    st.warning( f"⚠️ Total spending is ₹{total_expense:,.2f}. Your expenses are relatively high for the selected filters.")
   elif total_expense > 5000:
    st.info(f"ℹ️ Total spending is ₹{total_expense:,.2f}. Spending is within a moderate range.")
   else:
    st.success( f"✅ Total spending is ₹{total_expense:,.2f}. Spending is relatively low.")
   #Average Transaction Analysis
   average_expense = filtered_df["Amount"].mean()
   if average_expense > 1000:
    st.warning(f"⚠️ Average transaction amount is ₹{average_expense:,.2f}. You tend to make large purchases.")
   else:
    st.success( f"✅ Average transaction amount is ₹{average_expense:,.2f}. Spending per transaction is moderate.")

st.divider()

# Footer

st.caption("Personal Expense Tracker | Built using Python, Pandas and Streamlit")
st.divider()


