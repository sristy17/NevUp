# NevUp – Trading Behavior Analytics Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![NextJs](https://img.shields.io/badge/NextJs-Frontend-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-TSX-informational)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview
NevUp is a full-stack application designed to analyze trading behavior rather than just financial outcomes. Instead of focusing only on profit and loss, it evaluates how decisions are made during trading and highlights behavioral patterns that influence performance.

The platform processes trade data in real time and generates insights around discipline, emotional influence, and decision consistency.

---

## Tech Stack



### Backend
- FastAPI  
- SQLAlchemy  
- Python  

### Database
- PostgreSQL  

### Frontend
- Next.js (TypeScript)  

### Infrastructure
- Docker  
- Docker Compose  

---

## What It Does
NevUp ingests trade data through an API, stores it in a database, and computes behavioral metrics asynchronously. These insights are then displayed on an interactive dashboard that updates dynamically as new trades are added.

The system helps answer questions such as:
- Does performance change based on emotional state?
- Is the user trading impulsively after losses?
- Are there patterns of overtrading?
- How disciplined is the trading strategy over time?

---

## Core Capabilities

### Trade Ingestion
Trades are submitted through an API and stored reliably with idempotency, ensuring duplicate submissions do not corrupt data.

### Behavioral Analytics
The system evaluates each trade and computes metrics that reflect decision-making patterns rather than just outcomes.

### Session-Based Analysis
Trades are grouped into sessions, allowing the system to detect patterns such as repeated actions after losses within a short time frame.

### Real-Time Insights
Metrics are updated dynamically and reflected immediately on the dashboard, enabling continuous feedback.

### Interactive Simulation
The frontend includes a simulation feature that generates realistic trading behavior, making it easier to test and demonstrate system capabilities.

---

## Key Metrics

### Win Rate
Measures the percentage of profitable trades.

### Plan Adherence Score
Represents how closely trades follow a defined strategy or plan.

### Revenge Trades
Identifies trades placed shortly after a loss, indicating impulsive or emotionally driven decisions.

### Session Tilt
Tracks how often a trader continues trading after a loss within the same session. High values suggest emotional bias or lack of discipline.

### Win Rate by Emotion
Breaks down performance based on emotional states such as calm, anxious, or fearful, revealing how psychology impacts outcomes.

### Overtrading Detection
Flags unusually high trading frequency within short time intervals, which may indicate poor risk control.

---

## System Design

NevUp follows a streamlined architecture:

- The frontend provides an interface to submit trades and view insights  
- The backend handles API requests, authentication, and logic  
- The database stores trade data  
- Background processing computes behavioral metrics asynchronously  

This ensures fast responses while still performing deeper analysis in the background.

---

## User Experience

The dashboard presents:
- Key metrics in a structured format  
- Emotion-based performance breakdown  
- Session-level behavioral insights  
- Indicators for risky trading patterns  

Users can simulate multiple trades and observe how behavioral metrics evolve in real time.

---

rovides a deeper understanding of performance and helps identify patterns that would otherwise go unnoticed.
