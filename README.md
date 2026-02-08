# Device Tactical Analyst (DTA)

> **Status:** Stable Release (v1.0)
> **Architecture:** Modular Python Analysis Engine & HenrikAPI Integration

## ⚡ System Overview
**Device Tactical Analyst** is a specialized telemetry tool designed to audit Valorant gameplay against the "Device Philosophy"—the tactical framework of Nicolai "device" Reedtz.

Unlike standard trackers that prioritize raw K/D, this engine isolates **Systemic Discipline**:
* **Untradeability Index:** Measures your ability to reset positioning after a kill (Survival Rate).
* **Opening Duel Discipline:** Audits "First Death" rates to prevent over-aggression.
* **Economy Efficiency:** (In Progress) Calculates ROI on Operator purchases.

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **API Integration:** [HenrikDev Valorant API (v3)](https://github.com/Henrik-3/valorant-libs)
* **Resilience:** Custom `@retry_with_backoff` decorators for rate-limit handling.
* **Analysis Core:**
    * `DeviceEngine`: Calculates Survival Rate & KAST alignment.
    * `OpeningDuelAnalyzer`: Reconstructs round timelines to audit entry aggression using PUUID tracing.

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* A free API Key from [HenrikDev](https://henrikdev.xyz/)

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/vn-device/valorant-tracker.git](https://github.com/vn-device/valorant-tracker.git)
    cd valorant-tracker
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**
    Create a `.env` file in the root directory and populate it with your details:
    ```ini
    HENRIK_API_KEY=HDEV-xxxx-xxxx-xxxx
    VALORANT_NAME=YourName
    VALORANT_TAG=YourTag
    ```

### Usage

**Standard Analysis (Last 3 Competitive Games)**
```bash
python main.py