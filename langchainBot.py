import os
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI


def ask(Question):
  loader = TextLoader('info.txt', encoding="utf-8")
  index = VectorstoreIndexCreator().from_loaders([loader])
  messages = """[Maestro]Tu eres un experto en servicio al cliente. respondes con respuestas claras concisas, si el cliente quiere implementar un chatbot nuestro correo es sebastian@infobots.cl"""
  messages = f"{messages}, User: {Question}"
  return index.query(
      messages,
      llm=ChatOpenAI(),
  )
