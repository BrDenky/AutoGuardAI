import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(
    page_title="Chatbot AutoGuardAI",
    layout="wide"
)
st.title("Chatbot – AutoGuardAI")


api_key_input = st.text_input(
    "Introduce tu OpenAI API Key:",
    type="password",
    placeholder="sk-xxxxx..."
)
if api_key_input:
    st.session_state["OPENAI_API_KEY"] = api_key_input
    st.success("API Key guardada correctamente.")
else:
    st.warning("⚠️ Debes ingresar tu API Key para usar el chatbot.")
if "OPENAI_API_KEY" in st.session_state:
    client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
else:
    client = None
#client = OpenAI(api_key=OPENAI_API_KEY)

df = pd.read_csv('customer.csv')

# Parte visual de streamlit
col1, col2 = st.columns([2, 2], gap="large")

with col1:
    st.header("🙍‍♂️ Customer Dataset")
    st.dataframe(df, height=500)
    columnas = df.columns.tolist()

with col2:
    st.header("💬 Chatbot")
    
    # # Verificamos que la pregunta sea válida
    # def pregunta_en_contexto(pregunta, columnas):
    #     pregunta_lower = pregunta.lower()
    #     for col in columnas:
    #         if col.lower() in pregunta_lower:
    #             return True
    #     return False

    def generar_respuesta(pregunta, df):
            # Convertir el dataset en un texto legible
            contexto_tabla = df.to_string(index=False)

            prompt = f"""
        Eres un chatbot experto en analizar datos tabulares.
        Tu conocimiento está limitado EXCLUSIVAMENTE al siguiente dataset de clientes:

        {contexto_tabla}

        INSTRUCCIONES IMPORTANTES:
        - No inventes información.
        - Si la respuesta no puede obtenerse del dataset, responde únicamente:
          "No tengo conocimiento sobre eso. Y propon una segunda pregunta posible con respecto a la información del dataset"
        - Si el usuario pregunta por un nombre, apellido, ciudad, dirección, número de teléfono o correo,
          busca coincidencias dentro del dataset.
        - Si existen varias coincidencias, enuméralas.

        Ahora responde de forma clara y útil a esta pregunta del usuario:

        Pregunta: {pregunta}
        """

            respuesta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0
            )

            return respuesta.choices[0].message.content


    st.subheader("¿Qué necesitas saber hoy?")
    
    pregunta_usuario = st.text_input("Pregunta aquí...", key="pregunta")
    
    if st.button("Enviar pregunta", type="primary"):
        if pregunta_usuario.strip() == "":
            st.warning("Por favor escribe una pregunta.")
        else:
            with st.spinner("Procesando..."):
                respuesta = generar_respuesta(pregunta_usuario, df)
            
            st.write("### Respuesta del AutoGuardAI")
            st.info(respuesta)