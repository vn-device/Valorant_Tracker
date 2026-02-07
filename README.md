# Valorant Tactical Telemetry (VTT)

> **Status:** Active Development  
> **Architecture:** Low-Latency Computer Vision & Riot API Integration

## ⚡ System Overview
VTT is a high-performance analysis engine designed to quantify "device-coded" fundamentals in tactical FPS scenarios. Unlike standard trackers that rely solely on post-match aggregate stats, VTT fuses real-time telemetry with computer vision to isolate mechanical consistency and positioning errors.

### Core Modules
* **Device Engine (`src/device_engine.py`):** The physics core. Handles local state processing and input latency compensation calculations.
* **API Client (`src/api_client.py`):** Asynchronous wrapper for the Riot API, optimized for burst-rate limit handling and minimal overhead.
* **CV Pipeline (Planned):** Real-time crosshair placement validation using OpenCV.

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **Concurrency:** AsyncIO for non-blocking API telemetry.
* **State Management:** Localized discrete event simulation (DES) for match reconstruction.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Riot Developer Key (stored locally in `.env`)

### Installation
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/vn-device/valorant-tracker.git](https://github.com/vn-device/valorant-tracker.git)
    cd valorant-tracker
    ```

2.  **Environment Setup**
    ```bash
    python -m venv env
    .\env\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configuration**
    Create a `.env` file in the root:
    ```ini
    RIOT_API_KEY=RGAPI-xxxx-xxxx
    ```

## 🔒 Security & Compliance
This tool adheres to Riot Games' third-party developer policies.
* No memory reading or injection.
* Passive screen analysis only.
* API keys are strictly git-ignored.

---
*Maintained by vn-device*