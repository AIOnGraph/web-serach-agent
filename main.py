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


if query:
    st.title("News Artical")
    with st.spinner("Generating Artical..."):
        response = st.write_stream(NewsGenerator().run(query,st.session_state.prompt))
