from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
import json
from parameter_store import Ssm
import datetime


# from . import crud, deps, models, schemas, security
# from app
import schemas, config


# this is naughty
def clock_as_json(self):
    return json.dumps(
        {
            "id": self.id,
            "interval": self.interval,
            "start": self.start.timestamp(),
            "now": self.now.timestamp(),
            "tz": self.start.tzinfo(),
        }
    )


app = FastAPI()
ssm = Ssm()


@app.get("/clock/{id}", response_model=schemas.Clock)
def get_clock(id):
    raw_clock = ssm.get(f"{config.store_path}{id}")
    json_clock = json.loads(raw_clock)
    return schemas.Clock(
        interval=json_clock["interval"],
        start=datetime.datetime.fromtimestamp(json_clock["start"]),
        now=datetime.datetime.fromtimestamp(json_clock["now"]),
        id=json_clock["id"],
        tz=datetime.datetime.fromtimestamp(json_clock["start"]),  #####
    )


@app.post("/clock/", response_model=schemas.Clock)
def write_clock(clock: schemas.NewClock):
    return_clock = schemas.Clock(
        interval=clock.interval, start=clock.start, now=clock.start, id=clock.id
    )

    ssm.put(f"{config.store_path}{clock.id}", value=clock_as_json(return_clock))
    return return_clock


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
