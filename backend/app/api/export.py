from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.storage.trip_storage import get_trip
from app.export.exporter import (
    export_markdown,
    export_word,
    export_excel
)

router = APIRouter(
    prefix="/export",
    tags=["export"]
)


@router.post("/trip/{trip_id}")
def export_trip(trip_id: int, format: str):
    trip = get_trip(trip_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="攻略不存在"
        )

    destination = trip["destination"]
    days = trip["days"]
    content = trip["content"]

    filename = f"{destination}{days}天旅游攻略"

    if format == "md":
        file_path = export_markdown(
            content,
            filename
        )

    elif format == "word":
        file_path = export_word(
            content,
            filename
        )

    elif format == "excel":
        file_path = export_excel(
            destination,
            days,
            content,
            filename
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="不支持的导出格式"
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name
    )