import streamlit as st
from crud import get_db_session, create_feed_record, get_feed_by_animal, get_all_animal_names
from datetime import date

# Custom CSS for professional styling
def inject_css():
    st.markdown("""
    <style>
        .feed-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            background: white;
        }
        .section-title {
            color: #2c3e50;
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
        }
        .form-header {
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .stNumberInput, .stTextInput, .stDateInput {
            margin-bottom: 1.2rem;
        }
        .data-table {
            margin-top: 2rem;
            padding: 1rem;
            border-radius: 8px;
            background: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True)

def show_feed():
    inject_css()
    
    # Header Section
    # st.markdown('<div class="section-title">Feed Management System</div>', unsafe_allow_html=True)
    
    # Add Feed Entry Section
    with st.container():
        st.markdown('### 📥 New Feed Entry')
        st.markdown("---")
        
        try:
            with get_db_session() as db:
                animal_options = get_all_animal_names(db)
                
            if not animal_options:
                st.warning("No animals registered. Please add animals first.")
                return
                
            animal_dict = {name: id for id, name in animal_options}
            
            with st.form("feed_form", clear_on_submit=True):
                cols = st.columns(2)
                with cols[0]:
                    selected_animal = st.selectbox(
                        "Select Animal",
                        options=list(animal_dict.keys()),
                        index=0,
                        help="Choose animal from registered list"
                    )
                with cols[1]:
                    rec_date = st.date_input(
                        "Feeding Date",
                        value=date.today(),
                        max_value=date.today(),
                        help="Select feeding date"
                    )
                
                feed_type = st.text_input(
                    "Feed Type",
                    placeholder="Enter feed type (e.g., Alfalfa Hay, Corn Silage)",
                    help="Specify the type of feed given"
                )
                
                qty = st.number_input(
                    "Quantity (kg)",
                    min_value=0.1,
                    max_value=1000.0,
                    step=0.1,
                    value=5.0,
                    format="%.1f",
                    help="Enter quantity in kilograms"
                )
                
                submitted = st.form_submit_button("📩 Save Feed Record", 
                    help="Submit feeding details to system")
                
                if submitted:
                    if not feed_type.strip():
                        st.error("Please specify a valid feed type")
                        return
                        
                    try:
                        with st.spinner("Saving feed record..."):
                            with get_db_session() as db:
                                create_feed_record(db, animal_dict[selected_animal], rec_date, feed_type, qty)
                        st.success("✅ Feed record saved successfully")
                    except Exception as e:
                        st.error(f"Database error: {str(e)}")
        
        except Exception as e:
            st.error(f"System error: {str(e)}")
    
    # Feed History Section
    st.markdown("---")
    st.markdown('### 📖 Feed History Review')
    
    try:
        with st.expander("Filter Feed Records", expanded=True):
            filter_cols = st.columns(3)
            with filter_cols[0]:
                selected_animal = st.selectbox(
                    "Select Animal",
                    options=list(animal_dict.keys()),
                    key="history_filter"
                )
            with filter_cols[1]:
                start_date = st.date_input("Start Date", value=date.today().replace(day=1))
            with filter_cols[2]:
                end_date = st.date_input("End Date", value=date.today())
                
            if st.button("🔍 Load Feed History"):
                try:
                    with st.spinner("Fetching records..."):
                        with get_db_session() as db:
                            records = get_feed_by_animal(db, animal_dict[selected_animal])
                        
                        if records:
                            filtered = [
                                r for r in records
                                if start_date <= r.date <= end_date
                            ]
                            
                            if filtered:
                                with st.container():
                                    st.markdown('<div class="data-table">', unsafe_allow_html=True)
                                    st.dataframe(
                                        data=[(
                                            r.date.strftime("%Y-%m-%d"),
                                            r.feed_type,
                                            f"{r.quantity_kg} kg",
                                            selected_animal
                                        ) for r in filtered],
                                        column_names=["Date", "Feed Type", "Quantity", "Animal"],
                                        use_container_width=True,
                                        height=400
                                    )
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Export option
                                    st.download_button(
                                        label="📥 Export as CSV",
                                        data="\n".join([",".join(map(str, row)) for row in [
                                            ["Date", "Feed Type", "Quantity", "Animal"]
                                        ] + [
                                            [r.date, r.feed_type, r.quantity_kg, selected_animal] 
                                            for r in filtered
                                        ]]),
                                        file_name=f"feed_history_{selected_animal}.csv",
                                        mime="text/csv"
                                    )
                            else:
                                st.info("No records found for selected period")
                        else:
                            st.info("No feed records available")
                except Exception as e:
                    st.error(f"Error loading history: {str(e)}")
                    
    except Exception as e:
        st.error(f"Filter error: {str(e)}")

if __name__ == "__main__":
    show_feed()