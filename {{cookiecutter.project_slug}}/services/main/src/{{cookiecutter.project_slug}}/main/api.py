# (if api-service)
from fastapi import FastAPI
{% if cookiecutter.database != "none" -%}
from {{cookiecutter.namespace}}.utils.database import get_db_connection
{% endif -%}

app = FastAPI(
    title="{{cookiecutter.project_name}}",
    description="{{cookiecutter.description}}",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "{{cookiecutter.project_slug}}"}

@app.get("/api/v1/items")
def list_items():
    # TODO: Implement your API logic
    return {"items": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
