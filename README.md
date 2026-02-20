# 🌤️ Weather AI Agent (ReAct)

A lightweight, autonomous AI agent that implements the **ReAct (Reason + Act)** pattern to provide **real-time weather updates**.

Unlike traditional bots, this agent *thinks through its plan* and uses **external tools** to fetch **live weather data**, ensuring **zero hallucination** of atmospheric conditions.

---

## ✨ Key Features

- **Autonomous Reasoning**  
  Uses a logical loop to plan, act, and observe results.

- **Live Data Integration**  
  Fetches real weather data via the [`wttr.in`](https://wttr.in) service.

- **Zero-Hallucination Policy**  
  Weather responses strictly follow tool outputs.

- **Robust Parsing**  
  Regex-based JSON extraction handles conversational LLM outputs safely.

- **Resilient Design**  
  Built-in **10-second backoff** logic for Gemini Free Tier rate limits.

---

## 🛠️ Tech Stack

- **LLM:** Google Gemini 1.5 Flash (via OpenAI SDK compatibility)
- **Runtime:** Python 3.12+
- **Libraries:**  
  - `openai`  
  - `python-dotenv`  
  - `requests`  
  - `re`

---

## 🚀 Quick Start

### 1️⃣ Prerequisites

You will need a **Google Gemini API Key**.  
Get one for free from **Google AI Studio**.

---

### 2️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/weather-agent.git
cd weather-agent

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirement.txt