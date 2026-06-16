# YatraAI - AI Travel Planner 🧭

An intelligent travel planning application powered by LLMs and machine learning models that creates personalized travel itineraries, budget plans, and local insights.

## Features

- **Smart Trip Planning**: AI-powered itinerary generation based on interests and preferences
- **Budget Analytics**: Intelligent budget allocation across accommodation, food, and activities
- **Accommodation Recommendations**: ML-based hotel and accommodation suggestions
- **Local Insights**: Hidden gems, food spots, and travel hacks powered by LLMs
- **Booking Strategy**: Step-by-step booking guidance for flights, hotels, and activities
- **Weather Intelligence**: Real-time weather forecasts for your destination
- **Interactive Maps**: Visual trip routes and location highlights
- **Model Evaluation**: Performance metrics for ML models (accuracy, MAPE, R² scores)

## Tech Stack

- **Frontend**: Streamlit
- **LLMs**: Google Generative AI (Gemini)
- **ML Framework**: LangGraph, LangChain
- **ML Models**: Scikit-learn (Budget Allocator, Accommodation Recommender)
- **Visualization**: Plotly, Folium, Streamlit
- **Backend**: Python 3.10+

## Project Structure

```
YatraAI/
├── streamlit_app.py              # Main Streamlit app entry point
├── main.py                       # Alternative entry point
├── requirements.txt              # Python dependencies
├── graph.py                      # LangGraph workflow definition
├── state.py                      # Application state management
├── tests.py                      # Test suite
│
├── .streamlit/
│   ├── config.toml              # Streamlit configuration
│   └── secrets.toml             # API keys & secrets (not in git)
│
├── agents/                      # LLM agents
│   ├── accommodation_recommender_ml.py
│   ├── budget_allocator_ml.py
│   ├── booking_strategy_llm.py
│   ├── itinerary_generator_llm.py
│   └── local_insights_llm.py
│
├── ml/                          # Machine learning models
│   ├── models/
│   ├── training/
│   └── evaluation/
│
├── ui/                          # UI components
│   ├── theme.py
│   ├── hero.py
│   ├── chat.py
│   ├── insights.py
│   ├── destinations.py
│   ├── itinerary_cards.py
│   ├── maps.py
│   ├── analytics.py
│   ├── hotels.py
│   └── weather.py
│
├── utils/                       # Utilities
│   └── constants.py
│
├── workflow/                    # Workflow definitions
│
├── data/                        # Data files
│   ├── raw/
│   ├── processed/
│   ├── training_dataset/
│   └── evaluation_dataset/
│
└── .gitignore
```

## Installation

### Local Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd YatraAI
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your-google-api-key-here
```

Or use Streamlit secrets (`.streamlit/secrets.toml`):
```toml
GOOGLE_API_KEY = "your-google-api-key-here"
```

5. **Run locally**
```bash
streamlit run streamlit_app.py
```

## Deployment on Streamlit Cloud Community

### Prerequisites
- GitHub account with the repository pushed
- Google Cloud API key (for Gemini LLM)
- Streamlit Cloud Community account (free tier)

### Step 1: Prepare Your Repository

1. Ensure `streamlit_app.py` is in the root directory ✓
2. Ensure `requirements.txt` is present and up-to-date ✓
3. Add `.gitignore` to exclude sensitive files ✓
4. Create `.streamlit/config.toml` for Streamlit configuration ✓

### Step 2: Add Secrets to Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Deploy your app using the GitHub link
3. Once deployed, go to **App settings** → **Secrets**
4. Add your API keys in the Secrets section:

```toml
GOOGLE_API_KEY = "your-google-api-key-here"
```

**Important**: Never commit API keys or secrets to GitHub. Always add them through the Streamlit Cloud dashboard.

### Step 3: Deploy to Streamlit Cloud

1. Log in to [Streamlit Cloud](https://share.streamlit.io)
2. Click **New app** → Select your GitHub repository
3. Select the branch: `main`
4. Set the main file path: `streamlit_app.py`
5. Click **Deploy**

The app will be live at: `https://[your-username]-[repo-name]-[random-string].streamlit.app`

### Step 4: Manage Secrets

Add your API keys and secrets through the Streamlit Cloud dashboard:

1. Go to your app settings
2. Click on **Secrets** tab
3. Paste your secrets in TOML format
4. The app will automatically reload with the new secrets

Example secrets format:
```toml
GOOGLE_API_KEY = "AIzaSy..."
MODEL_NAME = "gemini-pro"
TEMPERATURE = 0.7
```

## API Keys Required

### Google Generative AI (Required)
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click "Get API key"
3. Create a new API key
4. Copy and add to Streamlit Cloud secrets

### Optional APIs
- OpenWeather API (for weather data)
- Booking.com API (for accommodation data)
- OpenStreetMap/Folium (built-in, no key needed)

## Usage

### For End Users
1. Open the deployed app
2. Use the sidebar to set your preferences:
   - Choose destination
   - Select travel companion type
   - Set budget range and travel style
   - Pick interests and travel season
3. Click "Generate Plan" or chat with Yatra AI
4. Explore tabs: Overview, Budget, Accommodation, Itinerary, Maps, Weather, Insights, Booking

### For Developers

Run tests:
```bash
pytest tests.py
```

Evaluate ML models:
```bash
python -m ml.evaluation.evaluate_models
```

## Performance Considerations

- **Model Loading**: Models are cached in session state to avoid reloading
- **API Calls**: LLM calls are optimized with streaming when possible
- **Data Processing**: CSV datasets are cached using `@st.cache_data`
- **Memory**: Streamlit Cloud Community tier has limits (~1GB RAM)

## Troubleshooting

### "ModuleNotFoundError"
- Ensure all dependencies are in `requirements.txt`
- Check that all Python files are properly organized in modules

### "API Key Not Found"
- Verify the API key is added to Streamlit Cloud Secrets
- Check that the environment variable name matches exactly
- Access secrets in code using: `st.secrets["GOOGLE_API_KEY"]`

### App Running Slowly
- Optimize LLM calls (use streaming, caching)
- Reduce dataset sizes if possible
- Use Streamlit caching decorators (`@st.cache_data`, `@st.cache_resource`)

### Data Not Loading
- Ensure relative paths work (use `__file__` for paths)
- Check that data files are committed to the repository
- For large files, consider using cloud storage (Firebase, S3)

## Monitoring

After deployment, monitor your app:
1. View logs in Streamlit Cloud dashboard
2. Check for errors and exceptions
3. Monitor resource usage (CPU, memory, disk)
4. Set up GitHub Actions for CI/CD if needed

## Limitations of Community Tier

- **Storage**: Limited to what's in the repository
- **Memory**: ~1GB RAM per app instance
- **CPU**: Shared resources
- **Uptime**: Best effort (no SLA)
- **Apps**: Up to 3 concurrent apps
- **Duration**: No limits on app runtime

For production use, consider Streamlit Cloud Pro or other hosting platforms.

## Contributing

1. Create a feature branch
2. Make changes and test locally
3. Commit with clear messages
4. Push and create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the [Streamlit documentation](https://docs.streamlit.io)
2. Review the [GitHub Issues](https://github.com/your-repo/issues)
3. Visit [Streamlit Community Forum](https://discuss.streamlit.io)

## Authors

- **YatraAI Team**

## Changelog

### v1.0.0 (Initial Release)
- Complete travel planning workflow
- ML-based budget allocation and accommodation recommendations
- LLM-powered itinerary and insights generation
- Interactive UI with maps and analytics
- Model evaluation dashboard

---

**Happy Traveling! 🌍✈️**
