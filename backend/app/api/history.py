from fastapi import APIRouter, HTTPException

from app.storage.trip_storage import (
    list_trips,
    get_trip,
    delete_trip
)


router = APIRouter(
    prefix="/history",
    tags=["history"]
)


@router.get("")
def get_history():
    """
    获取历史攻略列表。
    """
    return {
        "trips": list_trips()
    }


@router.get("/{trip_id}")
def get_history_detail(trip_id: int):
    """
    获取指定历史攻略详情。
    """
    trip = get_trip(trip_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="攻略不存在"
        )

    return trip


@router.delete("/{trip_id}")
def delete_history(trip_id: int):
    """
    删除指定历史攻略。
    """
    success = delete_trip(trip_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="攻略不存在"
        )

    return {
        "message": "删除成功"
    }