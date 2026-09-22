import json
from datetime import datetime
from pathlib import Path


TRIPS_PATH = Path(__file__).resolve().parents[2] / "data" / "trips"


def save_trip(
    destination: str,
    days: int,
    interests: list[str],
    pace: str,
    content: str
) -> int:
    """
    保存一条历史攻略
    如果相同的旅行需求已经存在，则直接返回已有攻略ID
    """
    TRIPS_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    for trip_file in TRIPS_PATH.glob("*.json"):
        with open(
            trip_file,
            "r",
            encoding="utf-8"
        ) as file:
            trip = json.load(file)

        if (
            trip["destination"] == destination
            and trip["days"] == days
            and trip["interests"] == interests
            and trip["pace"] == pace
        ):
            return trip["id"]

    files = list(TRIPS_PATH.glob("*.json"))

    trip_id = 1

    if files:
        trip_id = max(
            int(file.stem)
            for file in files
        ) + 1

    trip = {
        "id": trip_id,
        "destination": destination,
        "days": days,
        "interests": interests,
        "pace": pace,
        "content": content,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    file_path = TRIPS_PATH / f"{trip_id}.json"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            trip,
            file,
            ensure_ascii=False,
            indent=2
        )

    return trip_id

def list_trips() -> list[dict]:
    """
    获取历史攻略列表
    """
    if not TRIPS_PATH.exists():
        return []

    trips = []
    for file_path in TRIPS_PATH.glob("*.json"):
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            trip = json.load(file)

        trips.append({
            "id": trip["id"],
            "destination": trip["destination"],
            "days": trip["days"],
            "interests": trip["interests"],
            "pace": trip["pace"],
            "created_at": trip["created_at"]
        })

    trips.sort(
        key=lambda x: x["id"],
        reverse=True
    )
    return trips

def get_trip(trip_id: int) -> dict | None:
    """
    根据ID获取完整攻略
    """
    file_path = TRIPS_PATH / f"{trip_id}.json"

    if not file_path.exists():
        return None


    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def list_trips() -> list[dict]:
    """
    获取历史攻略列表。
    """

    if not TRIPS_PATH.exists():
        return []

    trips = []

    for file_path in TRIPS_PATH.glob("*.json"):
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            trip = json.load(file)

        trips.append({
            "id": trip["id"],
            "destination": trip["destination"],
            "days": trip["days"],
            "interests": trip["interests"],
            "pace": trip["pace"],
            "created_at": trip["created_at"]
        })

    trips.sort(
        key=lambda x: x["id"],
        reverse=True
    )

    return trips


def get_trip(trip_id: int) -> dict | None:
    """
    根据ID获取完整攻略。
    """

    file_path = TRIPS_PATH / f"{trip_id}.json"

    if not file_path.exists():
        return None

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)

def delete_trip(trip_id: int) -> bool:
    file_path = TRIPS_PATH / f"{trip_id}.json"

    if not file_path.exists():
        return False

    file_path.unlink()
    return True



# 测试
if __name__ == "__main__":
    trip_id = save_trip(
        destination="上海",
        days=3,
        interests=["历史文化", "夜景"],
        pace="休闲",
        content="# 上海3天旅游行程\n\n## 第1天\n豫园..."
    )

    print(f"保存成功，攻略ID：{trip_id}")

if __name__ == "__main__":
    print("历史攻略：")
    print(list_trips())

    print("\n完整攻略：")
    print(get_trip(1))