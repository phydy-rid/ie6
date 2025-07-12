import streamlit as st
import time
from get_embedding_function import get_embedding_function
from prem_rag import getPremAnswer


# Título de la aplicación
st.set_page_config(page_title="Chatbot Test")


# Configuración de la barra lateral
with st.sidebar:
    # Título de bienvenida en la barra lateral
    st.title('Bienvenido al Chatbot del colegio 🦙')
    
    # Controles deslizantes para ajustar parámetros del modelo
    # Temperatura: controla la creatividad de las respuestas
    temperature = st.sidebar.slider('Temperatura', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    
    # Top_p: controla la diversidad del muestreo
    top_p = st.sidebar.slider('Top p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    
    # Longitud máxima: controla el tamaño de las respuestas generadas
    max_length = st.sidebar.slider('Longitud maxima', min_value=64, max_value=4096, value=512, step=8)
    

# Inicializa el historial de mensajes si no existe
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": 'Como te puedo ayudar hoy ?'}]

# Mostrar mensajes del chat existentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Función para limpiar el historial del chat
def clear_chat_history():
    st.session_state.messages = [{"role": "developer", "content": "Eres un asistente útil para unos estudiantes de colegio en Colombia."}, {"role": "assistant", "content": "Como te puedo ayudar hoy ?"}]

# Botón para limpiar el historial
st.sidebar.button('Limpiar el historial', on_click=clear_chat_history)

# Entrada de texto proporcionada por el usuario
if prompt := st.chat_input():
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mostrar mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.write(prompt)

# Generar una nueva respuesta si el último mensaje no es del asistente
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        # Mostrar indicador de carga mientras se genera la respuesta
        with st.spinner("Pera, pera, yo sé, yo sé...🤔"):
            # Simular tiempo de respuesta
            time.sleep(5)
            # Llamada a ChatGPT
            response = getPremAnswer(prompt)
            response = response.content
            
            # Crear un efecto de escritura letra por letra
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    
    # Añadir respuesta del asistente al historial
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

