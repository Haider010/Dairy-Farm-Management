import streamlit as st
from crud import get_db_session, create_animal, get_all_animals, delete_animal
from datetime import date

def show_animals():
    st.markdown("## 🐄 Animal Management", unsafe_allow_html=True)
    st.markdown("---")

    with st.expander("➕ Add New Animal", expanded=False):
        with st.form("add_animal_form"):
            name = st.text_input("🐾 Animal Name", placeholder="e.g. Daisy")
            breed = st.text_input("📜 Breed", placeholder="e.g. Holstein Friesian")
            dob = st.date_input("📅 Date of Birth", value=date.today())
            notes = st.text_area("📝 Notes (optional)", placeholder="Enter any special notes")

            submitted = st.form_submit_button("✅ Add Animal")

            if submitted:
                if not name or not breed:
                    st.warning("Please fill out both Name and Breed fields.")
                else:
                    try:
                        with get_db_session() as db:
                            animal = create_animal(db, name, breed, dob, notes)
                            st.success(f"✅ Successfully added animal **{animal.name}** (ID: {animal.id})")
                    except Exception as e:
                        st.error(f"🚨 Failed to add animal. Error: {e}")

    st.markdown("### 📋 Existing Animals")
    st.markdown("View or delete registered animals below:")
    st.write("")

    with get_db_session() as db:
        try:
            animals = get_all_animals(db)
            if not animals:
                st.info("No animals found in the database.")
                return

            for a in animals:
                with st.container():
                    cols = st.columns([1, 3, 3, 2])
                    cols[0].markdown(f"**#{a.id}**")
                    cols[1].markdown(f"**Name:** {a.name}")
                    cols[2].markdown(f"**Breed:** {a.breed}")
                    if cols[3].button("🗑️ Delete", key=f"del_{a.id}"):
                        try:
                            delete_animal(db, a.id)
                            st.success(f"Deleted animal #{a.id}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting animal: {e}")
        except Exception as e:
            st.error(f"❌ Failed to load animals: {e}")
