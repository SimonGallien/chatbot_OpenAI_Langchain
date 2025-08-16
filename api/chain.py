import os
from prompts import PROMPT_SUMMARIZE
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def summarize(conversation: str) -> str:
    prompt_template = PROMPT_SUMMARIZE
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["OPENAI_MODEL_API"],
        temperature=0.2,
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke(conversation)
