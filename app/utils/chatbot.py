import streamlit as st
from collections import defaultdict
from transformers import pipeline
from langchain_core.messages import AIMessage, HumanMessage


@st.cache_resource(show_spinner=False)
def get_cached_model():
    """
    Load and cache the Hugging Face text-generation pipeline for distilgpt2.
    """
    return pipeline('text-generation', model='distilgpt2')

def get_response(question, chat_history, vectordb):
    """
    Generate a response to the user's question based on the chat history and vector database

    Parameters:
    - question (str): The user's question
    - chat_history (list): List of previous chat messages
    - vectordb: Vector database used for context retrieval

    Returns:
    - response: The generated response
    - context: The context associated with the response
    """
    # Retrieve relevant context from vectordb
    context_docs = vectordb.similarity_search(question, k=3) if vectordb else []
    context = ' '.join([doc.page_content for doc in context_docs])
    # Truncate context to avoid exceeding model input limit (distilgpt2: 512 tokens ~ 400 chars)
    max_context_length = 400
    context = context[:max_context_length]
    prompt = f"Context: {context}\nQuestion: {question}"
    llm = get_cached_model()
    result = llm(prompt)
    answer = result[0]['generated_text'] if result and 'generated_text' in result[0] else str(result)
    return answer, context_docs

def chat(chat_history, vectordb):
    """
    Handle the chat functionality of the application

    Parameters:
    - chat_history (list): List of previous chat messages
    - vectordb: Vector database used for context retrieval

    Returns:
    - chat_history: Updated chat history
    """
    user_query = st.chat_input("Ask a question:")
    if user_query is not None and user_query != "":
        # Generate response based on user's query, chat history and vectorstore
        response, context = get_response(user_query, chat_history, vectordb)
        # Update chat history. The model uses up to 10 previous messages to incorporate into the response
        chat_history = chat_history + [HumanMessage(content=user_query), AIMessage(content=response)]
        # Display source of the response on sidebar
        with st.sidebar:
                metadata_dict = defaultdict(list)
                for metadata in [doc.metadata for doc in context]:
                    metadata_dict[metadata['source']].append(metadata['page'])
                for source, pages in metadata_dict.items():
                    st.write(f"Source: {source}")
                    st.write(f"Pages: {', '.join(map(str, pages))}")
    # Display chat history
    for message in chat_history:
            with st.chat_message("AI" if isinstance(message, AIMessage) else "Human"):
                st.write(message.content)
    return chat_history
