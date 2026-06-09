# 🔒 Real-Time Fraud Detection System

Enterprise-grade fraud detection system with ML, streaming, and real-time analytics.

## Architecture

┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │ Kafka │───▶│ Stream │───▶│ Redis │ │ Producer │ │ Processor │ │ Cache │ └─────────────┘ └─────────────┘ └─────────────┘  │ │  ▼ ▼ ┌─────────────┐ ┌─────────────┐ │ FastAPI │◀───────────────────│ Streamlit │ │ API │ │ Dashboard │ └─────────────┘ └─────────────┘


## Tech Stack
- **Backend**: FastAPI, Python 3.11
- **ML**: Scikit-learn, XGBoost
- **Streaming**: Kafka, Confluent
- **Cache**: Redis
- **Frontend**: Streamlit, Plotly
- **Deployment**: Docker, Docker Compose

## Quick Start

```bash
# Start all services
docker-compose up -d

# API: http://localhost:8000
# Dashboard: http://localhost:8501
