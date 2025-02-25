import streamlit as st
import pandas as pd

# Apply custom CSS to enhance visibility
st.markdown(
    """
    <style>
        body, .stApp {
            color: white !important;
            background-color: black !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p {
            color: #FFFFFF !important;
            font-weight: bold;
        }
        .stTextInput label, .stNumberInput label, .stRadio label, .stSelectbox label, .stFileUploader label {
            color: #FFFFFF !important;
            font-weight: bold;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

def calculate_tax_new(income):
    slabs = [(400000, 0.00), (800000, 0.05), (1200000, 0.10), (1600000, 0.15), (2000000, 0.20), (2400000, 0.25), (float('inf'), 0.30)]
    tax, previous_limit = 0, 0
    for limit, rate in slabs:
        if income > limit:
            tax += (limit - previous_limit) * rate
        else:
            tax += (income - previous_limit) * rate
            break
        previous_limit = limit
    return tax

def calculate_tax_old(income, deductions):
    taxable_income = max(0, income - deductions)
    return calculate_tax_new(taxable_income)

def show_tax_app():
    st.markdown("<h1>Tax Filing Document Checklist and Tax Calculator</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <h2>Mandatory Documents</h2>
    ✅ PAN Card<br>
    ✅ Aadhaar Card (linked to PAN)<br>
    ✅ Bank Account Details (Account Number, IFSC)<br>
    ✅ Form 16 (For Salaried Employees)<br>
    ✅ Form 26AS (Annual Tax Statement)<br>
    
    <h2>Additional Documents (if applicable)</h2>
    - Salary Slips, Rental Income Proofs, Freelance Income Invoices<br>
    - Home Loan Interest Certificate (Section 24b deduction)<br>
    - PPF, EPF, ELSS, Tax-Saving FDs (Section 80C proof)<br>
    - NPS Contribution Proof (Section 80CCD(1B))<br>
    - Charity Donations Receipts (Section 80G)<br>
    
    <b>Note:</b> Ensure secure storage if uploading documents online.
    """, unsafe_allow_html=True)
    
    st.markdown("<h2>AI-Powered Deduction Suggestions</h2>", unsafe_allow_html=True)
    
    employment_type = st.selectbox("Select Employment Type", ["Salaried", "Self-Employed/Freelancer"], key="employment_type")
    
    rent_paid = 0
    if employment_type == "Salaried":
        rent_paid = st.number_input("Enter House Rent Paid (for HRA under Old Regime)", min_value=0, step=1000, key="rent_paid")
    
    dependents = st.number_input("Number of Dependents (for Medical Insurance under Section 80D)", min_value=0, step=1, key="dependents")
    
    home_loan_interest = st.number_input("Home Loan Interest Paid (Section 24b)", min_value=0, step=1000, key="home_loan_interest")
    
    ppf_epf_elss = st.number_input("Investments in PPF, EPF, ELSS, Tax-Saving FDs (Section 80C)", min_value=0, step=1000, key="ppf_epf_elss")
    
    nps_contribution = st.number_input("NPS Contribution (Section 80CCD(1B))", min_value=0, step=1000, key="nps_contribution")
    
    education_loan_interest = st.number_input("Education Loan Interest Paid (Section 80E)", min_value=0, step=1000, key="education_loan_interest")
    
    donations = st.number_input("Donations to Charity (Section 80G)", min_value=0, step=1000, key="donations")
    
    st.markdown("<h2>Upload Expenditure Sheet</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key="uploaded_file")
    total_deductions = 0
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name=None)
        st.write("File uploaded successfully!")
        for sheet_name, data in df.items():
            st.markdown(f"<h3>{sheet_name}</h3>", unsafe_allow_html=True)
            st.write(data.head())
            if sheet_name in ['Food', 'Travel', 'Telephone', 'Books and Periodicals']:
                data.iloc[:, 1] = pd.to_numeric(data.iloc[:, 1], errors='coerce').fillna(0)
                total_deductions += data.iloc[:, 1].sum()
        st.markdown(f"<h2>Total Deductions from Expenditure Sheet: ₹{total_deductions:,.2f}</h2>", unsafe_allow_html=True)
    
    st.markdown("<h2>Income Tax Calculator</h2>", unsafe_allow_html=True)
    income = st.number_input("Enter your annual income (in INR):", min_value=0, step=10000, key="income")
    tax_regime = st.radio("Select Tax Regime:", ("New Tax Regime", "Old Tax Regime"), key="tax_regime")
    
    deductions = total_deductions
    if st.button("Calculate Tax"):
        tax_amount = calculate_tax_new(income) if tax_regime == "New Tax Regime" else calculate_tax_old(income, deductions)
        st.markdown(f"<h2>Your calculated tax is: ₹{tax_amount:,.2f}</h2>", unsafe_allow_html=True)

# Run the app
show_tax_app()
