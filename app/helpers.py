from datetime import datetime

import pickle
from redis import Redis

from app.config import Config

REQUEST_LIMIT = Config.REQUEST_LIMIT
RESET_TIME = Config.RESET_TIME

r = Redis(host=Config.REDIS_URL, port=Config.REDIS_PORT, db=0)


def check_request_limit(user_id):
    current_time = datetime.now()

    if r.exists(user_id):
        last_request_time, request_count = pickle.loads(r.get(user_id))

        # If the last request was more than 5 minutes ago, reset the count
        if current_time - last_request_time > RESET_TIME:
            r.set(user_id, pickle.dumps((current_time, 1)))
            return (REQUEST_LIMIT - 1, 0)

        # If request count is greater than REQUEST_LIMIT, return False
        elif request_count >= REQUEST_LIMIT:
            wait_time = RESET_TIME - (current_time - last_request_time)
            minutes, seconds = divmod(wait_time.seconds, 60)
            return (0, f"{minutes:02d}:{seconds:02d}")

        # If request count is less than REQUEST_LIMIT, return how many requests are left
        else:
            r.set(user_id, pickle.dumps((last_request_time, request_count + 1)))
            return (REQUEST_LIMIT - request_count - 1, 0)

    # If user is not in the cache, add them to the cache
    else:
        r.set(user_id, pickle.dumps((current_time, 1)))
        return (REQUEST_LIMIT - 1, 0)
