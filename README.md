# Livewell Autonomous Care Agent

An AI-powered autonomous care agent for urinary tract infection (UTI) treatment automation, following clinical guidelines to provide immediate care for straightforward cases while ensuring complex cases receive appropriate human oversight.

## 🏗️ System Architecture

<p align="center">
  <img src="docs/livewell.png" alt="Livewell System Architecture" width="750"/>
</p>

## 🔄 How It Works

- **Patient describes their symptoms in natural language** - they can type "I have burning sensation when I pee and need to go constantly" just like talking to a doctor
- **Language Understanding converts everyday language into medical data** - an LLM takes messy human descriptions and organizes them into clear, structured data (symptoms, severity, and so on)
- **Clinical Decision Engine follows clinical protocols** - applies the same [step-by-step guidelines](https://www.ocpinfo.com/wp-content/uploads/2022/12/assessment-prescribing-algorithm-urinary-tract-infection-english.pdf) that pharmacists and nurses use, checking for safety concerns and determining the right treatment
- **Response Generation explains the decision in plain English** - an LLM converts the medical recommendation back into clear instructions the patient can understand and follow
- **Evaluation & Logging captures everything for quality improvement** - records all interactions and decisions for future review and refinement of the system

The system prioritizes patient safety with built-in escalation protocols, ensuring complex cases receive appropriate human clinical oversight while autonomously handling routine cases that match established clinical protocols.

## 📚 Documentation Structure

| Document | Purpose |
|----------|---------|
| [**Deliverable 01: Conceptual Guide**](./docs/01-conceptual-overview.md) | System architecture & conceptual explanation |
| [**Setup & Installation**](./uti-agent/README.md) | Complete setup instructions, API configuration, and usage guide |
| [**Deliverable 03: Agent Eval & CI**](./docs/03-agent-eval-CI.md) | Short paper on managing agentic system |

## 📁 Project Structure

```
livewell-case-study/
├── README.md                   # Project overview and navigation
├── uti-agent/                  # Core agent implementation
│   ├── README.md                   # Setup and technical guide
│   ├── main.py                     # CLI entry point
│   ├── core/                       # Core components
│   ├── models/                     # Data models
│   ├── utils/                      # Utilities and logging
│   └── tests/                      # Test suite
└── docs/
    ├── 01-conceptual-overview.md
    ├── 03-agent-eval-CI.md
```

## 🚀 Quick Start

*See the [Setup Guide](./uti-agent/README.md) for detailed installation and configuration instructions.*

```bash
# Navigate to the agent directory
cd uti-agent

# Install dependencies
uv sync

# Run the agent
uv run python main.py
```

## ⚠️ Important Notice

Educational use only. Not for clinical deployment without proper validation and regulatory approval.

---