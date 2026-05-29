# StudyTrack AI 📚

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00ff41?style=for-the-badge)

**Intelligent student habit analysis & academic performance prediction powered by ML + Gemini AI**

*Developed under Infosys Springboard · Mentor: Anil Kumar*

</div>

---

## 🧠 About

**StudyTrack AI** is a data-driven system that analyses students' study habits and predicts their academic performance using machine learning. Upload any CSV/Excel student dataset and the system automatically:

- Cleans and standardises the data
- Trains a Linear Regression model for marks prediction
- Clusters students into performance profiles via K-Means
- Generates personalised AI mentor feedback via **Gemini 2.5 Flash**

No manual feature engineering needed — column names are auto-detected.

---

## ⚙️ Execution Pipeline

```
AUTH → UPLOAD → CLEAN → TRAIN → CLUSTER → PREDICT → MENTOR AI
```

| Step | Description |
|------|-------------|
| `01 AUTH` | Secure sign-up with OTP email verification (rate-limited) |
| `02 UPLOAD` | Accept CSV or Excel student datasets up to 200 MB |
| `03 CLEAN` | Auto-detect columns, handle nulls, standardise names |
| `04 TRAIN` | Fit Linear Regression on 80/20 train-test split |
| `05 CLUSTER` | K-Means (k=3) groups students by performance profile |
| `06 PREDICT` | Infer marks & cluster for new or bulk student inputs |
| `07 MENTOR AI` | Gemini generates personalised, actionable feedback |

---

## ✦ Features

- 🔐 Secure authentication with OTP email verification
- 🔍 Auto-detection of column names in any CSV / Excel layout
- 📈 Linear Regression marks prediction (capped at 100)
- 🎯 K-Means clustering into 3 dynamic performance tiers
- 📊 Interactive Plotly visualisations (dark theme)
- 🤖 Gemini 2.5 Flash AI mentor with personalised feedback
- 📦 Bulk prediction with per-student smart suggestions
- 📥 Downloadable cleaned dataset and prediction reports
- 📉 Model metrics: R², MAE, RMSE, ±10 mark accuracy

---

## 🧩 Dashboard Modules

### `01` Data Analysis
Processed data preview table, model performance report (R², MAE, RMSE, predictions within ±10 marks), and downloadable cleaned XLSX.

### `02` Visualization
Cluster distribution bar chart and regression accuracy scatter plot, both rendered with Plotly's dark theme.

### `03` Marks Prediction
Input Study / Work / Play / Sleep hours → get a predicted score, cluster group classification, and a personalised Gemini AI mentor analysis.

### `04` Bulk Prediction
Upload a new student dataset for batch scoring. Each student receives a predicted mark, cluster ID, performance status, and a smart contextual suggestion. Export as CSV.

---

## 📊 Dataset at a Glance

| Metric | Value |
|--------|-------|
| Students | 250 |
| Features | StudyHours, WorkHours, PlayHours, SleepHour |
| Target | Marks (0–100) |
| Clusters | 3 (CRITICAL / OK / EXCELLENT) |
| Train / Test Split | 80% / 20% |

---

## 🎯 Cluster Classification

Clusters are mapped dynamically at runtime based on centroid average marks:

| Cluster | Label | Description |
|---------|-------|-------------|
| Lowest marks centroid | 🔴 **CRITICAL** — Needs Improvement | Immediate intervention advised |
| Mid marks centroid | 🟡 **OK** — Room for Optimisation | Incremental improvement possible |
| Highest marks centroid | 🟢 **EXCELLENT** — Maintain Trajectory | High performance, sustain habits |

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Streamlit |
| Language | Python 3.11 |
| ML — Regression | scikit-learn · LinearRegression |
| ML — Clustering | scikit-learn · KMeans |
| AI Mentor | Google Gemini 2.5 Flash |
| Visualisation | Plotly Express |
| Auth / Database | SQLite + bcrypt |
| Email OTP | smtplib / Gmail SMTP SSL |
| Data Processing | Pandas, NumPy |
| File I/O | openpyxl |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourname/studytrack-ai.git
cd studytrack-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure secrets

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY  = "your-gemini-api-key"
EMAIL_USER      = "your@gmail.com"
EMAIL_PASSWORD  = "your-gmail-app-password"
```

> **Note:** Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your main account password.

### 4. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
studytrack-ai/
├── app.py                    # Main Streamlit application
├── auth.py                   # Sign-in / Sign-up with OTP flow
├── db.py                     # SQLite user management
├── otp.py                    # OTP generation, storage & email
├── model.py                  # Linear Regression training & inference
├── kmeans_clustering.py      # K-Means clustering + cluster maps
├── data_cleaner.py           # Auto column-detect & normalisation
├── gemini_helper.py          # Gemini AI mentor integration
├── styles.py                 # Global CSS injector
├── requirements.txt
├── randomized_student_data.csv   # Sample dataset (250 students)
└── .devcontainer/
    └── devcontainer.json     # GitHub Codespaces config
```

---

## 🌐 Deploy on GitHub Codespaces

This repo includes a full Codespaces configuration. Just click **Code → Open with Codespaces** — it installs all dependencies and launches the app automatically on port `8501`.

---

## 🔮 Future Enhancements

- Integration with e-learning platforms (Moodle, Canvas)
- Real-time habit tracking via wearables / mobile
- Time-series and deep learning models
- Attention & focus metrics from webcam data
- Multi-language support
- Scalable deployment for educational institutions

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change. Make sure your code is clean and consistently formatted.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by **Abhishek Jain** · Infosys Springboard 2026

`RUNNING ON PORT 8501`

</div>
