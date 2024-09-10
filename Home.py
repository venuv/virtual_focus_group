import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import demographics_dict as dd
import json
import os

st.set_page_config(page_title="Virtual Focus Group", page_icon=":tada:", layout="wide")
with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 2px solid rgba(49, 51, 63, 0.2);
                background-color: lightteal;
                border-radius: 25px;
                padding: calc(1em - 1px);
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                text-align: center;
            }
            """,
    ):
    st.markdown("<h1 style='text-align: center; color: black;'>Build Your Personas</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: grey;'>Select the number of Personas to create, add details, then click Submit Personas.<br><br></h4>", unsafe_allow_html=True)

# Load personas from file
def load_personas():
    if os.path.exists('docs/personas.json'):
        with open('docs/personas.json', 'r') as file:
            personas = json.load(file)
            return personas
    return {}

# Save personas to file
def save_personas(personas):
    with open('docs/personas.json', 'w') as file:
        json.dump(personas, file, indent=4)

# Main program logic
def main():
    personas = load_personas()
    if personas:
        st.markdown("<h4 style='text-align: center; color: grey;'>Previously saved personas detected. Do you want to load them or create new ones?<br><br></h4>", unsafe_allow_html=True)
        load_existing = st.radio("Load previous personas or create new?", ("Load Personas", "Create New Personas"))
    else:
        load_existing = "Create New Personas"

    # If loading existing personas
    if load_existing == "Load Personas":
        st.markdown("<h4 style='text-align: center; color: grey;'>Loaded Personas:<br><br></h4>", unsafe_allow_html=True)
        for persona_name, persona_data in personas.items():
            st.subheader(persona_name)
            for key, value in persona_data.items():
                st.text(f"{key}: {value}")
        return

    # If creating new personas
    col1, col2, col3, col4 = st.columns([.5, 1, .5, .5])
    with col1:
        num_personas = st.slider("Number of Personas to Create: ", min_value=1, max_value=5, step=1, value=1)
    with col2:
        st.empty()

    # Prepare to create new personas
    new_personas = {}
    columns = st.columns(num_personas)

    for persona_id in range(num_personas):
        with columns[persona_id]:
            st.subheader(f"Persona {persona_id + 1}")
            
            # Create input fields for each demographic attribute
            name = st.text_input(f"Name (Persona {persona_id + 1})", key=f"name_{persona_id}")
            age = st.selectbox(f"Age (Persona {persona_id + 1})", dd.age_groups, key=f"age_{persona_id}")
            gender = st.selectbox(f"Gender (Persona {persona_id + 1})", dd.gender_groups, key=f"gender_{persona_id}")
            location = st.selectbox(f"Geographic Location (Persona {persona_id + 1})", dd.geographic_location, key=f"location_{persona_id}")
            education = st.selectbox(f"Education Level (Persona {persona_id + 1})", dd.education_levels, key=f"education_{persona_id}")
            employment = st.selectbox(f"Employment Status (Persona {persona_id + 1})", dd.employment_status, key=f"employment_{persona_id}")
            income = st.selectbox(f"Income Level (Persona {persona_id + 1})", dd.income_levels, key=f"income_{persona_id}")
            marital = st.selectbox(f"Marital Status (Persona {persona_id + 1})", dd.marital_status, key=f"marital_{persona_id}")
            children = st.selectbox(f"Number of Children (Persona {persona_id + 1})", dd.number_of_children, key=f"children_{persona_id}")
            job = st.selectbox(f"Occupation (Persona {persona_id + 1})", dd.occupation, key=f"job_{persona_id}")
            hobby = st.multiselect(f"Hobbies (Persona {persona_id + 1})", dd.hobbies, key=f"hobby_{persona_id}")
            backstory = st.text_area(f"Key Traits and Miscellaneous Data:  (Persona {persona_id + 1})", key=f"backstory_{persona_id}")
            
            # Create a dictionary to represent the persona
            persona = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Location": location,
                "Education": education,
                "Employment": employment,
                "Income": income,
                "Marital Status": marital,
                "Children": children,
                "Occupation": job,
                "Hobbies": hobby,
                "Backstory": backstory
            }
            
            new_personas[f"Persona {persona_id + 1}"] = persona

    with col3:
        if st.button("Submit Personas"):
            personas.update(new_personas)
            save_personas(personas)
            st.success("Personas saved successfully!")

    with col4:
        if st.button("Launch Focus Group"):
            st.switch_page("pages/1 Run_Virtual_Focus_Group.py")

if __name__ == "__main__":
    main()
