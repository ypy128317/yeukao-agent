from typing import  TypedDict
from langgraph.graph import StateGraph,START,END
from tools import calc_math
from llm_provider import llm
class AgentState(TypedDict):
    user_query:str #用户提问
    task_type:str #任务类型
    worker_result:str #结果
    answer:str #最终答案

def orchestrator_node(state:AgentState):
    print('\n[进入orchestrator_node]')
    user_query = state['user_query']
    print(f"[编排器]正在分析用户意图{user_query}")
    if any(a in user_query for a in{'+','-','*','/'})and any(b.isdigit() for b in user_query):
        task_type='calc'
    else:
        task_type = 'text'
    print(f"[编排器]，识别到任务类型{task_type}")
    return {'task_type':task_type}

def calc_worker_node(state:AgentState):
    print('\n[进入calc_worker_node]')
    user_query = state['user_query']
    expr=user_query.replace('请计算','').strip()
    print(f"[计算worker]准备调用工具计算{expr}")

    result=calc_math.invoke(expr)
    result_one=f"计算结果:{expr}={result}"
    print(f"[计算worker]计算完成,结果{result_one}")
    return {'worker_result':result_one}
async def text_worker_node(state:AgentState):
    print('\n[进入text_worker_node]')
    user_query = state['user_query']
    print(f'[文本worker]正在请求大模型{user_query}')
    res=await llm.ainvoke(user_query)
    print(f"[文本Worker]文本处理完成")
    return{'worker_result':res.content}

def collect_node(state:AgentState):
    print('\n[collect_node]')
    worker_result=state.get('worker_result','未知结果')
    answer=f"任务处理完毕，\n问题:{state['user_query']}\n最终回答:{worker_result}"
    print(f"最终答案:{answer}")
    return {'answer':answer}

def route_orchestrator(state:AgentState):
    task_type=state.get('task_type')
    if task_type=='calc':
        return 'calc_worker'
    elif task_type=='text':
        return 'text_worker'
    else:
        return 'text_worker'

builder=StateGraph(AgentState)
builder.add_node('orchestrator_node',orchestrator_node)
builder.add_node('calc_worker_node',calc_worker_node)
builder.add_node('text_worker_node',text_worker_node)
builder.add_node('collect_node',collect_node)
builder.add_edge(START,'orchestrator_node')
builder.add_conditional_edges(
'orchestrator_node',
        route_orchestrator,
{
        'calc_worker':'calc_worker_node',
        'text_worker':'text_worker_node',
    }
)
builder.add_edge('calc_worker_node','collect_node')
builder.add_edge('text_worker_node','collect_node')
builder.add_edge('collect_node',END)
graph = builder.compile()

