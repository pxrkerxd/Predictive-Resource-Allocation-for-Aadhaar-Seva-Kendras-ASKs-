🛡️ Aadhaar Intelligence Hub: Gov-Tech Command Center
Optimizing Citizen Services through Predictive Analytics & Geospatial Intelligence
The Aadhaar Intelligence Hub is a data-driven decision support system designed to assist UIDAI administrators in managing Aadhaar Seva Kendras (ASKs). It transforms millions of rows of fragmented API data into actionable insights to reduce waiting times, bridge demographic gaps, and optimize resource deployment.

🚀 Key Features
📈 Predictive Resource Allocation: Forecasts daily traffic surges at Aadhaar centers using historical demand patterns. Includes a "System Stress Gauge" to alert managers when capacity is exceeded.

👶 MBU Gap Analysis: Identifies the "Digital Divide" by comparing new child enrolments against Mandatory Biometric Updates (MBU). High-gap districts are automatically flagged.

🚚 Strategic Mobile Van Planner: An algorithmic engine that suggests high-priority routes for mobile Aadhaar vans based on regional demand and service gaps.

🌍 Geospatial Command Center: A state-and-district level heatmap to visualize national demand and regional inequalities.

📋 Executive PDF Reporting: Generate professional, timestamped briefing documents for field officers with a single click.

🛠️ Tech Stack
Language: Python 3.9+

Frontend: Streamlit (with Custom Glassmorphism CSS)

Data Processing: Pandas

Database: SQLite3 (Cleaned & Normalized)

Visualization: Plotly Express & Plotly Graph Objects

Reporting: FPDF

📁 Project Structure
Plaintext

aadhaar_project/
├── app.py                # Main Streamlit Web Application
├── db_builder.py         # Data Cleaning & SQL Normalization Script
├── aadhaar_analysis.db   # Processed SQLite Database
├── requirements.txt      # List of dependencies
└── data/                 # Raw CSV API Datasets (Biometric, Demographic, Enrolment)
⚙️ Installation & Setup
1. Clone the repository
Bash

git clone https://github.com/yourusername/aadhaar-intelligence-hub.git
cd aadhaar-intelligence-hub
2. Install Dependencies
Bash

python -m pip install -r requirements.txt
3. Build the Cleaned Database
Run the builder script to merge the raw CSVs and apply the modern administrative mapping (fixing Telangana/Andhra legacy issues).

Bash

python db_builder.py
4. Launch the Dashboard
Bash

python -m streamlit run app.py
🧩 The "Data Cleaning" Innovation
One of the biggest challenges in this project was handling dirty historical data. Our db_builder.py script includes a custom Normalization Engine that:

Remaps legacy districts (like Hyderabad/Nalgonda) to their modern states (Telangana).

Standardizes inconsistent casing (e.g., merging "Yadgir" and "yadgir").

Fixes common typographical variants in district names to ensure 100% data accuracy.

📝 License
This project is developed for [Insert Hackathon Name] and is open for educational use under the MIT License.

Contributor
https://github.com/pxrkerxd
