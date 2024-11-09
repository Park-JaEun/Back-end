from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
# import uvicorn

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    데이터 검증
    데이터 가공
    데이터 베이스에 입력
    응답 생성
    """
    return {"item_id": item_id, "q": q}


@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)