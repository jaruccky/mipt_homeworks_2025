from fastapi import APIRouter, Query

from app.services.repositories_service import search_and_save_repositories

router = APIRouter(tags=["repositories"])


@router.get("/repositories/search")
async def search_repositories(
    limit: int = Query(..., gt=0),
    offset: int = Query(0, ge=0),
    lang: str = Query(..., min_length=1),
    stars_min: int = Query(0, ge=0),
    stars_max: int | None = Query(None, ge=0),
    forks_min: int = Query(0, ge=0),
    forks_max: int | None = Query(None, ge=0),
) -> dict[str, str]:
    filename = await search_and_save_repositories(
        limit=limit,
        offset=offset,
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max,
    )

    return {
        "status": "ok",
        "file": filename,
    }
