import uvicorn
from fastapi import FastAPI

from controllers import (
    cards,
    pagos,
    suscripcion,
    planes,
    pasarelas,
    pyments,
    users_subscriptions,
    webhooks,
)
from settings import Settings

settings = Settings()


app = FastAPI(
    title="Membership API",
    description="Membership API to interact with Trely",
    version="1.1.0",
    root_path=settings.ROOT_PATH,
)

app.include_router(webhooks.router)
app.include_router(pyments.router)
app.include_router(users_subscriptions.router)
app.include_router(cards.router)
app.include_router(pagos.router)
app.include_router(suscripcion.router)
app.include_router(planes.router)
app.include_router(planes.router)
app.include_router(pasarelas.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
