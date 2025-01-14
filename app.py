import streamlit as st

###############################################################################
# 1) CATEGORY DEFINITIONS
###############################################################################
CATEGORY_DEFINITIONS = {
    1: "Category 1: A condition for which there is no restriction for the use of the method",
    2: "Category 2: A condition where the advantages generally outweigh the theoretical or proven risks",
    3: "Category 3: A condition where the theoretical or proven risks usually outweigh the advantages. Use of the method requires expert clinical judgement.",
    4: "Category 4: A condition which represents an unacceptable health risk if the method is used"
}

METHODS = ["Cu-IUD", "LNG-IUS", "IMP", "DMPA", "POP", "CHC"]

###############################################################################
# 2) THE MASTER UKMEC TABLE
###############################################################################
UKMEC_DATA = {
    "AGE_MENARCHE_LT_20": {"Cu-IUD": 2, "LNG-IUS": 2, "IMP": 1, "DMPA": 2, "POP": 1, "CHC": 1},
    "AGE_GE_20": {"Cu-IUD": 1, "LNG-IUS": 1, "IMP": 1, "DMPA": 1, "POP": 1, "CHC": 1},
    "SMOKE_LT_35": {"Cu-IUD": 1, "LNG-IUS": 1, "IMP": 1, "DMPA": 1, "POP": 1, "CHC": 2},
    "BMI_30_34": {"Cu-IUD": 1, "LNG-IUS": 1, "IMP": 1, "DMPA": 1, "POP": 1, "CHC": 2},
    "BMI_GE_35": {"Cu-IUD": 1, "LNG-IUS": 1, "IMP": 1, "DMPA": 1, "POP": 1, "CHC": 3},
    "BREASTFEEDING_0_TO_6_WEEKS": {"Cu-IUD": 1, "LNG-IUS": 1, "IMP": 2, "DMPA": 1, "POP": 4, "CHC": 4},
    # Add additional conditions as needed...
}

###############################################################################
# 3) COMBINING MULTIPLE CONDITIONS
###############################################################################
def combine_categories(condition_keys):
    """
    Combines condition keys into a final set of categories for each method.
    """
    final_cat = {method: 1 for method in METHODS}  # Start at Category 1 for all methods

    for key in condition_keys:
        if key in UKMEC_DATA:
            for method, category in UKMEC_DATA[key].items():
                if category is not None:
                    final_cat[method] = max(final_cat[method], category)

    return final_cat

###############################################################################
# 4) STREAMLIT APP
###############################################################################
def main():
    st.title("Full UKMEC Contraceptive Eligibility Checker (Comprehensive)")

    st.write("""
    This tool calculates UKMEC contraceptive eligibility categories based on the conditions you select.  
    Use this tool as a guide alongside clinical judgment and official guidance.
    """)

    # Initialize condition keys
    condition_keys = []

    st.header("Step 1: Basic Demographics")
    # Age
    age = st.number_input("Age (years)", 10, 60, 25)
    if age < 20:
        condition_keys.append("AGE_MENARCHE_LT_20")
    else:
        condition_keys.append("AGE_GE_20")

    # Smoking
    smokes = st.checkbox("Smoking?")
    if smokes:
        condition_keys.append("SMOKE_LT_35")

    # BMI
    bmi = st.number_input("BMI", 10.0, 70.0, 25.0)
    if 30 <= bmi < 35:
        condition_keys.append("BMI_30_34")
    elif bmi >= 35:
        condition_keys.append("BMI_GE_35")

    st.header("Step 2: Additional Conditions")
    # Breastfeeding
    breastfeeding = st.checkbox("Is the patient breastfeeding?")
    if breastfeeding:
        weeks = st.number_input("Weeks postpartum (0-26)", 0, 26, 0)
        if weeks < 6:
            condition_keys.append("BREASTFEEDING_0_TO_6_WEEKS")

    # Display selected conditions
    st.header("Selected Condition Keys:")
    st.write(condition_keys)

    # Combine categories and calculate results
    final_categories = combine_categories(condition_keys)

    st.header("RESULT: UKMEC Category for Each Method")
    for method in METHODS:
        category = final_categories[method]
        st.write(f"**{method}**: {CATEGORY_DEFINITIONS[category]}")

if __name__ == "__main__":
    main()
