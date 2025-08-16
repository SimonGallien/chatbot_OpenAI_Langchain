import os
from prompts import PROMPT_SUMMARIZE, SYSTEM_PROMPT
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langgraph.graph import MessagesState, END
from typing import Literal

load_dotenv()


class State(MessagesState):
    history: str


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


# workflow = StateGraph(state_schema=State)


def call_model(state: State, conversation_summary: str) -> dict:

    llm = ChatOpenAI(
        temperature=os.environ["TEMPERATURE"],
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["OPENAI_MODEL_API"],
    )

    history = state.get("history", "")
    if history:
        system_message = f"Summary of conversation earlier: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        system_message = SYSTEM_PROMPT.format(
            conversation=conversation_summary
        )
        messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def summarize_history(state: State) -> dict:
    llm_summarize = ChatOpenAI(
        temperature=os.environ["TEMPERATURE"],
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["OPENAI_MODEL_API"],
    )

    history = state.get("history", "")
    if history:
        history_message = f"Summary of conversation earlier: {history}"
    else:
        history_message = "No conversation history available"
    message = state["messages"] + [HumanMessage(content=history_message)]
    response = llm_summarize.invoke(message)
    delete_message = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"history": response.content, "messages": delete_message}


def should_continue(state: State) -> Literal["summarize_history", END]:
    message = state["messages"]
    if len(message) > 6:
        return "summarize_history"
    return END


def print_update(update: dict) -> None:
    for k, v in update.items():
        for m in v["messages"]:
            m.pretty_print()
        if "history" in v:
            print(v["history"])
