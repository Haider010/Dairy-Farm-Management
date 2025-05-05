import streamlit as st
from crud import get_db_session, get_all_animals, MilkRecord, Animal
from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

def inject_dashboard_css():
    st.markdown("""
    <style>
        .dashboard-header {
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stPlotlyChart {
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def show_dashboard():
    inject_dashboard_css()
    
    # Page Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 style='color: #2c3e50; margin-bottom: 0.5rem;'>🐮 DairyFarm Analytics</h1>
        <p style='color: #7f8c8d; font-size: 1.1rem;'>Real-time Farm Performance Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

    with get_db_session() as db:
        animals = get_all_animals(db)
        milk_records = db.query(MilkRecord).all()
    
    # ========== Key Metrics ==========
    col1, col2, col3, col4 = st.columns(4)
    today = date.today()
    
    with col1:
        st.metric("🐄 Total Animals", len(animals), help="Registered animals in system")
    with col2:
        today_milk = sum(r.quantity_liters for r in milk_records if r.date == today)
        st.metric("🥛 Today's Milk", f"{today_milk} L", delta="vs yesterday")
    with col3:
        avg_milk = round(sum(r.quantity_liters for r in milk_records)/len(milk_records), 1) if milk_records else 0
        st.metric("📦 Avg Daily", f"{avg_milk} L", help="Average daily production")
    with col4:
        unique_breeds = len(set(a.breed for a in animals)) if animals else 0
        st.metric("🏷️ Unique Breeds", unique_breeds)
    
    style_metric_cards(border_left_color="#3498db", box_shadow=True)

    # ========== Main Content ==========
    tab1, tab2, tab3 = st.tabs(["📈 Production Analytics", "🐄 Animal Insights", "📁 Data Management"])

    with tab1:
        # Date Range Selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=today - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=today)

        # Production Trends
        st.subheader("Milk Production Trends", divider="blue")
        df_milk = pd.DataFrame([
            {"Date": r.date, "Liters": r.quantity_liters} 
            for r in milk_records if start_date <= r.date <= end_date
        ])
        
        if not df_milk.empty:
            fig = px.line(df_milk.groupby("Date").sum().reset_index(), 
                        x="Date", y="Liters",
                        title="Daily Milk Production",
                        height=400)
            fig.update_layout(hovermode="x unified",
                            xaxis=dict(rangeslider=dict(visible=True)))
            st.plotly_chart(fig, use_container_width=True)

            # Productivity Comparison
            st.subheader("📆 Productivity Comparison", divider="blue")
            cols = st.columns(2)
            with cols[0]:
                current_week = df_milk[df_milk["Date"] > today - timedelta(days=7)]
                last_week = df_milk[df_milk["Date"].between(today - timedelta(days=14), today - timedelta(days=7))]
                if not last_week.empty and not current_week.empty:
                    change = (current_week["Liters"].sum()/last_week["Liters"].sum() - 1) * 100
                    st.metric("Weekly Change", f"{change:.1f}%", 
                            delta_color="inverse" if change < 0 else "normal")
            
            with cols[1]:
                st.metric("Best Day", 
                        df_milk.loc[df_milk["Liters"].idxmax(), "Date"].strftime("%b %d") if not df_milk.empty else "N/A",
                        f"{df_milk['Liters'].max():.1f} L")
        else:
            st.info("No production data in selected period")

    with tab2:
        # Animal Performance
        st.subheader("Animal Performance", divider="green")
        if animals and milk_records:
            animal_df = pd.DataFrame([{
                "ID": a.id,
                "Name": a.name,
                "Breed": a.breed,
                "Age": (today - a.date_of_birth).days // 365,
                "Total Milk": sum(r.quantity_liters for r in milk_records if r.animal_id == a.id)
            } for a in animals])

            # Top Performers
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### 🏆 Top 5 Producers")
                top_5 = animal_df.sort_values("Total Milk", ascending=False).head(5)
                fig = px.bar(top_5, x="Name", y="Total Milk", color="Breed",
                            text_auto=".1f", height=300)
                st.plotly_chart(fig, use_container_width=True)

            # Breed Analysis
            with col2:
                st.markdown("##### 🧬 Breed Productivity")
                breed_stats = animal_df.groupby("Breed").agg(
                    Total_Milk=("Total Milk", "sum"),
                    Avg_Milk=("Total Milk", "mean"),
                    Count=("Breed", "count")
                ).reset_index()
                fig = px.scatter(breed_stats, x="Count", y="Avg_Milk", size="Total_Milk",
                                color="Breed", hover_name="Breed", size_max=40)
                st.plotly_chart(fig, use_container_width=True)

            # Age vs Productivity
            st.markdown("##### 📅 Age vs Milk Production")
            fig = px.scatter(animal_df, x="Age", y="Total Milk", color="Breed",
                            hover_data=["Name"], trendline="lowess")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No animal data available")

    with tab3:
        # Data Export
        st.subheader("Data Export", divider="orange")
        
        # Animal Data
        with st.expander("📦 Animal Records"):
            animal_export = pd.DataFrame([{
                "ID": a.id, 
                "Name": a.name, 
                "Breed": a.breed,
                "Date of Birth": a.date_of_birth,
                "Age": (today - a.date_of_birth).days // 365
            } for a in animals])
            
            st.dataframe(animal_export, use_container_width=True)
            st.download_button("💾 Export Animal Data", 
                             animal_export.to_csv(index=False), 
                             "animal_records.csv",
                             help="Download complete animal registry")

        # Milk Records
        with st.expander("🥛 Milk Production Data"):
            milk_export = pd.DataFrame([{
                "Animal ID": r.animal_id,
                "Animal Name": next((a.name for a in animals if a.id == r.animal_id), "Unknown"),
                "Date": r.date,
                "Liters": r.quantity_liters
            } for r in milk_records])
            
            st.dataframe(milk_export, use_container_width=True)
            st.download_button("💾 Export Milk Data", 
                             milk_export.to_csv(index=False), 
                             "milk_records.csv",
                             help="Download complete milking history")

    # ========== Footer ==========
    st.markdown("---")
    st.caption("🔔 Real-time data updated every 15 minutes | Last refresh: {}".format(pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))

if __name__ == "__main__":
    show_dashboard()