import streamlit as st
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from news_generator import NewsGenerator

st.title('Web Search Agent')

if "prompt" not in st.session_state:
    st.session_state.prompt = ChatPromptTemplate(
        messages=[
                SystemMessagePromptTemplate.from_template(
                    """
                        You are a helpful assistant. 
                        You will summarize the provided news content.
                        You will never provide any url or website in response,like PEOPLE.com,glamour.com etc.
                        Always use the user's memory while giving the answer, as the user's chat history is saved. If the user asks about a previous question, give them the correct answer based on the memory.
                        Strictly follow these guidelines. 
                        News Content: {news_content} 
                        Memory: {memory}
                        Helpful Answer:
                    """
                ),
                HumanMessagePromptTemplate.from_template("{news_content},")
            ],input_variables=["news_content","memory"])

if "Memory" not in st.session_state:
    st.session_state.Memory = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "Hi human!,How can I help you today?"}]

for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if query := st.chat_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        news_generator = NewsGenerator()
        response = st.write_stream(news_generator.run(query,st.session_state.prompt,st.session_state.Memory))
        st.session_state.messages.append({"role": "assistant", "content": response })
        st.session_state.Memory.append({"inputs": query,"output": response})