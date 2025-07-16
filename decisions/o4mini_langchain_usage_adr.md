# ADR: Using o4-mini-2025-04-16 with LangChain

## Context
OpenAI released o4-mini as a fast reasoning model optimized for coding and visual tasks. The [model page](https://platform.openai.com/docs/models/o4-mini) describes it as "our latest small o-series model" with a 200k context window and a snapshot named `o4-mini-2025-04-16`. The [April 16, 2025 release notes](https://platform.openai.com/docs/changelog) introduced both o3 and o4-mini reasoning models. The official [blog post](https://openai.com/index/introducing-o3-and-o4-mini/) highlights their ability to combine tools like web search and file analysis for more complex answers.

## Decision
Developers can call the model through LangChain's `ChatOpenAI` interface by specifying the snapshot name.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="o4-mini-2025-04-16")
response = llm.invoke("Explain Newton's third law in simple terms")
print(response)
```

## Links
- <https://platform.openai.com/docs/models/o4-mini>
- <https://platform.openai.com/docs/changelog>
- <https://openai.com/index/introducing-o3-and-o4-mini/>
