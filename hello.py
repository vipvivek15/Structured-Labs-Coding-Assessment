from preswald import connect, get_df, query, slider, table, text, plotly, sidebar
import plotly.express as px
import pandas as pd

# === Connect and Load Dataset ===
text("## 🔌Connecting to Dataset...")
try:
    connect()
    df = get_df("health_activity_data")
    df.columns = df.columns.str.strip()
    text(f"✅ Dataset loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
    table(df.head(), title="📂 First 5 Rows of Dataset")
except Exception as e:
    text(f"❌ Failed to load dataset: {e}")



# === Welcome Screen ===
text("# 👋 Welcome to the Health Activity Dashboard")
text("""
This dashboard provides insights into user fitness behavior:
- 🏃 Filter records based on daily steps
- 🔥 Discover high calorie consumption days
- 📊 Visualize trends in user lifestyle data
""")

# === Derived Columns ===
text("## 🧮 Adding Activity Level Classification")
try:
    df["ActivityLevel"] = pd.cut(
        df["Daily_Steps"],
        bins=[0, 5000, 10000, 20000],
        labels=["Low", "Moderate", "High"]
    )
    text("✅ 'ActivityLevel' column created successfully.")
    text("### 🔍 Activity Level Definitions")
    text("""
    - 🟢 **Low**: 0 to 5,000 steps  
    - 🟡 **Moderate**: 5,001 to 10,000 steps  
    - 🔴 **High**: 10,001 to 20,000 steps  
    """)
    activity_counts = df["ActivityLevel"].value_counts().sort_index()
    activity_table = activity_counts.reset_index()
    activity_table.columns = ["Activity Level", "User Count"]
    table(activity_table, title="📊 Users by Activity Level")


except Exception as e:
    text(f"❌ Failed to create ActivityLevel column: {e}")

# === Interactive Filter ===
text("## 🎚️ Creating Step Threshold Slider")
try:
    threshold = slider("Minimum Daily Steps", min_val=0, max_val=20000, default=10000)
    filtered_df = df[df["Daily_Steps"] > threshold]
    table(filtered_df, title=f"📊 Records with Steps > {threshold}")
except Exception as e:
    text(f"❌ Slider/filter failed: {e}")

# === SQL Query for High Calorie ===
text("## 📈 High Calorie Intake Query")
try:
    sql = "SELECT * FROM health_activity_data WHERE Calories_Intake > 2500"
    high_cal_df = query(sql, "health_activity_data")
    table(high_cal_df, title="🔥 High Calorie Days (> 2500)")
except Exception as e:
    text(f"❌ SQL query failed: {e}")

# === Scatter Plot ===
text("## 🟢 Scatter Plot")
try:
    fig1 = px.scatter(
        df,
        x="Daily_Steps",
        y="Calories_Intake",
        color="ActivityLevel",
        title="🏃‍♂️ Daily Steps vs Calories Intake"
    )
    plotly(fig1)
except Exception as e:
    text(f"❌ Scatter plot failed: {e}")

# === Pie Chart ===
text("## 🥧 Pie Chart for Activity Levels")
try:
    fig2 = px.pie(
        df,
        names="ActivityLevel",
        title="🧩 Activity Level Distribution",
        hole=0.4
    )
    plotly(fig2)
except Exception as e:
    text(f"❌ Pie chart failed: {e}")

# === Bar Chart ===
text("## 📊 Bar Chart - Avg Calories by Activity Level")
try:
    avg_calories = df.groupby("ActivityLevel")["Calories_Intake"].mean().reset_index()
    fig3 = px.bar(
        avg_calories,
        x="ActivityLevel",
        y="Calories_Intake",
        title="🍽️ Avg Calories Intake by Activity Level"
    )
    plotly(fig3)
except Exception as e:
    text(f"❌ Bar chart failed: {e}")



