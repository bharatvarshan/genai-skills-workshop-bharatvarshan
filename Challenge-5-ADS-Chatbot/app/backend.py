import os
from google.cloud import bigquery
from vertexai.preview.generative_models import GenerativeModel, SafetySetting
from config import TABLE_ID, EMBED_MODEL_ID, PROJECT_ID

# Set credentials (optional if GOOGLE_APPLICATION_CREDENTIALS is already set)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "qwiklabs-gcp-03-be6b72ae4b0d-fb64442a0a9f.json")
system_instruction = "You are a helpful assistant for the town of Alaska Snow Department. Be polite, concise, and avoid speculation."

bq_client = bigquery.Client(project=PROJECT_ID)
chat_model = GenerativeModel(
    model_name="gemini-2.0-flash-001",
    system_instruction=system_instruction,
    safety_settings=[
        SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"),
        SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
        SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_LOW_AND_ABOVE"),
        SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_LOW_AND_ABOVE"),
    ]
)


def fetch_faq_results(user_question):
    """
    1. This function queries the BigQuery table that stores VECTOR_SEARCH results.
    2. It filters results by the current user question and returns top 3 most relevant rows
    """
    try:
        query = f"""
        SELECT
        query.query,
        result.base.question,
        result.base.answer,
        result.distance
        FROM VECTOR_SEARCH(
        TABLE `{TABLE_ID}`,
        'embedding',
        (
            SELECT
            ml_generate_embedding_result AS embedding,
            '{user_question}' AS query
            FROM ML.GENERATE_EMBEDDING(
            MODEL `{EMBED_MODEL_ID}`,
            (SELECT '{user_question}' AS content)
            )
        ),
        top_k => 3,
        options => '{{"fraction_lists_to_search": 1.0}}'
        ) AS result
        """
        return bq_client.query(query).to_dataframe()
    except Exception as e:
        print("Exception:", e)
        return ""

def generate_bot_response(user_input):
    """
    1. This function uses the Gemini generative model to generate a chatbot response.
    2. It builds a prompt from top FAQ results retrieved from BigQuery.
    3. The Gemini Model has Safety Parameters which verifies the prompt sent by user.
    """
    try:
        results = fetch_faq_results(user_input)
        context = "\n\n".join([f"Q: {row['question']}\nA: {row['answer']}" for _, row in results.iterrows()])
        prompt = f"You are a helpful assistant for the town of Alaska Snow Department. Use the following FAQ context to answer:\n\n{context}\n\nUser: {user_input}"
        response = chat_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return ""
