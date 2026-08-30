# 🏥 Health Data Fraud Risk Analysis Dashboard

> **An interactive Streamlit dashboard for exploring healthcare provider data, identifying fraud-risk patterns, and monitoring key financial and operational indicators.**

---

## 🚀 Live Dashboard

🔗 **Live Streamlit App:** `https://health-data-fraud-streamlit.streamlit.app/`

> 💡 If your deployed Streamlit URL is different, replace the URL above with your actual app link.

---

## 📌 Project Overview

Healthcare claims and provider data can contain complex patterns related to **payments, charges, utilization, provider activity, and potential fraud risk**.

This project transforms healthcare provider data into an **interactive analytical dashboard** that helps users:

- 🔎 Explore provider-level data
- 📊 Analyze financial and operational KPIs
- 🚨 Identify unusual or high-risk patterns
- 📈 Compare providers and categories
- 🎯 Filter the dashboard dynamically
- 💡 Generate data-driven insights

The dashboard is designed as a **Data Analytics / Fraud Risk Analysis project**, not as a medical diagnosis system.

---

## 🎯 Business Problem

Healthcare organizations handle large volumes of provider and claim-related data. Manually analyzing this information makes it difficult to identify:

- Unusual payment patterns
- High utilization
- Significant charge-to-payment differences
- Providers with unusual performance metrics
- Potentially suspicious financial behavior

### 💡 Objective

Build an interactive analytics solution that converts raw healthcare data into **actionable fraud-risk insights** through KPIs, filters, and visualizations.

---

## 📊 Key KPIs

The dashboard focuses on important healthcare financial and operational indicators, including:

| KPI | Purpose |
|---|---|
| 💰 **Payment per Episode** | Measures the average payment associated with an episode |
| 📉 **LUPA Rate** | Helps evaluate the frequency of Low Utilization Payment Adjustments |
| 💵 **Charge-to-Payment Ratio** | Compares submitted charges with actual payments |
| 🏥 **Provider Activity** | Helps understand provider-level operational patterns |
| 🚨 **Risk Indicators** | Highlights patterns that may require further investigation |

> ⚠️ A high-risk indicator does **not** automatically mean fraud. It represents a pattern that may require additional investigation.

---

## 🎛️ Interactive Dashboard

The Streamlit application provides interactive filtering and visualization capabilities.

### 🔹 Filters

Users can dynamically filter the analysis using dashboard slicers such as:

- 📍 Provider / Location-related dimensions
- 🏥 Provider categories
- 📅 Relevant time periods
- 📊 Other available categorical dimensions

The selected filters dynamically update the dashboard's KPIs and visualizations.

---

## 📈 Dashboard Visualizations

The dashboard contains multiple analytical visualizations designed to examine different dimensions of healthcare provider data.

### 📊 Analytical Views

- 📈 Trend analysis
- 📊 Category-wise comparison
- 🏥 Provider-level analysis
- 💰 Payment and charge analysis
- 🥧 Distribution analysis
- 🚨 Fraud-risk pattern exploration

These visualizations allow users to move from **high-level KPIs → detailed patterns → potential risk areas**.

---

## 🧠 Analytical Approach

The project follows a practical data analytics workflow:

```text
Raw Healthcare Data
        ↓
Data Loading
        ↓
Data Cleaning & Preparation
        ↓
Exploratory Data Analysis
        ↓
KPI Development
        ↓
Fraud-Risk Pattern Analysis
        ↓
Interactive Visualization
        ↓
Streamlit Dashboard
        ↓
Actionable Insights
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 **Python** | Data analysis and application development |
| 🧮 **Pandas** | Data manipulation and analysis |
| 🔢 **NumPy** | Numerical operations |
| 📊 **Plotly** | Interactive visualizations |
| 🎨 **Streamlit** | Interactive dashboard and deployment |
| 📁 **JSON** | Healthcare dataset storage |
| 🐙 **Git & GitHub** | Version control and project hosting |
| ☁️ **Streamlit Community Cloud** | Dashboard deployment |

---

## 📂 Project Structure

```text
Health_Data_Fraud_Risk_Analysis/
│
├── 📁 data/
│   └── health_data_100k.json
│
├── 🐍 app.py
│
├── 📄 requirements.txt
│
├── 📄 .gitattributes
│
└── 📄 README.md
```

### 📌 File Description

**`app.py`**  
Main Streamlit application containing the dashboard logic, data processing, KPIs, filters, and visualizations.

**`data/health_data_100k.json`**  
Healthcare dataset used by the dashboard.

**`requirements.txt`**  
Contains the Python dependencies required to run the application.

**`.gitattributes`**  
Git configuration used for handling the large dataset through Git LFS.

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/pslvgyanendra/Health_Data_Fraud_Risk_Analysis.git
```

