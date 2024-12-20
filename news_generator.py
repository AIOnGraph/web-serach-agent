from langchain_groq.chat_models import ChatGroq
from openai import AuthenticationError
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import os
import time
from langchain_community.tools import TavilySearchResults
import streamlit as st

class NewsGenerator:
    def __init__(self):
        """
        Initializes the GlamourFashionNewsBot with the necessary API keys, search tools, and prompt templates.
        """
        self.news_content = []
        self.news_url = []
        self.llm = ChatGroq(
            api_key=st.secrets['GROQ_API_KEY'],
            model="llama3-70b-8192",
            temperature=0,
            max_retries=2,
            streaming=True,
            verbose=True
        )
        self.search_tool = TavilySearchResults(search_depth="advanced",verbose=True, description="Glamour and fashion",max_results=10)

    def fetch_news_articles(self,news):
        """
        Fetches the news articles related to glamour and fashion celebrities, extracting the content.

        Returns:
            bool: True if the operation completes successfully.
        """
        news_result = self.search_tool.invoke({'query': news})
        for news in news_result:
            self.news_content.append(news['content'])
            self.news_url.append(news['url'])
        return True

    def generate_news_summary(self, user_question, prompt):
        """
        Generates a news summary related to glamour and fashion using the ChatGroq model.

        Parameters:
            user_question (str): The user's question or request for news.

        Yields:
            str: Chunks of the AI-generated news summary.
        """
        try:
            chain = (prompt | self.llm)
            output = ""
            for chunk in chain.stream({"question": user_question, 'news_content': self.news_content,"news_url":self.news_url}):
                output += chunk.content
                yield chunk.content
                time.sleep(0.05)
        except AuthenticationError:
            return 'AuthenticationError'
    def run(self, question,prompt):
        """
        Runs the bot to fetch news articles and generate a news summary.

        Parameters:
            question (str): The user's question or request for news.
        """
        self.fetch_news_articles(question)
        news_summary = self.generate_news_summary(question,prompt)
        return news_summary

if __name__ == "__main__":
    bot = NewsGenerator()
    news = input("Enter the news title: ")
    news = bot.run(news)