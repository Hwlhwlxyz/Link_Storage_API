from fastapi import APIRouter

ROUTER = APIRouter()

@ROUTER.get('/api')
def health_check():
    return {"base": "Hello World"};