from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
import retriever
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
#Test
def get_response(user_query):
    context = retriever.retrieve_from_pinecone(user_query)[:5]
    print(context)
    st.session_state.context_log = [context]
    
    llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0) #Prev: llama3
    
    template = """
        Answer the question below according to your knowledge in a way that will be helpful to students asking the question.
        The following context is your only source of knowledge to answer from.
        Context: {context}
        User question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "context": context,
        "user_question": user_query
    })



# Example questions
example_questions = [
    "Provide information about SIS as indicated by the glossary.",
    "Explain what the FDSN codes are.",
    "What are examples of datums?",
    "Summarize the information about epochs as provided by the glossary.",
    "What are logger boards and modules?",
    "What are the different equipment categories?",
    "Elaborate on ew2moledb.",
    "Is Mole the subsystem used for Earthworm modules?",
    "How is Earthworm related to SIS?, based on the documentation available?",
    "Summarize Earthworm."
]


st.set_page_config(page_title="Seismolab Assistant Chat", page_icon="🤖")
st.title("Seismolab Assistant Chat")

# # Add examples in an expandable section
# with st.expander("💡 Example Questions"):
#     for question in example_questions:
#         if st.button(question):
#             user_query = question  # Automatically fill the input box with the example question


# Add examples in an expandable section
with st.expander("💡 Example Questions"):
    for question in example_questions:
        if st.button(question):
            st.session_state.user_query = question  # Set the example question when clicked

# Check if there's an existing user_query in session_state, if not, set a default empty value
if "user_query" not in st.session_state:
    st.session_state.user_query = ""


if "context_log" not in st.session_state:
    st.session_state.context_log = ["Retrieved context will be displayed here"]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Hi, I'm a Caltech Seismolab assistant. Ask questions about Caltech Seismolab terminology")]
result = st.toggle("Toggle Context")
if result:
    st.write(st.session_state.context_log)


for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# Automatically populate the chat input box with the user_query from session_state
# user_query = st.chat_input("Type your message here...", value=st.session_state.user_query)
# user_query = st.chat_input("Type your message here...")

# Use st.text_input to allow pre-filling the input box with the user_query
user_query = st.text_input("Type your message here...", value=st.session_state.user_query)


if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query))
    
    st.session_state.chat_history.append(AIMessage(content=response))





# import streamlit as st
# from langchain_community.chat_models import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import AIMessage, HumanMessage
# import retriever
# import warnings
# warnings.filterwarnings('ignore')

# def get_response(user_query):
#     context = retriever.retrieve_from_pinecone(user_query)[:5]
#     st.session_state.context_log = [context]
    
#     llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
    
#     template = """
#         Answer the question below according to your knowledge in a way that will be helpful to students asking the question.
#         The following context is your only source of knowledge to answer from.
#         Context: {context}
#         User question: {user_question}
#     """
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | llm | StrOutputParser()
    
#     return chain.stream({
#         "context": context,
#         "user_question": user_query
#     })

# # Example questions
# example_questions = [
#     "Provide information about SIS as indicated by the glossary.",
#     "Explain what the FDSN codes are.",
#     "What are examples of datums?",
#     "Summarize the information about epochs as provided by the glossary.",
#     "What are logger boards and modules?",
#     "What are the different equipment categories?",
#     "Elaborate on ew2moledb.",
#     "Is Mole the subsystem used for Earthworm modules?",
#     "How is Earthworm related to SIS?",
#     "Summarize Earthworm."
# ]

# st.set_page_config(page_title="Seismolab Assistant Chat", page_icon="🤖")
# st.title("PDF Chat")

# # CSS to make the chat history scrollable and the input area fixed at the bottom
# st.markdown(
#     """
#     <style>
#     /* Make chat history take up available space and be scrollable */
#     .chat-history {
#         height: calc(100vh - 140px);
#         overflow-y: auto;
#         padding-bottom: 20px;
#     }
#     /* Fix the input area to the bottom */
#     .chat-input {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         width: 100%;
#         background-color: white;
#         padding: 10px;
#         box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Expandable section for example questions
# with st.expander("💡 Example Questions"):
#     for question in example_questions:
#         if st.button(question):
#             st.session_state.user_query = question  # Save the example question in session state

# # Initialize session state variables if they don't exist
# if "user_query" not in st.session_state:
#     st.session_state.user_query = ""
# if "context_log" not in st.session_state:
#     st.session_state.context_log = ["Retrieved context will be displayed here"]
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = [
#         AIMessage(content="Hi, I'm a Caltech Seismolab assistant. Ask questions about Caltech Seismolab terminology")
#     ]

# # Container for chat history (apply our custom CSS class)
# chat_container = st.container()
# with chat_container:
#     st.markdown('<div class="chat-history">', unsafe_allow_html=True)
#     for message in st.session_state.chat_history:
#         if isinstance(message, AIMessage):
#             with st.chat_message("AI"):
#                 st.write(message.content)
#         elif isinstance(message, HumanMessage):
#             with st.chat_message("Human"):
#                 st.write(message.content)
#     st.markdown('</div>', unsafe_allow_html=True)

# # Fixed input area container
# st.markdown('<div class="chat-input">', unsafe_allow_html=True)
# # Using a text_input here so we can pre-fill from session_state
# user_query = st.text_input("Type your message here...", value=st.session_state.user_query, key="chat_input_box")
# st.markdown('</div>', unsafe_allow_html=True)

# # When the user submits text (presses Enter in the text_input)
# if user_query and user_query != "":
#     st.session_state.chat_history.append(HumanMessage(content=user_query))
    
#     with st.chat_message("Human"):
#         st.markdown(user_query)
    
#     with st.chat_message("AI"):
#         response = st.write_stream(get_response(user_query))
    
#     st.session_state.chat_history.append(AIMessage(content=response))