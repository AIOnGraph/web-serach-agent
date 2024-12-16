import streamlit as st
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from news_generator import NewsGenerator


with st.sidebar:
    st.title('Web Search Agent')
    st.markdown('''
    ## About
    This app is an LLM-powered web search agent that can search the web for news articles and generate the news articles.
    ''')
    query = st.text_input("Enter the news title: ")

if "prompt" not in st.session_state:
    st.session_state.prompt = ChatPromptTemplate(
        messages=[
                SystemMessagePromptTemplate.from_template(
                    """
                You are an expert news article writer tasked with creating a well-structured, engaging article based on the following guidelines:

                    Create a news article with the following:
                    	1.	Headline: Engaging and descriptive.
                    	2.	Intro: Concise hook summarizing the content.
                    	3.	Body: Clear sections, context, facts, and quotes.
                    	4.	Tone: Professional, accurate, objective.
                    	5.	Conclusion: Meaningful summary or implications.
                    
                    Sources:
                    	•	Content: {news_content}
                    	•	URL: {news_url}
                    Output Format:
                    - Headline: [Engaging, Descriptive Headline]

                    [Structured Article Content]

                    ---
                    Original Source: 
                        [If news urls]
                        - url1
                        - url2
                        [...continue the rest]


                    """
                ),
                HumanMessagePromptTemplate.from_template("{news_content},{news_url}")
            ],input_variables=["news_content","news_url"])

# if "Memory" not in st.session_state:
#     st.session_state.Memory = []

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = [{"role": "assistant", "content": "Hi human!,How can I help you today?"}]

# for message in st.session_state.messages:
#     if message["role"] == 'assistant':
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
#     else:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

if query:
    st.title("News Artical")
    with st.spinner("Generating Artical..."):
        response = st.write_stream(NewsGenerator().run(query,st.session_state.prompt))

# if query := st.chat_input("Ask me anything"):
#     st.session_state.messages.append({"role": "user", "content": query})
#     with st.chat_message("user"):
#         st.markdown(query)
    
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         news_generator = NewsGenerator()
#         response = st.write_stream(news_generator.run(query,st.session_state.prompt))
#         st.session_state.messages.append({"role": "assistant", "content": response })
