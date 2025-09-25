import load_env
load_env.run_env()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Literal
from langgraph.graph import START, END
from langgraph.graph import StateGraph

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

class GetWeather(BaseModel):
    '''指定された場所の現在の天気を取得する'''
    location: str = Field(
        ..., description="都市の名前"
    )

class GetPopulation(BaseModel):
    '''指定された場所の現在の人口を取得する'''
    location: str = Field(
        ..., description="都市の名前"
    )

tools = [GetWeather, GetPopulation]
model_with_tools = llm.bind_tools(tools)


from typing_extensions import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent(state: State):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

def tools(state: State):
    tool_by_name = {
        "GetWeather": get_weather,
        "GetPopulation": get_population,
    }

    last_message = state["messages"][-1]
    tool_function = tool_by_name[last_message.tool_calls[0]["name"]]
    tool_output = tool_function.invoke(
        last_message.tool_calls[0]["args"]
    )

    tool_message = ToolMessage(
        content=tool_output,
        tool_call_id=last_message.tool_calls[0]["id"]
    )

    return {"messages": [tool_message]}

@tool
def get_weather(location: str):
    '''指定された場所の現在の天気を取得する'''
    return f"{location}は晴れです。"

@tool
def get_population(location: str):
    """人口に関する情報を返す関数"""
    return f"{location}の人口は100人です。"



from typing_extensions import Literal
from langgraph.graph import START, END

def should_continue(state: State) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

from langgraph.graph import StateGraph

graph = StateGraph(State)

graph.add_node("agent", agent)
graph.add_node("tools", tools)
graph.add_edge("tools", 'agent')
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue
)

compiled_graph = graph.compile()
mermaid_md = compiled_graph.get_graph().draw_mermaid()
with open("graph.md", "w") as f:
    f.write("```mermaid\n")
    f.write(mermaid_md)
    f.write("\n```")


# from langchain_core.messages import HumanMessage
# response = compiled_graph.invoke({"messages": [HumanMessage(content="東京の天気は？")]})
# print(response)
