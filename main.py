import streamlit as st
import google.generativeai as genai


# Configuração da API Key e Modelo (conforme solicitado)
api_key = "AIzaSyBYRDMl2DuZmJ-m1jfrj2UBlmvDTEJlW6g" 
genai.configure(api_key=api_key)

try:
    # Utilizando o modelo especificado
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Erro ao carregar o modelo Gemini 'gemini-2.0-flash': {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele.")
    st.stop()

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'): # Tenta obter mais detalhes do erro da API do Gemini
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None

# Título do aplicativo
st.title("Criador de Histórias Interativas")
st.markdown("Crie sua história utilizando IA generativa de texto")


# Entradas do usuário
protagonista = st.text_input("Qual nome do Protagonista?")

genero_literario = ["Fantasia", "Ficção Científica", "Mistério", "Aventura", "Dark Fantasy"]
genero_escolhido = st.selectbox("Escolha o gênero literário", genero_literario)

local_inicio = st.radio(
    "Qual local você gostaria de iniciar?",
    ["Uma floresta antiga", "Uma cidade futurista", "Uma delegacia", "Uma montanha", "Um castelo assombrado"]
)

frase_efeito = st.text_area(
    "Insira uma frase de efeito para o protagonista",
    placeholder="Ex: E de repente, tudo ficou escuro. ou O mapa indicava um perigo iminente."
)

if st.button("Gerar Início da História"):
    if not protagonista:
        st.warning("Por favor, informe o nome do protagonista.")
    elif not genero_escolhido:
        st.warning("Por favor, selecione pelo menos um genero para a história.")
    else:
        interesses_str = ", ".join(genero_escolhido)

        prompt_aluno = (
            f"Preciso de ajuda para criar uma história. O nome do protagonista é {protagonista}.\n"
            f"O gênero da história será {interesses_str}.\n"
            f"A história começará em {local_inicio}.\n"
            f"E o protagonista terá uma frase de efeito, que será: {frase_efeito}.\n"
            f"Com base nessas informações, por favor, crie uma história. "
            f"Apresente a resposta de forma organizada."
        )

        st.markdown("---")
        st.markdown("⚙️ **Prompt que será enviado para a IA (para fins de aprendizado):**")
        st.text_area("",prompt_aluno, height=250)
        st.markdown("---")

        st.info("Aguarde, a IA está montando seu roteiro dos sonhos...")
        resposta_ia = gerar_resposta_gemini(prompt_aluno)

        if resposta_ia:
            st.markdown("### ✨ Sugestão de Roteiro da IA:")
            st.markdown(resposta_ia)
        else:
            st.error("Não foi possível gerar o roteiro. Verifique as mensagens acima ou tente novamente mais tarde.")