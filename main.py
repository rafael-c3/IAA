import streamlit as st
import google.generativeai as genai

# Configura a API key do Gemini corretamente para a versão instalada
genai.configure(api_key="AIzaSyBYRDMl2DuZmJ-m1jfrj2UBlmvDTEJlW6g")

model = genai.GenerativeModel("gemini-2.0-flash")

def gerar_resposta_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"
    
# Interface para o usuário
pergunta = st.text_area("Digite sua pergunta:")

if st.button("Gerar Resposta"):
    if pergunta:
        with st.spinner("Gerando resposta..."):
            resposta = gerar_resposta_gemini(pergunta)
            st.write("**Resposta:**")
            st.write(resposta)
    else:
        st.warning("Por favor, digite uma pergunta.")