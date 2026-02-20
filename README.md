🌤️ Weather AI Agent (ReAct)
A lightweight, autonomous AI agent that implements the ReAct (Reason + Act) pattern to provide real-time weather updates. Unlike traditional bots, this agent "thinks" through its plan and uses external tools to fetch live data, ensuring zero hallucination of weather conditions.

✨ Key Features
Autonomous Reasoning: Uses a logical loop to plan, act, and observe results.
Live Data Integration: Fetches actual atmospheric conditions via the wttr.in service.
Zero-Hallucination Policy: Strictly follows tool outputs for weather data.
Robust Parsing: Implements regex-based JSON extraction to handle conversational LLM outputs.
Resilient Design: Includes built-in 10-second backoff logic for Gemini Free Tier rate limits.
🛠️ Tech Stack
LLM: Google Gemini 1.5 Flash (via OpenAI SDK compatibility)
Runtime: Python 3.12+
Libraries: openai, python-dotenv, requests, re
🚀 Quick Start
1. Prerequisites
You will need a Google Gemini API Key. You can get one for free at Google AI Studio.

2. Installation
Bash
# Clone the repository
git clone https://github.com/yourusername/weather-agent.git
cd weather-agent

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# venv\Scripts\activate     # Windows

# Install dependencies
pip install openai python-dotenv requests
3. Configuration
Create a .env file in the root directory:

Code snippet
GEMINI_API_KEY=your_actual_key_here
4. Run the Agent
Bash
python agent.py
🧠 System Architecture
The agent operates on a State Machine logic:
PLAN: The AI analyzes the user query and describes its intended strategy.
TOOL: The AI outputs a JSON command (e.g., {"step": "TOOL", "tool": "get_weather", "input": "Delhi"}).
OBSERVE: The Python runtime catches the JSON, executes the get_weather function, and appends the result to the conversation.
OUTPUT: The AI synthesizes the observation into a final human-friendly response.
🗂️ Project Structure
Plaintext
Weather_Agent/
├── agent.py         # Main agent logic and ReAct loop
├── .env             # Sensitive API keys (Hidden)
├── .gitignore       # Prevents sensitive files from being committed
└── README.md        # You are here!