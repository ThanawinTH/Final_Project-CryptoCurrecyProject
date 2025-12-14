# api/binance_rest.py

import requests

BASE_URL = "https://api.binance.com"


def get_24h_ticker(symbol: str) -> dict:
    """
    Get 24h ticker statistics from Binance

    Returns dict with keys:
    - lastPrice
    - priceChangePercent
    - highPrice
    - lowPrice
    - quoteVolume
    """

    url = f"{BASE_URL}/api/v3/ticker/24hr"
    params = {
        "symbol": symbol.upper()
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # basic validation (fail fast)
        required_keys = [
            "lastPrice",
            "priceChangePercent",
            "highPrice",
            "lowPrice",
            "quoteVolume",
        ]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing key in response: {key}")

        return data

    except requests.RequestException as e:
        raise RuntimeError(f"Binance REST request failed: {e}")

    except ValueError as e:
        raise RuntimeError(f"Invalid Binance REST response: {e}")
def get_klines(symbol: str, interval="1h", limit=100):
    url = f"{BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    return r.json()
