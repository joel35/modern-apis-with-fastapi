from typing import Optional
import fastapi
from fastapi import Depends

from models.location import Location
from models.validation_error import ValidationError
from services import openweather_service

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(loc: Location = Depends(), units: str = "metric"):

    try:
        return await openweather_service.get_report_async(
            loc.city, loc.state, loc.country, units
        )
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)

    except Exception as x:
        print(f"Server crashed while processing request: {x}")
        return fastapi.Response(
            content="Error processing your request.", status_code=500
        )
