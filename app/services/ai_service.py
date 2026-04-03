from datetime import datetime

from ollama import Client, ListResponse, AsyncClient, list
from fastapi import HTTPException
from app.schemas.ai_schemas import ModelParameters, CreateModel, ChatOptions 
from app.services import chroma_service


async def list_models(family: str | None = None):
    response: ListResponse = list()
    if not response.models:
        raise HTTPException(status_code=404, detail="No models found")
    
    families: set[str] = {entry.details.family for entry in response.models}

    if family:
        filtered = [m for m in response.models if m.details.family == family]
        return {"families": families, "models": filtered}
    return {"families": families, "models": response.models}


async def create_new_model(model: CreateModel):
    model.new_model_name = model.new_model_name or f"{model.selected_model}-assistant"
    model.system_prompt = model.system_prompt or f"You are my personal assistant"

    if model_exists(model.new_model_name):
        return {"message":"model name already exists"}
    
    client = Client()
    response = client.create(
      model=model.new_model_name,
      from_=model.selected_model,
      system=model.system_prompt,
      stream=False,
    )
    return response.status

def model_exists(name: str):    
    response: ListResponse = list()    
    return any(f.model == name for f in response.models)

async def get_streaming_model_answer(parameters: ModelParameters):
    client = AsyncClient()
    response = await client.generate(
        parameters.model_name, 
        parameters.prompt, 
        stream=True,
        options=parameters.options.to_dict()
    )
    async for chunk in response:
        yield chunk['response']

async def get_model_answer(parameters: ModelParameters):
    client = AsyncClient()

    response = await client.chat(
        parameters.model_name, 
        messages=[{"role": "assistant", "content": parameters.prompt}],
        options=parameters.options.to_dict()
        )

    return response

async def get_personal_model_answer(chroma_client, user_query: str):
    chroma_response = await chroma_service.get_collection_entry(chroma_client, user_query)
    
    model_prompt = prepare_personal_model_prompt(chroma_response, user_query)

    ai_response = await get_model_answer(ModelParameters(
        model_name="gemma3:4b-it-q8_0",
        prompt=model_prompt,
        options=ChatOptions(
            max_tokens=500,
            temperature=0.2,
            top_p=0.9
        )
    ))   

    return {"question": user_query, "response": ai_response['message']['content'], "created_at": ai_response['created_at']}

def prepare_personal_model_prompt(response, query: str = ""):
    result = response  # obiectul tău

    text = []
    
    [text.append(f"- [Time]: ({human_readable_time(metadata['timestamp'])}) - [INFO]: ({document})")
    for metadata, document, distance in zip(
        result["metadatas"][0],
        result["documents"][0],
        result["distances"][0],
    )]
    
    entries_text = "\n".join(text)

    prompt = f"""
    System:
    You are a precise assistant. Use ONLY the provided informations.
    For any time-related questions, use the current date and time: {human_readable_time(datetime.now().isoformat())}.
    All dates in your answers must be written in the format: day month year
    Write all answers addressing the user directly (e.g., instead of "Am lucrat la cod", write "Ai lucrat la cod").
    The relevant informations (list of informations) are written in this format [Time]: (the time of recording) - [INFO]: (the information)
    You must take into consideration the Entry and the Time

    Relevant informations (list of informations):
    {entries_text}
    --- END OF RELEVANT MEMORIES ---
    
    Instructions:
    - Treat each item above as a separate event.
    - Only use information that explicitly mention the topic asked in the question
    - Use information from multiple relevant informations if necessary.
    - If more than one information relates to the question, combine the informations into a single coherent answer.
    - Reference the exact informations entries details.
    - Do not invent new information or dates.
    - Focus on the most relevant informations.
    Question: 
    {query} 
    Answer:
    """
    return prompt

def human_readable_time(iso_time_str: str):
    return datetime.fromisoformat(iso_time_str).strftime("%#d %B %Y %H:%M:%S")
