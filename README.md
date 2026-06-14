# 🚢 SmartContainer Risk Engine

**AI-powered customs shipment risk monitoring and anomaly detection platform.**

SmartContainer Risk Engine is an end-to-end ML system that helps customs and trade-compliance teams flag high-risk shipments in real time. It pairs a trained risk classification & anomaly detection model with a SHAP-based explainability layer, exposed through an interactive Streamlit dashboard and a production-ready FastAPI inference service.

---

## 🔗 Live Demo

| Resource | Link |
|---|---|
| 🖥️ Streamlit Dashboard | [smartcontainer-risk-engine.streamlit.app](https://smartcontainer-risk-engine-fz4vxkakst8qlg9e8uye7m.streamlit.app/) |
| ⚙️ Prediction API (FastAPI on Render) | [smartcontainer-risk-engine-api.onrender.com](https://smartcontainer-risk-engine-api.onrender.com) |
| 📦 Source code | [AnshulRPatel/smartcontainer-risk-engine](https://github.com/AnshulRPatel/smartcontainer-risk-engine) |

> ⚠️ The API is hosted on Render's free tier, so the first request after a period of inactivity may take a few extra seconds while the service spins up.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [License](#license)
- [Author](#author)

---

## Overview

Customs agencies process thousands of shipment declarations every day, and only a fraction can be manually inspected. SmartContainer Risk Engine scores every incoming shipment for risk and anomaly likelihood, surfaces the key drivers behind each score, and gives analysts a single dashboard to triage, investigate, and explain decisions — individually or in bulk.

## Features

- **Executive Overview** — High-level KPIs (total shipments, critical/medium risk counts, average anomaly score) plus a shipment risk distribution chart (Low / Medium / Critical).
- **Operational Queue** — Working queue of shipments for analyst review.
- **Anomaly Intelligence** — Drill-down into shipments with abnormal anomaly scores.
- **Behavioral Intelligence** — Pattern analysis across importers, exporters, and shipping lines.
- **Importer / Exporter Profiles** — Historical shipment behavior by trade entity.
- **Live Prediction** — Submit a single shipment's details to the live FastAPI service and instantly get back a risk label, model confidence, risk score, anomaly score, a plain-language explanation, and the top contributing risk factors.
- **Batch Intelligence Center** — Upload a shipment CSV (up to 200MB) to generate predictions for an entire batch at once.
- **Explainability Center** — Global and local SHAP explanations (summary plot, bar plot, and per-shipment SHAP values), generated after running a live or batch prediction.
- **Dashboard Filters** — Filter every view by Risk Level (Critical / Medium / Low) and Trade Regime (Import / Transit).

## Screenshots

### Executive Overview
Total shipment counts, risk breakdown, and risk distribution chart.

![Executive Overview](screenshots/executive_overview.png)

### Live Prediction — Input Form
Analysts enter shipment metadata (Container ID, declaration date/time, trade regime, origin/destination, HS code, importer/exporter IDs, declared value & weight, measured weight, shipping line, dwell time).

![Live Prediction Form - Part 1](screenshots/live_prediction_form_1.png)
![Live Prediction Form - Part 2](screenshots/live_prediction_form_2.png)

### Live Prediction — Result
The model returns a predicted risk label, confidence score, risk/anomaly scores, a human-readable explanation, and the top risk factors driving the decision.

![Prediction Result](screenshots/prediction_result.png)

### Batch Intelligence Center
Upload a shipment CSV to generate predictions and explore risk insights across an entire batch.

![Batch Intelligence Center](screenshots/batch_intelligence_center.png)

### Explainability Center
SHAP-based global and local explanations, generated once a live or batch prediction has been run.

![Explainability Center](screenshots/explainability_center.png)

## Tech Stack

- **Frontend / Dashboard:** [Streamlit](https://streamlit.io/) multipage app (deployed on Streamlit Community Cloud)
- **Backend / Inference API:** [FastAPI](https://fastapi.tiangolo.com/) (deployed on [Render](https://render.com/) via `render.yaml`)
- **Risk Classification:** [CatBoost](https://catboost.ai/)
- **Anomaly Detection:** Isolation Forest (scikit-learn)
- **Explainability:** [SHAP](https://shap.readthedocs.io/) (global summary/bar plots + per-shipment local explanations)
- **Experiment Tracking:** [MLflow](https://mlflow.org/)
- **Containerization:** Docker & Docker Compose
- **CI:** GitHub Actions
- **Language:** Python

## How It Works

1. An analyst enters shipment details in the **Live Prediction** form, or uploads a CSV via the **Batch Intelligence Center**.
2. The Streamlit app sends the shipment data to the FastAPI prediction service.
3. The API runs the data through the trained risk classification and anomaly detection models and returns:
   - `Predicted Risk` / `Risk Label` (e.g., Low, Medium, Critical)
   - `Model Confidence`
   - `Risk Score`
   - `Anomaly Score`
   - A natural-language `Explanation`
   - `Top Risk Factors` driving the prediction
4. SHAP artifacts (summary plot, bar plot, local SHAP values) are generated and surfaced in the **Explainability Center**.
5. Dashboards (Executive Overview, Operational Queue, Anomaly Intelligence, Behavioral Intelligence, Importer/Exporter Profiles) aggregate these results, filterable by risk level and trade regime.

## Getting Started

### Prerequisites
- Python 3.9+
- pip
- (Optional) Docker & Docker Compose

### Clone & Install

```bash
git clone https://github.com/AnshulRPatel/smartcontainer-risk-engine.git
cd smartcontainer-risk-engine
```

Install dependencies for the component(s) you want to run:

```bash
# API only
pip install -r requirements-api.txt

# Dashboard only
pip install -r requirements-dashboard.txt

# Everything (full dev environment)
pip install -r requirements.txt
```

### Run the API locally

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### Run the Streamlit dashboard locally

```bash
streamlit run dashboard/app.py
```

> Update the API base URL used by the dashboard (e.g., in `.env` or `dashboard/utils/api_client.py`) to point to your local API (`http://localhost:8000`) when running everything locally.

### Run with Docker

```bash
docker-compose up --build
```

## API Reference

**Base URL:** `https://smartcontainer-risk-engine-api.onrender.com`

| Endpoint | Method | Description |
|---|---|---|
| `/predict` | `POST` | Submit a single shipment's data and receive a risk prediction, anomaly score, explanation, and top risk factors. |
| `/explain` | `GET` / `POST` | Retrieve SHAP-based local/global explanations for a prediction. |
| `/model-info` | `GET` | Metadata about the currently loaded risk and anomaly models. |
| `/monitoring` | `GET` | Model and prediction monitoring metrics/logs. |
| `/health` | `GET` | Service health check. |
| `/docs` | `GET` | Interactive FastAPI (Swagger) documentation for all available endpoints. |

> Exact paths and request/response schemas may vary slightly — see `/docs` on the live API for the authoritative, up-to-date reference.

Example `/predict` request body:

```json
{
  "container_id": "88268883",
  "declaration_date": "2020-01-02",
  "declaration_time": "20:56:03",
  "trade_regime": "Import",
  "origin_country": "CN",
  "destination_port": "PORT_40",
  "destination_country": "RS",
  "hs_code": "610910",
  "importer_id": "EKI0ID0",
  "exporter_id": "CXC3E7O",
  "declared_value": 624.0,
  "declared_weight": 40.0,
  "measured_weight": 48.3,
  "shipping_line": "LINE_MODE_40",
  "dwell_time_hours": 93.4
}
```

## Project Structure

```
smartcontainer-risk-engine/
├── app/                        # FastAPI backend service
│   ├── core/                   # Config, logging, versioning
│   ├── models/                 # Pydantic request/response schemas
│   ├── routers/                # API endpoints (predict, explain, health, model_info, monitoring)
│   ├── services/                # Model, anomaly, explainability & risk calibration logic
│   ├── utils/                  # Inference helpers
│   └── main.py                 # API entry point
│
├── dashboard/                   # Streamlit frontend
│   ├── assets/                  # Static assets
│   ├── components/              # KPI cards, charts, sidebar filters, queue table
│   ├── pages/                   # Executive Overview, Live Prediction, Batch Intelligence, etc.
│   ├── utils/                   # API clients, data loader, metrics helpers
│   └── app.py                   # Dashboard entry point
│
├── ml/                           # Model training & ML pipeline
│   ├── preprocessing/            # Data cleaning & schema validation
│   ├── features/                 # Feature engineering (behavioral, temporal, anomaly, outlier)
│   ├── labeling/                  # Risk scoring & label generation
│   ├── modeling/                  # Training, evaluation, feature importance
│   ├── anomaly_detection/          # Isolation Forest pipeline & evaluation
│   ├── explainability/             # SHAP analysis & explanation generation
│   ├── inference/                  # Inference helpers
│   └── training/                   # Exploration notebooks
│
├── data/                          # raw / processed / synthetic shipment datasets
├── outputs/                        # Trained models, metrics, SHAP plots, predictions, reports
├── templates/                      # Sample CSV template for batch uploads
├── scripts/                         # Debugging & validation scripts
├── tests/                            # Unit & integration tests
├── docker/                           # Docker configs
├── screenshots/                       # Dashboard screenshots (used in this README)
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml                        # Render deployment config (API)
├── requirements_main.txt                    # Full dev environment
├── requirements-api.txt                # API-only dependencies
├── requirements-dashboard.txt          # Dashboard-only dependencies
├── LICENSE
└── README.md
```

## Roadmap

- [ ] Pre-populate the Explainability Center with sample SHAP artifacts
- [ ] Add authentication for the Live Prediction and Batch Intelligence endpoints
- [ ] Expand Behavioral Intelligence with time-series trend views
- [ ] Add automated model retraining pipeline

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Anshul R Patel**
GitHub: [@AnshulRPatel](https://github.com/AnshulRPatel)