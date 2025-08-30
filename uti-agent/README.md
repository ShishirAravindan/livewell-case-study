# UTI Care Agent

An AI-powered command-line tool for assessing urinary tract infection (UTI) symptoms and providing evidence-based treatment recommendations.

## Features

- **Intelligent Symptom Assessment**: Uses LLM-powered natural language understanding to extract symptoms from patient descriptions
- **Clinical Decision Engine**: Implements UTI clinical guidelines with safety checks and exclusion criteria
- **Treatment Recommendations**: Provides first-line antibiotic recommendations with alternatives based on allergies
- **Safety-First Approach**: Defaults to referral for complicated cases or red flag symptoms
- **Conversational Interface**: Natural CLI conversation flow with empathetic responses

## Setup

### Prerequisites
- Python 3.9+
- UV package manager
- Google Gemini API key

### Installation

1. Clone and navigate to the project:
```bash
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

## Usage

### Run the Agent
```bash
uv run python main.py
```

### Test the Integration
```bash
uv run python tests/test_llm_integration.py
```

## How It Works

1. **Conversation Flow**: Guides users through symptom assessment, demographics, and medical history collection
2. **LLM Processing**: Uses Gemini to extract structured data from natural language input
3. **Clinical Assessment**: Applies evidence-based UTI criteria and safety checks
4. **Response Generation**: Provides empathetic, clear treatment recommendations or referrals
5. **Fallback Mode**: Works without LLM using basic keyword matching if API unavailable

## Clinical Logic

The agent implements standard UTI assessment criteria:
- **Symptom Assessment**: Acute dysuria OR 2+ qualifying symptoms
- **Exclusion Screening**: Male patients, pregnancy, age <12, immunocompromised
- **Treatment Selection**: Nitrofurantoin first-line, alternatives for allergies
- **Safety Mechanisms**: Default referral for complications or uncertainty

## Development

### Running Tests
```bash
uv run python tests/test_llm_integration.py
```

### Adding New Features
The modular architecture allows easy extension:
- Add new extraction patterns in `input_parser.py`
- Extend clinical rules in `clinical_engine.py`  
- Customize responses in `response_gen.py`

## Safety & Disclaimers

- This tool is for guidance only and does not replace professional medical advice
- All complex or uncertain cases default to healthcare provider referral
- Built-in safety checks prevent inappropriate self-treatment recommendations
- Session logging enables clinical review and quality improvement