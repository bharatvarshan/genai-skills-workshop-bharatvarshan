# Alaska Snow Department AI Assistant

An AI assistant built for the Alaska Department of Snow, leveraging advanced RAG (Retrieval-Augmented Generation) technology. This solution combines robust safety measures with powerful backend API integration, implemented in Python with a Streamlit interface and deployed on Google Cloud Platform.

## Key Features

- **Intelligent Response Generation**: Advanced RAG implementation for context-aware responses
- **Safety First**: Multi-layer prompt filtering with LLM-based safety checks
- **Quality Assurance**: Comprehensive evaluation metrics using Google's Evaluation API
- **Robust Testing**: Complete test suite covering core functionality
- **Modern Interface**: Clean and intuitive Streamlit-based user interface
- **Cloud-Ready**: Optimized for GCP Cloud Run deployment

## Architecture

```
.
├── app/                    # Core application code
│   ├── backend.py         # Core response generation and RAG implementation
│   ├── filters.py         # Safety and content filtering mechanisms
│   └── __init__.py
├── ui/                    # User interface components
│   └── main.py           # Streamlit-based user interface
├── test/                  # Test suite
│   ├── test_backend_agent.py  # Backend functionality tests
│   └── test_filters.py       # Safety filter validation tests
├── output/               # Output and evaluation results
├── rag-embedding/        # RAG implementation and embeddings
├── .streamlit/          # Streamlit configuration
├── settings.py          # Environment and configuration management
├── requirements.txt     # Project dependencies
├── DockerFile          # Container configuration for GCP deployment
├── .gitignore          # Git ignore rules
└── Conceptual_Architecture.png  # System architecture diagram
```



## Getting Started

### Local Development

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run ui/main.py
```

### Cloud Deployment

Build and deploy to GCP Cloud Run:

```bash
# Build container
gcloud builds submit --tag gcr.io/[PROJECT-ID]/streamlit-app

# Deploy to Cloud Run
gcloud run deploy streamlit-app --image gcr.io/[PROJECT-ID]/streamlit-app --platform managed
```

## Performance Evaluation

The system implements comprehensive evaluation metrics including:
- Response fluency assessment
- Content relevance scoring
- BLEU score analysis
- Additional text quality metrics

## Security Implementation

- Multi-stage prompt validation
- LLM-based content filtering
- Automated safety checks
- Response blocking for flagged content

## Data Integration

The system utilizes data from:
```
gs://labs.roitraining.com/alaska-dept-of-snow
```

Data processing and storage is managed through BigQuery, with the RAG datastore configured via `rag-embedding/load_embedding_bigquery_from_gs.ipynb`.

## Testing

Run the complete test suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Evaluation metrics for test cases are available in the `outputs` directory.

