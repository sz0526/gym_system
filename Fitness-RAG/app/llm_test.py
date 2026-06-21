from llm import get_llm

llm = get_llm()

response = llm.invoke("你好，请介绍一下你自己。")

print(response.content)