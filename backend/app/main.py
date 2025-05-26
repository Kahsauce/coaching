from fastapi import FastAPI

app = FastAPI(title="Coaching App")

@app.get("/health")
def health_check():
    return {"status": "ok"}
