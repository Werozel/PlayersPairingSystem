import pickle


def load_address_cache() -> dict:
    with open("address_cache", "rb") as fin:
        try:
            res = pickle.load(fin)
        except Exception:
            res = {}
        return res


address_cache: dict = load_address_cache()


def save_address_cache():
    with open("address_cache.py", "wb") as out:
        pickle.dump(address_cache, out)
    print("Caches saved")
