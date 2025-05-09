# Data Processing Application

A Streamlit-based web application for processing and analyzing CSV data files.

## Features
- Upload CSV files
- Data cleaning (remove duplicates, handle missing values)
- Basic statistical analysis
- Data visualization (histogram, box plot, scatter plot)
- Download processed data as Excel file

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install openpyxl
```

## Running Locally
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud
1. Push your code to a GitHub repository
2. Sign in to Streamlit Cloud (share.streamlit.io)
3. Create a new app and link it to your GitHub repository
4. Specify `app.py` as the main file
5. Deploy the app

## Requirements
See `requirements.txt` for the list of required Python packages.

## License
MIT License
