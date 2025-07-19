import streamlit as st
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ.pop("SSL_CERT_FILE", None)

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector2(collection='recipes', db_url=db_url)
)
knowledge_base.load()


storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)


st.set_page_config(page_title="🍜 Thai Recipe Assistant", layout="wide")

st.title("🍜 Thai Recipe Assistant")
st.markdown("Ask anything about Thai recipes from the uploaded PDF!")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "run_id" not in st.session_state:
    user = "user"
    existing_run_ids = storage.get_all_run_ids(user)
    if len(existing_run_ids) > 0:
        st.session_state.run_id = existing_run_ids[0]
    else:
        st.session_state.run_id = None

assistant = Assistant(
    run_id=st.session_state.run_id,
    user_id="user",
    knowledge_base=knowledge_base,
    storage=storage,
    show_tool_calls=True,
    search_knowledge=True,
    read_chat_history=True,
)

if st.session_state.run_id is None:
    st.session_state.run_id = assistant.run_id
    st.success(f"Started new chat session! 🆕 (Run ID: {assistant.run_id})")
else:
    st.info(f"Resumed chat session (Run ID: {assistant.run_id})")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Ask about Thai Recipes..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = assistant.run(prompt)
    full_response = "".join(chunk for chunk in response)

    st.chat_message("assistant").markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})



if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.session_state.run_id = None
    st.experimental_rerun()

st.sidebar.markdown("Made with ❤️ using [phi](https://github.com/nostr-ai/phi)")
