from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from chain import summarize
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from chain import (
    State,
    call_model,
    summarize_history,
    should_continue,
    print_update,
)

chain = None
app = FastAPI()


@app.get("/")
async def root():
    print("message: Hello World")


@app.post("/summarize")
async def summarize_text(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()

    text = content.decode("utf-8")
    summary = summarize(text)

    return {"summary": summary}


@app.post("/initialize")
async def initialize(file: UploadFile = File(...)):
    global chain
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()
    text = content.decode("utf-8")

    workflow = StateGraph(State)
    workflow.add_node(
        "conversation",
        lambda input: call_model(state=input, conversation_summary=summary),
    )
    workflow.add_node(summarize_history)
    workflow.add_edge(START, "conversation")
    workflow.add_conditional_edges(
        "conversation",
        should_continue,
    )
    workflow.add_edge("summarize_history", END)

    memory = MemorySaver()
    chain = workflow.compile(checkpointer=memory)
    summary = summarize(text)
    return {"summarize": summary}


async def generate_stream(input_message, config, chain):
    for event in chain.stream(
        {"messages": [input_message]}, config, stream_mode="updates"
    ):
        yield event["conversation"]["messages"][
            0
        ].content  # Envoie le contenu de l'évènement au fur et à mesure


@app.post("/update")
async def update(request: str = Form(...)):
    config = {"configurable": {"thread_id": "4"}}
    input_message = HumanMessage(content=request)
    return StreamingResponse(
        generate_stream(input_message, config, chain), media_type="text/plain"
    )
