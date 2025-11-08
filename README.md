# 🧠 Data Quality Validator

A lightweight **Python-based ETL utility** that validates raw data files (CSV/JSON) for schema consistency, nulls, duplicates, and data type mismatches before loading.  
Designed for data engineers who want a reusable pre-validation step in ETL pipelines.

---

## 📘 Overview
In real-world ETL systems, poor-quality data can break downstream analytics.  
This project provides a configurable **Data Quality Validator** that checks data before it enters your warehouse or analytics layer.

The validator:
- Reads a file (CSV/JSON)
- Validates column schema & data types
- Detects nulls, duplicates, invalid ranges
- Generates summary reports and logs results

---

## 🧱 Architecture

+--------------------+
| Raw Data (CSV/JSON)| --> validation_rules.yaml
+--------------------+
|
▼
+---------------------+
| Data Quality Check |
| (Python + Pandas) |
+---------------------+
|
▼
+--------------------+
| Logs & Reports |
+--------------------+

---

## ⚙️ Tech Stack
| Component | Technology |
|------------|-------------|
| **Language** | Python 3 |
| **Libraries** | Pandas, PyYAML, Logging, argparse |
| **Data Sources** | CSV, JSON |
| **Output** | Console + Report file (CSV) |

---

## 🧩 Features
✅ Configurable validation rules (in YAML)  
✅ Checks for nulls, duplicates, invalid data types  
✅ Logs invalid rows to separate files  
✅ Generates summary report with pass/fail counts  
✅ Modular code structure for easy reuse  

---

