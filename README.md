# 🛡️ Aadhaar Intelligence Hub  
### A Gov-Tech Command Center for Optimizing Citizen Services using Predictive Analytics & Geospatial Intelligence

The **Aadhaar Intelligence Hub** is a data-driven decision support system designed to assist **UIDAI administrators** in efficiently managing **Aadhaar Seva Kendras (ASKs)**.  
It transforms millions of rows of fragmented Aadhaar API datasets into **actionable insights** to reduce waiting times, identify demographic gaps, and optimize resource deployment across regions.

---

## 🚀 Core Capabilities

### 📈 Predictive Resource Allocation
- Forecasts daily enrolment and update traffic at Aadhaar centers using historical demand patterns  
- Includes a **System Stress Gauge** to alert administrators when service capacity is exceeded

### 👶 MBU (Mandatory Biometric Update) Gap Analysis
- Identifies the **digital divide** by comparing:
  - New child enrolments  
  - Mandatory Biometric Updates (MBU)
- Automatically flags **high-gap districts** requiring immediate attention

### 🚚 Strategic Mobile Aadhaar Van Planner
- Algorithmically recommends **high-priority routes** for mobile Aadhaar vans  
- Optimizes outreach based on regional demand and service gaps

### 🌍 Geospatial Command Center
- Interactive **state- and district-level heatmaps**
- Visualizes national demand density and regional service inequalities

### 📋 Executive PDF Reporting
- One-click generation of **professional, timestamped PDF briefing reports**
- Designed for field officers and decision-makers

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Language | Python 3.9+ |
| Frontend | Streamlit (Custom Glassmorphism CSS) |
| Data Processing | Pandas |
| Database | SQLite3 (Cleaned & Normalized) |
| Visualization | Plotly Express, Plotly Graph Objects |
| Reporting | FPDF |

---

## 📁 Project Structure

aadhaar_project/
├── app.py # Main Streamlit web application
├── db_builder.py # Data cleaning & SQL normalization engine
├── aadhaar_analysis.db # Processed SQLite database
├── requirements.txt # Python dependencies
└── data/ # Raw CSV API datasets


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/aadhaar-intelligence-hub.git
cd aadhaar-intelligence-hub
2️⃣ Install Dependencies
python -m pip install -r requirements.txt

3️⃣ Build the Cleaned Database

Run the normalization engine to merge raw datasets and fix legacy administrative mappings (e.g., Telangana–Andhra bifurcation).

python db_builder.py

4️⃣ Launch the Dashboard
python -m streamlit run app.py

🧩 Data Cleaning & Normalization Engine (Key Innovation)

Handling dirty and inconsistent historical data was a major challenge in this project.

The db_builder.py script implements a custom Normalization Engine that:

Remaps legacy districts (e.g., Hyderabad, Nalgonda) to modern states (Telangana)

Standardizes inconsistent casing (e.g., "Yadgir" vs "yadgir")

Fixes common typographical variations in district names

Ensures 100% referential integrity before analytics and visualization

📝 License

This project was developed for UIDAI DATA HACKATHON 2026 and is released under the MIT License for educational and non-commercial use.

👤 Contributor

Parijat Dwary
GitHub: https://github.com/pxrkerxd
