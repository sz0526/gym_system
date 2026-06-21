from rag import rag_chat

while True:

    question = input("用户：")

    if question.lower() == "exit":
        break

    answer = rag_chat(question)

    print("\nAI：")
    print(answer)
    print()