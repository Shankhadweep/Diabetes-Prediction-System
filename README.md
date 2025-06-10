<div align="center">
  <h1>🏥 Diabetes Prediction System</h1>
  <p>An intelligent healthcare solution leveraging Machine Learning to predict diabetes risk.</p>
  
  ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
  ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Sklearn-orange)
  ![License](https://img.shields.io/badge/License-MIT-green)
  ![Status](https://img.shields.io/badge/Status-Active-brightgreen)
</div>

## 📋 Table of Contents
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Model Performance](#model-performance)

## 🎯 About <a name="about"></a>
The Diabetes Prediction System is an innovative healthcare solution that utilizes machine learning algorithms to predict the likelihood of diabetes in patients based on various health parameters. This system aims to assist healthcare professionals in early diagnosis and preventive care.

## ✨ Features <a name="features"></a>
- 🔍 Real-time diabetes risk prediction
- 📊 Interactive data visualization
- 🎯 High prediction accuracy
- 📱 User-friendly interface
- 📈 Detailed analysis reports
- 🔐 Secure data handling

## 🛠️ Tech Stack <a name="tech-stack"></a>
- Python 3.8+
- Scikit-learn
- Pandas
- NumPy
- Streamlit

## ⚙️ Installation <a name="installation"></a>
1. Clone the repository
```bash
git clone https://github.com/Shankhadweep/Diabetes-Prediction-System.git
```
2.Install required packages
```bash
pip install -r requirements.txt
```
3.Run the application
```bash
streamlit run app.py
```
## 📊 Model Performance Metrics

### Overall Metrics
| Metric    | Score (%) |
|-----------|-----------|
| Accuracy  | 84.2      |
| Precision | 83.7      |
| Recall    | 82.1      |
| F1-Score  | 82.9      |

### Detailed Classification Metrics

```python
Classification Report:
              precision    recall  f1-score   support

           0       0.85      0.88      0.86       102  # Non-diabetic
           1       0.81      0.76      0.79        52  # Diabetic

    accuracy                           0.84       154
   macro avg       0.83      0.82      0.82       154
weighted avg       0.84      0.84      0.84       154
