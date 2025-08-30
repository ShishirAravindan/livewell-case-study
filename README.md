# Livewell Autonomous Care Agent

An AI-powered autonomous care agent for urinary tract infection (UTI) treatment automation, following clinical guidelines to provide immediate care for straightforward cases while ensuring complex cases receive appropriate human oversight.

## 🚀 Features

- **Natural Language Processing**: Understands patient symptoms described in everyday language
- **Clinical Decision Support**: Follows established UTI treatment protocols
- **Safety-First Approach**: Automatically identifies red flags requiring medical attention
- **Structured Logging**: Comprehensive evaluation and quality improvement tracking
- **CLI Interface**: Simple command-line interface with rich formatting

## 📋 Requirements

- Python 3.9+
- Google Gemini API key
- uv package manager (recommended)

## 🛠️ Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd livewell-case-study
   uv sync
   ```

2. **Configure API key**:
   ```bash
   # Set environment variable
   export GEMINI_API_KEY="your-gemini-api-key-here"

   # Or create a .env file
   echo "GEMINI_API_KEY=your-gemini-api-key-here" > .env
   ```

   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## 💡 Usage

Start the agent:
```bash
uv run python main.py
```

### Example Conversation

TODO: attach screenshot

---

## How it Works

- **Patient describes their symptoms in natural language** - they can type "I have burning sensation when I pee and need to go constantly" just like talking to a doctor
- **Language Understanding converts everyday language into medical data** - an LLM takes messy human descriptions and organizes them into clear, structured data (symptoms, severity, and so on)
- **Clinical Decision Engine follows clinical protocols** - applies the same [step-by-step guidelines](https://www.ocpinfo.com/wp-content/uploads/2022/12/assessment-prescribing-algorithm-urinary-tract-infection-english.pdf) that pharmacists and nurses use, checking for safety concerns and determining the right treatment
- **Response Generation explains the decision in plain English** - an LLM converts the medical recommendation back into clear instructions the patient can understand and follow
- **Evaluation & Logging captures everything for quality improvement** - records all interactions and decisions for future review and refinment of the system

The system prioritizes patient safety with built-in escalation protocols, ensuring complex cases receive appropriate human clinical oversight while autonomously handling routine cases that match established clinical protocols.

<p align="center">
  <img src="livewell.svg" alt="system-architecture" width="600"/>
</p>

## 📊 Logging and Evaluation

All conversations are logged to `logs/` directory for quality improvement:
- Session data in JSON format
- Clinical decision rationale
- LLM interaction metrics
- User input parsing success rates

## 📄 License

Educational use only. Not for clinical deployment without proper validation and regulatory approval.