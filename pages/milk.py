import streamlit as st
from crud import get_db_session, create_milk_record, get_milk_by_animal, get_all_animal_names
from datetime import date

# Custom CSS for professional styling
def inject_css():
    st.markdown("""
    <style>
        .milk-card {
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


def show_milk():
    inject_css()
    
    # Page Title
    st.markdown('<div class="section-title">🥛 Milk Management System</div>', unsafe_allow_html=True)

    # ----- New Milk Entry -----
    with st.container():
        st.markdown('### 📥 New Milk Entry')
        st.markdown("---")
        try:
            with get_db_session() as db:
                animal_options = get_all_animal_names(db)
            
            if not animal_options:
                st.warning("No animals registered. Please add animals first.")
                return
            
            animal_dict = {name: id for id, name in animal_options}
            
            with st.form("milk_form", clear_on_submit=True):
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
                        "Date",
                        value=date.today(),
                        max_value=date.today(),
                        help="Select record date"
                    )
                qty = st.number_input(
                    "Quantity (liters)",
                    min_value=0.1,
                    max_value=1000.0,
                    step=0.1,
                    value=10.0,
                    format="%.1f",
                    help="Enter quantity in liters"
                )
                submitted = st.form_submit_button("📩 Save Milk Record", help="Submit milk record to system")

                if submitted:
                    if qty <= 0:
                        st.error("Please specify a valid quantity greater than 0.")
                        return
                    try:
                        with st.spinner("Saving milk record..."):
                            with get_db_session() as db:
                                create_milk_record(db, animal_dict[selected_animal], rec_date, qty)
                        st.success("✅ Milk record saved successfully")
                    except Exception as e:
                        st.error(f"Database error: {str(e)}")
        except Exception as e:
            st.error(f"System error: {str(e)}")

    # ----- Milk History Section -----
    st.markdown("---")
    st.markdown('### 📖 Milk History Review')
    try:
        with st.expander("Filter Milk Records", expanded=True):
            filter_cols = st.columns(3)
            with filter_cols[0]:
                selected_animal = st.selectbox(
                    "Select Animal",
                    options=list(animal_dict.keys()),
                    key="history_milk_filter"
                )
            with filter_cols[1]:
                start_date = st.date_input("Start Date", value=date.today().replace(day=1))
            with filter_cols[2]:
                end_date = st.date_input("End Date", value=date.today())
            
            if st.button("🔍 Load Milk History"):
                try:
                    with st.spinner("Fetching records..."):
                        with get_db_session() as db:
                            records = get_milk_by_animal(db, animal_dict[selected_animal])
                        filtered = [r for r in records if start_date <= r.date <= end_date]
                        
                        if filtered:
                            st.markdown('<div class="data-table">', unsafe_allow_html=True)
                            st.dataframe(
                                data=[(
                                    r.date.strftime("%Y-%m-%d"),
                                    f"{r.quantity_liters} L",
                                    selected_animal
                                ) for r in filtered],
                                column_names=["Date","Quantity","Animal"],
                                use_container_width=True,
                                height=400
                            )
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Export
                            csv_data = "Date,Quantity,Animal\n" + "\n".join([
                                f"{r.date},{r.quantity_liters},{selected_animal}" for r in filtered
                            ])
                            st.download_button(
                                label="📥 Export as CSV",
                                data=csv_data,
                                file_name=f"milk_history_{selected_animal}.csv",
                                mime="text/csv"
                            )
                        else:
                            st.info("No records found for selected period")
                except Exception as e:
                    st.error(f"Error loading history: {str(e)}")
    except Exception as e:
        st.error(f"Filter error: {str(e)}")

if __name__ == "__main__":
    show_milk()