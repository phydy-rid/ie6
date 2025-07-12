#retrieve imports
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

from get_embedding_function import get_embedding_function


def retrieve_context(query_text):
    CHROMA_PATH = "chroma"
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function) #deben haber instalado chromaDB y creado la BD con vectorDB.py antes. El vectorDB-llamaIndex crea una VDB pero con lalamIndex y creo que no al pude conectar finalmente, no se que tan bien funcione

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)
    return results

def generate_prompt(query, context):
    prompt = f"Vous êtes un assistant de travail pour la TEST TIENEN QUE CAMBIAR ESTO, vous êtes donc spécialisé dans ce domaine et vous êtes prêt à répondre à toutes les questions. Votre tâche consiste à répondre à la question posée entre les balises <Question></Question> en vous basant sur le contexte fourni entre les balises <Contexte></Contexte>. Fournissez des réponses avec des phrases complètes et détaillées mais concis, sans contourner le sujet. Si vous ne trouvez pas la réponse dans le contexte, vous pouvez dire que vous n'avez pas la réponse à cette question ; n'inventez pas de réponse : \n\n<Question>{query}</Question>\n\n"
    
    for i, ctx in enumerate(context):
        prompt += f" <Context{i+1}> {ctx[0].page_content}</Context{i+1}>\n\n\n"
    return prompt

def getPremAnswer(
        prompt: str,
        max_tokens: int = 512,
        model_name: str = "gpt-4o-mini"
    ): 
    # 1) Componemos el prompt enriquecido con contexto
    full_prompt = generate_prompt(prompt, retrieve_context(prompt))
    
    # 2) Creamos el LLM de OpenAI
    llm = ChatOpenAI(
        model_name=model_name,
        max_tokens=max_tokens,
        #pasar la clave directamente:
        openai_api_key=""
    )
    
    # 3) Obtenemos la respuesta
    answer = llm.invoke(full_prompt)
    
    return answer
