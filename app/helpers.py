import pickle
from redis import Redis
from datetime import datetime, timedelta

from app.config import Config


REQUEST_LIMIT = 3
RESET_TIME = timedelta(minutes=5)

r = Redis(host=Config.redis_url, port=Config.redis_port, db=0)


def check_request_limit(user_id):
    current_time = datetime.now()

    if r.exists(user_id):
        last_request_time, request_count, user_request_limit = pickle.loads(
            r.get(user_id)
        )

        # If the last request was more than 5 minutes ago, reset the count
        if current_time - last_request_time > RESET_TIME:
            r.set(user_id, pickle.dumps((current_time, 1, user_request_limit)))
            return (user_request_limit - 1, 0, user_request_limit)

        # If request count is greater than user_request_limit, return False
        elif request_count >= user_request_limit:
            wait_time = RESET_TIME - (current_time - last_request_time)
            minutes, seconds = divmod(wait_time.seconds, 60)
            return (0, f"{minutes:02d}:{seconds:02d}", user_request_limit)

        # If request count is less than user_request_limit, return how many requests are left
        else:
            r.set(
                user_id,
                pickle.dumps(
                    (last_request_time, request_count + 1, user_request_limit)
                ),
            )
            return (user_request_limit - request_count - 1, 0, user_request_limit)

    # If user is not in the cache, add them to the cache
    else:
        r.set(user_id, pickle.dumps((current_time, 1, REQUEST_LIMIT)))
        return (REQUEST_LIMIT - 1, 0, REQUEST_LIMIT)


def get_request_limit(user_id):
    current_time = datetime.now()
    last_request_time, request_count, user_request_limit = pickle.loads(r.get(user_id))

    wait_time = RESET_TIME - (current_time - last_request_time)

    minutes, seconds = divmod(wait_time.seconds, 60)

    return (
        user_request_limit - request_count,
        f"{minutes:02d}:{seconds:02d}",
        user_request_limit,
    )


def set_request_limit(user_id, limit):
    r.set(user_id, pickle.dumps((datetime.now(), 0, limit)))


if __name__ == "__main__":
    set_request_limit(Config.admin_telegram_id, 10)
    print(check_request_limit(Config.admin_telegram_id))
