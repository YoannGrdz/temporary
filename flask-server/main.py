import os
import sys
from openAI_api_key import openAI_api_key
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

#Importing the datasource dictionary containing chunks of data to be used for RAG 
from prompts import dataSource

#Main system prompt
from prompts import mainSystemPromptDescription

# Retrieval Augmented Generation Decision Orchester for Langchain System Prompt
from prompts import RAGDOL_sp

os.environ["OPENAI_API_KEY"] = openAI_api_key


context = ""
instructions = mainSystemPromptDescription

#Main chat system prompt
mainSystemPrompt = f"""
    {instructions}
    {context}
"""


#LLM models and chat histories
RAGDOLchat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-4',
    temperature=0
)

RAGDOLchatMessages = [
    # the system prompt
    SystemMessage(content=RAGDOL_sp)
]


MainChat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-4',
    temperature=1
)

MainChatMessages = [
    # the system prompt
    SystemMessage(content=instructions)
]

# conversation flow
query = None

print("")

while True:

    #Reseting the main system prompt and the context
    context = None
    mainSystemPrompt = f"""
        {instructions}
        {context}
    """
    MainChatMessages[0] = SystemMessage(content=mainSystemPrompt)

    # Asking user for input
    if not query:
        query = input("Prompt: ")

    # Exiting the program if the user inputs one of the following
    if query in ['quit', 'q', 'exit']:
        sys.exit()

    # The query is added to the messages object
    userQuery = HumanMessage(content=query)
    RAGDOLchatMessages.append(userQuery)
    # the RAGDOL bot is returning the appropriate action
    decision = RAGDOLchat(RAGDOLchatMessages).content
    print("action:", decision)


    #In case no document is necessary to answer the query, we just pass the query to the main chatbot without the need to augment the system prompt
    if decision == "answerUser":
        print("\n")
        
    #In case a document is necessary, we retrieve the correct one and write its content in the context string
    ##Todo: Make it so that we dynamically generate the link with the RAGDOL system prompt instead of using this long if statement
    context = dataSource[decision]


    #Updating context in the main system prompt by redeclaring it
    mainSystemPrompt = f"""
        {instructions}
        {context}
    """
    #Updating the main system prompt in the chat history
    MainChatMessages[0] = SystemMessage(content=mainSystemPrompt)

    MainChatMessages.append(userQuery)
    answer = MainChat(MainChatMessages)
    MainChatMessages.append(AIMessage(content=answer.content))
    print(answer.content)

    query = None
