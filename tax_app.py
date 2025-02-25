import streamlit as st
import pandas as pd

def show_tax_app():
    st.title("Tax Filing Document Checklist and Tax Calculator")
    
    st.markdown("""
    ## Mandatory Documents
    ✅ PAN Card
    ✅ Aadhaar Card (linked to PAN)
    ✅ Bank Account Details (Account Number, IFSC)
    ✅ Form 16 (For Salaried Employees)
    ✅ Form 26AS (Annual Tax Statement)
    
    ## Additional Documents (if applicable)
    - Salary Slips, Rental Income Proofs, Freelance Income Invoices
    - Home Loan Interest Certificate (Section 24b deduction)
    - PPF, EPF, ELSS, Tax-Saving FDs (Section 80C proof)
    - NPS Contribution Proof (Section 80CCD(1B))
    - Charity Donations Receipts (Section 80G)
    
    **Note:** Ensure secure storage if uploading documents online.
    """)
    
    st.subheader("AI-Powered Deduction Suggestions")
    employment_type = st.selectbox("Select Employment Type", ["Salaried", "Self-Employed/Freelancer"])
    
    rent_paid = 0
    if employment_type == "Salaried":
        rent_paid = st.number_input("Enter House Rent Paid (for HRA under Old Regime)", min_value=0, step=1000)
    
    dependents = st.number_input("Number of Dependents (for Medical Insurance under Section 80D)", min_value=0, step=1)
    
    home_loan_interest = st.number_input("Home Loan Interest Paid (Section 24b)", min_value=0, step=1000)
    
    ppf_epf_elss = st.number_input("Investments in PPF, EPF, ELSS, Tax-Saving FDs (Section 80C)", min_value=0, step=1000)
    
    nps_contribution = st.number_input("NPS Contribution (Section 80CCD(1B))", min_value=0, step=1000)
    
    education_loan_interest = st.number_input("Education Loan Interest Paid (Section 80E)", min_value=0, step=1000)
    
    donations = st.number_input("Donations to Charity (Section 80G)", min_value=0, step=1000)
    
    if st.button("Get AI Recommendations"):
        st.subheader("Eligible Deductions Based on Your Inputs")
        if rent_paid > 0:
            st.write("🏠 You can claim **HRA deduction** under the Old Regime.")
        if dependents > 0:
            st.write("🩺 You can claim **Medical Insurance deductions (Section 80D)**.")
        if home_loan_interest > 0:
            st.write("🏡 You can claim **Home Loan Interest deduction (Section 24b)**.")
        if ppf_epf_elss > 0:
            st.write("📈 You can claim **Investments under Section 80C** (up to ₹1.5L).")
        if nps_contribution > 0:
            st.write("💰 You can claim **NPS contributions under Section 80CCD(1B)** (up to ₹50k).")
        if education_loan_interest > 0:
            st.write("🎓 You can claim **Education Loan Interest deduction (Section 80E)**.")
        if donations > 0:
            st.write("🙏 You can claim **Donations under Section 80G**.")
        
        if all(x == 0 for x in [rent_paid, dependents, home_loan_interest, ppf_epf_elss, nps_contribution, education_loan_interest, donations]):
            st.write("❌ No eligible deductions found. Consider tax-saving investments!")
        
        # Store values in session state
        st.session_state['home_loan_interest'] = home_loan_interest
        st.session_state['ppf_epf_elss'] = ppf_epf_elss
        st.session_state['nps_contribution'] = nps_contribution
        st.session_state['medical_insurance'] = dependents * 25000  # Assuming 25000 per dependent
        st.session_state['education_loan_interest'] = education_loan_interest
        st.session_state['donations'] = donations
        st.session_state['rent_paid'] = rent_paid
        st.session_state['dependents'] = dependents

    st.subheader("Income Tax Calculator")
    income = st.number_input("Enter your annual income (in INR):", min_value=0, step=10000)
    tax_regime = st.radio("Select Tax Regime:", ("New Tax Regime", "Old Tax Regime"))
    
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
    
    deductions = 0
    if tax_regime == "Old Tax Regime":
        st.subheader("Enter Deduction Details")
        home_loan_interest = st.session_state.get('home_loan_interest', 0)
        ppf_epf_elss = st.session_state.get('ppf_epf_elss', 0)
        nps_contribution = st.session_state.get('nps_contribution', 0)
        medical_insurance = st.session_state.get('medical_insurance', 0)
        education_loan_interest = st.session_state.get('education_loan_interest', 0)
        donations = st.session_state.get('donations', 0)
        rent_paid = st.session_state.get('rent_paid', 0)
        dependents = st.session_state.get('dependents', 0)
        
        deductions = min(150000, ppf_epf_elss) + min(50000, nps_contribution) + min(200000, home_loan_interest) + min(25000, medical_insurance) + education_loan_interest + donations + (dependents * 25000)
    
    if st.button("Calculate Tax"):
        tax_amount = calculate_tax_new(income) if tax_regime == "New Tax Regime" else calculate_tax_old(income, deductions)
        st.write(f"### Your calculated tax is: ₹{tax_amount:,.2f}")

    st.subheader("Upload Expenditure Sheet")
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name=None)
        st.write("File uploaded successfully!")
        total_deductions = 0
        for sheet_name, data in df.items():
            st.write(f"### {sheet_name}")
            st.write(data.head())
            if sheet_name == 'Food':
                total_deductions += data['Bill Amount'].sum()
            elif sheet_name == 'Travel':
                total_deductions += data['Amount'].sum()
            elif sheet_name == 'Telephone':
                total_deductions += data['Amount'].sum()
            elif sheet_name == 'Books and Periodicals':
                total_deductions += data['Amount'].sum()
        
        st.write(f"### Total Deductions from Expenditure Sheet: ₹{total_deductions:,.2f}")
        st.session_state['total_deductions'] = total_deductions

# Call the function to display the app
show_tax_app()