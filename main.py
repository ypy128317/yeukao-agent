import asyncio
import json
from graph import graph
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


@app.get('/')
def health():
    return {'ok': True}


@app.post('/api/chat')
async def chat(req: QueryRequest):
    result = await graph.ainvoke({'user_query': req.query})
    return {'answer': result.get('answer', '')}


async def aab(user_query: str):
    print(f"开始执行:{user_query}")
    result = await graph.ainvoke({'user_query': user_query})
    print('最终state')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


async def main():
    await aab('简单介绍一下人工智能')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
