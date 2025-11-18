import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Interfaz con Gemini",
    page_icon="✨",
    layout="centered"
)

# --------------------------
# CSS PERSONALIZADO
# --------------------------
custom_css = """
<style>
body {
    background: radial-gradient(circle at top, #1e1b4b 0%, #020617 60%, #000 100%);
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
}

.main {
    padding-top: 40px;
}

.title {
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(120deg, #a855f7, #22d3ee, #facc15);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
}

.description {
    font-size: 1rem;
    color: #cbd5e1;
    text-align: center;
    margin-bottom: 30px;
}

.prompt-label {
    font-weight: 600;
    margin-bottom: 6px;
}

.prompt-box textarea {
    background-color: rgba(15, 23, 42, 0.85) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(148, 163, 184, 0.5) !important;
    color: #e5e7eb !important;
    font-size: 1rem !important;
}

.response-box {
    margin-top: 25px;
    padding: 20px;
    background-color: rgba(15, 23, 42, 0.8);
    border-radius: 18px;
    border: 1px solid rgba(148, 163, 184, 0.4);
    font-size: 1rem;
    line-height: 1.5;
}

.footer {
    margin-top: 40px;
    text-align: center;
    color: #64748b;
    font-size: 0.8rem;
}

.stButton>button {
    background: linear-gradient(120deg, #6366f1, #06b6d4);
    padding: 10px 24px;
    color: white;
    border: none;
    border-radius: 999px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s ease;
}

.stButton>button:hover {
    opacity: 0.9;
    transform: translateY(-2px);
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --------------------------
# CONFIGURAR GEMINI
# --------------------------
if not API_KEY:
    st.error("⚠️ No se encontró GEMINI_API_KEY. Configúrala en un archivo .env (local) o en los Secrets de Streamlit Cloud.")
else:
    genai.configure(api_key=API_KEY)

    # --------------------------
    # UI
    # --------------------------
    st.markdown('<div class="title">Interfaz con Gemini · Streamlit</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="description">Escribe un prompt, envíalo al modelo y observa cómo responde. '
        'Piensa esta app como un pequeño laboratorio de interacción con un LLM.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="prompt-label">Escribe tu prompt</div>', unsafe_allow_html=True)
    user_prompt = st.text_area(
        label="",
        placeholder="Por ejemplo: Explícame qué es la arquitectura Transformer con una metáfora sencilla...",
        height=140,
        key="prompt_area"
    )

    col1, col2 = st.columns([1, 1.2])
    with col1:
        enviar = st.button("Enviar a Gemini")

    with col2:
        modo = st.selectbox(
            "Modo de respuesta",
            ["Explicación clara", "Tono académico", "Tono creativo"],
            index=0
        )

    if enviar and user_prompt.strip():
        # Ajustar el prompt según el modo elegido (un pequeño plus creativo)
        if modo == "Explicación clara":
            final_prompt = f"Explica esto de forma sencilla y clara, como a un estudiante: {user_prompt}"
        elif modo == "Tono académico":
            final_prompt = f"Responde con un tono más académico, organizado en párrafos: {user_prompt}"
        else:
            final_prompt = f"Responde con un tono creativo, usando metáforas pero siendo comprensible: {user_prompt}"

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            with st.spinner("Generando respuesta..."):
                result = model.generate_content(final_prompt)

            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.write(result.text)
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error al llamar a Gemini: {e}")

    st.markdown('<div class="footer">Asignación #11 — Interfaz de IA · 2025</div>', unsafe_allow_html=True)
