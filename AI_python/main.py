from http.client import responses

# from binstar_client import STATUS_CODES
from fastapi import FastAPI, HTTPException # FastAPI -> http에 대한 비동기 방식을 처리
from pydantic import BaseModel # 데이터 유효성 검사와 설정 관리에 사용되는 라이브러리(모델링이 쉽고 강력함)
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# 요청과 응답사이에 특정 작업 수행

# middleware 는 모든 요청에 대해 실행되며, 요청을 처리하기 전에 응답을 반환하기 전에 특정 작업을 수행할 수 있음
# 로깅, 인증, cors처리, 압축 등
import logging

from starlette.requests import Request # 요청
from starlette.responses import Response # 응답

app = FastAPI(
    title="My API",
    description="This is a sample API",
    version="1.0.0",
    docs_url=None, # http://localhost:8001/docs 보안상 None 처리
    redoc_url=None # redoc 에도 적용
) # 객체 생성후 app 변수에 저장

@app.get("/") # http://localhost/ 의 라우트(경로)
async def read_root():
    return {"Hello" : "World"}

# main.py 가 존재하는 폴더에서 uvicorn main:app --reload --port 8001

class LoggingMiddleware(BaseHTTPMiddleware): # 로그를 콘솔에 출력하는 용도
    logging.basicConfig(level=logging.INFO) # 로그 출력 추가
    async def dispatch(self, request, call_next) :
        logging.info(f"Req: {request.method}{request.url}") #  HTTP 메서드(GET, POST 등)와 요청 URL을 로그로 출력
        response = await call_next(request) # 요청을 처리하고, 해당 요청에 대해 응답을 반환
        logging.info(f"Status Code : {response.status_code}") # 응답의 상태 코드를 로그로 출력
        return response

app.add_middleware(LoggingMiddleware) # 모든 요청에 대해 로그를 남기는 미들웨어 클래스를 사용

class Item(BaseModel): # 아이템 객체 생성(BaseModel : 객체 연결 -> 상속)
    name : str
    description : str = None # 기본값이 None
    price : float
    tax : float = None

@app.get("/items/{item_id") # http://ip주소:포트/items/1
async def read_item(item_id: int, q: str = None):
    return {"item_id" : item_id, "q": q}
    # item_id: 상품번호 -> 경로 매개변수
    # q: 쿼리 매개변수 (기본값 none)

@app.post("/items/{item_id") 
async def create_item(item: Item): # BaseModel 은 데이터 모델링을 쉽게 도와주고 유효성검사도 수행
    return item
    # 잘못된 데이터가 들어오면 422 코드 반환

# 기본주소뒤에 docs 추가입력해서 post 테스트가능