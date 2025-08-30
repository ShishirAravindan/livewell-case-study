# UTI Care Agent - Setup & Technical Guide

This is the core implementation of the Livewell UTI Care Agent - an AI-powered command-line tool for assessing urinary tract infection (UTI) symptoms and providing evidence-based treatment recommendations.

## 🚀 Features

- **Intelligent Symptom Assessment**: Uses LLM-powered natural language understanding to extract symptoms from patient descriptions
- **Clinical Decision Engine**: Implements UTI clinical guidelines with safety checks and exclusion criteria
- **Treatment Recommendations**: Provides first-line antibiotic recommendations with alternatives based on allergies
- **Safety-First Approach**: Defaults to referral for complicated cases or red flag symptoms
- **Conversational Interface**: Natural CLI conversation flow with empathetic responses

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.9+
- UV package manager
- Google Gemini API key

### Installation

1. Clone and navigate to the project:
    ```bash
    git clone https://github.com/ShishirAravindan/livewell-case-study.git
    cd uti-agent
    ```

2. Install dependencies:
    ```bash
    uv sync
    ```

3. Set up environment variables:

    **Google Gemini API Setup**
    1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. Add it to your `.env` file as shown above

    ```bash
    # GOOGLE_API_KEY=your-actual-api-key-here
    ```

### Usage

4. **Run the Agent** 
    - Make sure you are in the `uti-agent` directory before running the agent.
    ```bash
    uv run python main.py
    ```

## Development

### Clinical Logic

The agent implements standard UTI assessment criteria:
- **Symptom Assessment**: Acute dysuria OR 2+ qualifying symptoms
- **Exclusion Screening**: Male patients, pregnancy, age <12, immunocompromised
- **Treatment Selection**: Nitrofurantoin first-line, alternatives for allergies
- **Safety Mechanisms**: Default referral for complications or uncertainty

### Adding New Features
The modular architecture allows easy extension:
- Add new extraction patterns in `input_parser.py`
- Extend clinical rules in `clinical_engine.py`  
- Customize responses in `response_gen.py`