### 2️⃣ Navigate to the project

```bash
cd Health_Data_Fraud_Streamlit
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit application

```bash
streamlit run app.py
```

### 5️⃣ Open the dashboard

Streamlit will provide a local URL, normally similar to:

```text
http://localhost:8501
```

---

## 🔍 Fraud Risk Analysis Perspective

This dashboard should be interpreted as a **risk-analysis and anomaly-identification tool**.

The objective is to identify **unusual patterns**, such as:

- 📌 Providers with unusually high payment activity
- 📌 Significant differences between charges and payments
- 📌 Unusual utilization patterns
- 📌 Outlier provider behavior
- 📌 Concentrations of activity in specific categories

These signals can support **further investigation and decision-making**.

> 🚨 **Important:** The dashboard does not independently establish that a provider committed fraud. Any fraud determination requires appropriate investigation, validation, and domain expertise.

---

## 💼 Business Value

The project demonstrates how data analytics can support healthcare organizations by:

✅ Converting raw data into meaningful KPIs  
✅ Reducing manual exploratory analysis  
✅ Identifying unusual provider patterns  
✅ Improving analytical visibility  
✅ Supporting fraud-risk investigation  
✅ Enabling interactive, filter-based exploration  
✅ Presenting complex healthcare data in an understandable format  

---

## 👨‍💻 Skills Demonstrated

### Data Analytics

- 🧹 Data Cleaning
- 🔄 Data Transformation
- 🔍 Exploratory Data Analysis
- 📊 KPI Development
- 📈 Data Visualization
- 🚨 Fraud Risk Analysis
- 💡 Business Insight Generation

### Python

- Pandas
- NumPy
- Plotly
- Streamlit
- JSON Data Handling

### Deployment & Version Control

- Git
- GitHub
- Git LFS
- Streamlit Community Cloud

---

## 🌟 Project Highlights

- 📦 **100K-row healthcare dataset**
- 🎛️ Interactive dashboard filters
- 📊 Multiple analytical visualizations
- 💰 Healthcare financial KPIs
- 🚨 Fraud-risk pattern analysis
- ⚡ Streamlit-based interactive interface
- ☁️ Cloud-deployed dashboard
- 🐙 GitHub version-controlled project

---

## 📸 Dashboard Preview

> Add screenshots of the dashboard here to make the GitHub repository more visually attractive.

Example:

```text
📸 Dashboard Screenshot
📸 KPI Section
📸 Fraud Risk Analysis
📸 Interactive Charts
```

---

## 🔗 Project Links

| Resource | Link |
|---|---|
| 🌐 **Live Dashboard** | `https://health-data-fraud-streamlit.streamlit.app/` |
| 🐙 **GitHub Repository** | `https://github.com/pslvgyanendra/Health_Data_Fraud_Risk_Analysis` |

---

## ⚠️ Disclaimer

This project is created for **educational, analytical, and portfolio purposes**.

The dashboard identifies analytical patterns and potential risk indicators. It should **not** be used as the sole basis for accusing a healthcare provider of fraud or making clinical, legal, or financial decisions.

---

## 👤 Author

### **Gyanendra Singh**

📊 **Data Analyst | Python | SQL | Power BI | Tableau | Streamlit**

🔗 **GitHub:** `https://github.com/pslvgyanendra`

---

## ⭐ Support

If you find this project useful:

⭐ **Star the repository**  
🍴 **Fork the project**  
💬 **Share your feedback**

---

### 🚀 Built with Python, Streamlit & Data Analytics

**Turning healthcare data into actionable insights. 📊🏥**
