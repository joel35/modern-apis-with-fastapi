from typing import List, Optional
import fastapi
from fastapi import Depends

from models.location import Location
from models.validation_error import ValidationError
from models.reports import Report, ReportSubmittal
from services import openweather_service, report_service

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


@router.get("/api/reports", name="all_reports", response_model=List[Report])
async def reports_get() -> List[Report]:
    # await report_service.add_report("A", location=Location(city="NYC"))
    return await report_service.get_reports()


@router.post("/api/reports", name="add_report", status_code=201, response_model=Report)
async def reports_post(report_submittal: ReportSubmittal) -> Report:
    d = report_submittal.description
    loc = report_submittal.location

    return await report_service.add_report(d, loc)
