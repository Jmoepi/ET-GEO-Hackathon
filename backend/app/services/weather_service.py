"""
Weather service for OpenWeather API integration.
Provides forecast data for the Water Stress Model.
"""
import httpx
import structlog
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional
from app.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

OPENWEATHER_BASE = "https://api.openweathermap.org/data/2.5"


@dataclass
class WeatherForecast:
    temperature: float
    humidity: float
    rainfall_forecast: float
    wind_speed: float
    description: str
    forecast_date: datetime
    source: str = "openweathermap"


@dataclass
class WeatherDaily:
    date: datetime
    temp_min: float
    temp_max: float
    humidity: float
    rainfall_mm: float
    description: str


async def get_current_weather(lat: float, lon: float) -> Optional[WeatherForecast]:
    if not settings.OPENWEATHER_API_KEY:
        logger.warning("OpenWeather API key not configured")
        return None

    url = f"{OPENWEATHER_BASE}/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        weather = data.get("weather", [{}])[0]
        main = data.get("main", {})
        rain = data.get("rain", {})

        return WeatherForecast(
            temperature=main.get("temp", 0.0),
            humidity=main.get("humidity", 0.0),
            rainfall_forecast=rain.get("1h", 0.0),
            wind_speed=data.get("wind", {}).get("speed", 0.0),
            description=weather.get("description", "N/A"),
            forecast_date=datetime.now(timezone.utc),
        )
    except httpx.HTTPStatusError as e:
        logger.error("OpenWeather HTTP error", status=e.response.status_code)
        return None
    except Exception as e:
        logger.error("OpenWeather error", error=str(e))
        return None


async def get_forecast(lat: float, lon: float, days: int = 5) -> list[WeatherDaily]:
    if not settings.OPENWEATHER_API_KEY:
        logger.warning("OpenWeather API key not configured")
        return []

    url = f"{OPENWEATHER_BASE}/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "cnt": min(days * 8, 40),
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        daily_map: dict[str, WeatherDaily] = {}

        for item in data.get("list", []):
            dt = datetime.fromtimestamp(item["dt"], tz=timezone.utc)
            date_key = dt.strftime("%Y-%m-%d")

            main = item.get("main", {})
            rain = item.get("rain", {})
            weather_desc = item.get("weather", [{}])[0].get("description", "N/A")

            if date_key not in daily_map:
                daily_map[date_key] = WeatherDaily(
                    date=dt,
                    temp_min=main.get("temp_min", 999),
                    temp_max=main.get("temp_max", -999),
                    humidity=main.get("humidity", 0),
                    rainfall_mm=rain.get("3h", 0.0),
                    description=weather_desc,
                )
            else:
                existing = daily_map[date_key]
                existing.temp_min = min(existing.temp_min, main.get("temp_min", 999))
                existing.temp_max = max(existing.temp_max, main.get("temp_max", -999))
                existing.rainfall_mm += rain.get("3h", 0.0)

        return list(daily_map.values())[:days]

    except httpx.HTTPStatusError as e:
        logger.error("OpenWeather forecast error", status=e.response.status_code)
        return []
    except Exception as e:
        logger.error("OpenWeather forecast error", error=str(e))
        return []


def fallback_weather(lat: float, lon: float) -> WeatherForecast:
    return WeatherForecast(
        temperature=22.0,
        humidity=60.0,
        rainfall_forecast=0.0,
        wind_speed=5.0,
        description="fallback - API unavailable",
        forecast_date=datetime.now(timezone.utc),
        source="fallback",
    )
