from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
import json
from parameter_store import Ssm
import datetime
from dateutil.relativedelta import relativedelta


# from . import crud, deps, models, schemas, security
# from app
import schemas, config


def update_clock(new_clock: dict):
    ssm.put(f"{config.store_path}{new_clock['id']}", value=json.dumps(new_clock))
    return new_clock


app = FastAPI()
ssm = Ssm()


@app.put("/clock/{id}/tick", response_model=schemas.Clock)
def tick_clock(id):
    json_clock = get_clock(id)
    now = datetime.datetime.fromisoformat(json_clock["now"])
    delta = relativedelta(seconds=json_clock["interval"])
    new_now = now + delta
    new_clock = json_clock.copy()
    new_clock["now"] = str(new_now)
    updated_clock = update_clock(new_clock)

    return updated_clock


@app.put("/clock/{id}/reset", response_model=schemas.Clock)
def reset_clock(id):
    json_clock = get_clock(id)
    new_clock = json_clock.copy()
    new_clock["now"] = json_clock["start"]
    updated_clock = update_clock(new_clock)

    return updated_clock


@app.get("/clock/{id}", response_model=schemas.Clock)
def get_clock(id):
    raw_clock = ssm.get(f"{config.store_path}{id}")
    json_clock = json.loads(raw_clock)
    return json_clock


@app.get("/clock/{id}/now", response_model=str)
def get_clock_now(id):
    raw_clock = ssm.get(f"{config.store_path}{id}")
    json_clock = json.loads(raw_clock)
    return json_clock["now"]


@app.post("/clock/", response_model=schemas.Clock)
def write_new_clock(clock: schemas.NewClock):
    return_clock = schemas.Clock(
        interval=clock.interval, start=clock.start, now=clock.start, id=clock.id
    )

    ssm.put(f"{config.store_path}{clock.id}", value=json.dumps(return_clock.dict()))
    return return_clock


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
