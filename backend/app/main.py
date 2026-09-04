# from fastapi import FastAPI

# app = FastAPI(title = "Client Follow-Up Automation API")

# @app.get('/')
# def root():
#     return {
#         'message':"Client Follow-Up Automation API is running"
#     }

# @app.get('/health')
# def health():
#     return {
#         'status':'healthy'
#     }

# # @app.get('/clients')
# # def get_clients():
# #     return [
# #         {
# #             'id':1,
# #             'name':'Rahul',
# #             'company':'ABC technologies'
# #         },
# #         {
# #             'id':2,
# #             'name':'priya',
# #             'company':'xyz solutions'   
# #         }
# #     ]

# from backend.app.core.database import engine
# from sqlalchemy import text

# @app.get('/db-health')
# def db_health():
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))

#     return {
#         "database" : result.scalar()
#     }

# from app.api.clients import router as clients_router

# app.include_router(clients_router)




from fastapi import FastAPI

from backend.app.api.clients import router as clients_router
from backend.app.core.database import engine
from sqlalchemy import text


app = FastAPI(
    title="Client Follow-Up Automation API"
)


app.include_router(clients_router)


@app.get("/")
def root():
    return {
        "message": "Client Follow-Up Automation API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-health")
def db_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": result.scalar()
    }