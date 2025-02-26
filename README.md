# Not-so-Taxing: An App for Managing Taxes

Welcome to the Not-so-Taxing app! This application helps you manage your taxes by providing features such as tax calculation, document checklist, expenditure analysis, and summarizing tax advice from financial advisors.

## Features

- **Tax Filing Document Checklist**: Provides a list of mandatory and additional documents required for tax filing.
- **AI-Powered Deduction Suggestions**: Suggests eligible deductions based on your inputs.
- **Income Tax Calculator**: Calculates your income tax based on the selected tax regime (New or Old).
- **Expenditure Analysis**: Upload and analyze your expenditure sheet to calculate total deductions.
- **Tax Collection Forecast**: Forecasts future tax collections using ARIMA and LSTM models.
- **Tax Advice Summarization**: Summarizes tax advice from financial advisors' articles.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository  
```sh
git clone https://github.com/yourusername/not-so-taxing.git
cd not-so-taxing
```
### 2.Create a Virtual Environment
```sh
python -m venv venv
```
### 3. Activate the Virtual Environment
Windows:
```sh
venv\Scripts\activate
```
mac/Linux:
```sh
source venv/bin/activate
```
### 4. Install the Required Packages
```sh
pip install -r requirements.txt
```
### Running the Application
```sh
streamlit run app.py
```
### Running Tests
These tests ensure all components are working correctly
```sh
python -m unittest test_app.py
```
Usage:
*Navigation: Use the sidebar to navigate to different sections of the app.
*Tax Calculator: Enter your annual income and select the tax regime to calculate your tax.
*Expenditure Analysis: Upload your expenditure sheet to calculate total deductions.
*Tax Advice: Enter the URL of a financial advisor's article to get a summarized list of do's and don'ts for reducing taxes.

Notes:
*The app may take a few minutes to load due to the training of the LSTM model.
*If the app does not load correctly, try refreshing the page.
