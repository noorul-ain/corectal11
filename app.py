# File: lower_gi_triage_streamlit.py

import streamlit as st

def main():
    st.title("Lower GI 2WW Triage Pathway")
    triage_logic()

def triage_logic():
    symptoms = st.multiselect(
        "Which of the following symptom(s) does the patient have?",
        options=[
            "1. Abdominal mass",
            "2. Change of bowel habit",
            "3. Unexplained weight loss",
            "4. Unexplained rectal bleeding",
            "5. Unexplained abdominal pain",
            "6. Iron-deficiency anaemia (IDA)",
            "7. Anaemia (not IDA)",
            "8. Incidental finding",
            "9. Rectal mass (FIT not required)",
            "10. Unexplained anal mass (FIT not required)",
            "11. Unexplained anal ulceration (FIT not required)"
        ],
        help="Select all symptoms that apply."
    )
    symptom_indices = {int(symptom.split(".")[0]) for symptom in symptoms}

    if {9, 10, 11} & symptom_indices:
        q2a_rectal_anal_mass_pathway()
        return

    if 1 in symptom_indices:
        st.write("Abdominal mass noted. Ensure CT at PTL if no index CT.")

    if 6 in symptom_indices:
        st.write("IDA noted. Ensure OGD at PTL once colonic investigation is complete or if clinically indicated.")

    q2_fitness_check(symptom_indices)

def q2_fitness_check(symptoms):
    fit_done = st.radio("Has a FIT test been performed and is there a ferritin level?", ("yes", "no"))

    if fit_done == 'no':
        if {9, 10, 11} & symptoms:
            q2a_rectal_anal_mass_pathway()
        else:
            q2b_fit_below_10()
    elif fit_done == 'yes':
        fit_value = st.number_input("Enter FIT result:", min_value=0, step=1)
        if fit_value >= 10:
            q3_fit_high_pathway(fit_value)
        else:
            q2b_fit_below_10()

def q2a_rectal_anal_mass_pathway():
    st.write("Special Pathway: Rectal/Anal Mass or Ulceration")
    fos_suitable = st.radio("Is the patient suitable for urgent Flexible Sigmoidoscopy (FOS)?", ("yes", "no"))
    if fos_suitable == 'yes':
        st.write("Perform urgent FOS. After FOS, refer back to Primary Care if NAD.")
    else:
        st.write("Arrange Clinical Endoscopist Telephone Triage or urgent CR OPA if indicated.")

def q2b_fit_below_10():
    st.write("FIT <10 or missing ferritin pathway.")
    return_to_referrer = st.radio("Do you want to return to referrer?", ("yes", "no"))
    if return_to_referrer == 'yes':
        st.write("Send template letter to Primary Care to repeat FIT test or consider NSS pathway.")
    else:
        st.write("Follow local exceptions or pathway guidelines.")

def q3_fit_high_pathway(fit_value):
    st.write(f"FIT result is {fit_value}. Proceeding with high FIT pathway.")
    high_risk = st.radio(
        "Does the patient have WHO performance status 3/4, significant comorbidities/dementia, or are they >=80 years old?",
        ("yes", "no")
    )
    if high_risk == 'yes':
        q3a_telephone_triage()
    else:
        q4_fit_value_branching(fit_value)

def q3a_telephone_triage():
    st.write("High-risk group: Telephone triage.")
    suitable_for_endoscopy = st.radio("Is the patient suitable for endoscopy?", ("yes", "no"))
    if suitable_for_endoscopy == 'yes':
        st.write("Follow endoscopic algorithm as in Q4/Q5.")
    else:
        st.write("Consider CTC or CTAP based on patient suitability. Arrange urgent CR OPA if not suitable for imaging.")

def q4_fit_value_branching(fit_value):
    if fit_value >= 100:
        q5_high_fit_pathway()
    elif 10 <= fit_value <= 99:
        q4a_age_symptom_triad()

def q4a_age_symptom_triad():
    age = st.number_input("Enter patient's age:", min_value=0, step=1)
    rectal_bleeding = st.radio("Does the patient have rectal bleeding?", ("yes", "no")) == 'yes'

    if age < 40 and not rectal_bleeding:
        st.write("Offer Colon Capsule (max 7/week). If capacity reached or patient declines, proceed to Colonoscopy.")
    elif 40 <= age <= 59 and rectal_bleeding:
        st.write("Book Colonoscopy.")
    elif age >= 60 and rectal_bleeding:
        st.write("CTC or Colonoscopy based on clinical judgment.")
    elif age >= 60 and not rectal_bleeding:
        st.write("Colonoscopy preferred. If not suitable, consider CTC.")
    else:
        st.write("Check local guidelines for alternative pathways.")

def q5_high_fit_pathway():
    st.write("FIT >=100: Recommended primary investigation is Colonoscopy.")
    colonoscopy_suitable = st.radio("Is the patient suitable for Colonoscopy?", ("yes", "no"))
    if colonoscopy_suitable == 'yes':
        st.write("Book Colonoscopy.")
    else:
        st.write("Consider CTC or alternative imaging.")

if __name__ == "__main__":
    main()
