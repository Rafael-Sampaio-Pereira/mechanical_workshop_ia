from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from pyfiglet import Figlet

f = Figlet(font="slant")


model = OllamaLLM(model="llama3.2")

template = """
You are an exeprt in answering questions about Mechanical Workshop

Here are some relevant diagnostics: {diagnostics}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\033[1;32m")
    print(f.renderText("Workshop IA Agent 1.0"))
    print("\033[0m")
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    diagnostics = retriever.invoke(question)
    result = chain.invoke({"diagnostics": diagnostics, "question": question})
    print(result)


"""
Without RAG data (Our selves context data) the IA model will hallucinate and answer anything in random mode
"""