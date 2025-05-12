from concurrent.futures import as_completed

from requests_futures.sessions import FuturesSession
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Decision, engine

future_session = FuturesSession()

with Session(engine) as db:
    query = select(Decision).where(Decision.text == None).limit(100)

    while True:
        futures = []
        for decision in db.scalars(query):
            future = future_session.get(decision.url)
            future.decision = decision
            futures.append(future)

        for future in as_completed(futures):
            response = future.result()
            future.decision.text = response.text

        db.commit()

        if len(futures) == 0:
            break
        else:
            print(f"{futures[0].decision.id} - {futures[-1].decision.id}")
