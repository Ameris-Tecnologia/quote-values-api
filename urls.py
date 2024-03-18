"""Route creator"""

from typing import (
    Any,
    Dict,
    List,
)

from fastapi import (
    APIRouter,
    FastAPI,
)
from fastapi_jsonapi import RoutersJSONAPI
from fastapi_jsonapi.atomic import AtomicOperations

from models.fund import Fund
from models.permission import Permission
from models.series import Series
from models.upload import Upload
from models.schemas.fund_schema import FundSchema
from models.schemas.permission_schema import PermissionSchema
from models.schemas.series_schema import SeriesSchema
from models.schemas.upload_schema import UploadSchema
from view_base import DetailViewBase, ListViewBase


def add_routes(app: FastAPI) -> List[Dict[str, Any]]:
    """
    Generic Routes
    """
    tags = [
        {
            "name": "Quotes Values",
            "description": "Quotes Values API",
        }
    ]

    router: APIRouter = APIRouter()
    RoutersJSONAPI(
        router=router,
        path="/funds",
        tags=["Fund"],
        class_detail=DetailViewBase,
        class_list=ListViewBase,
        model=Fund,
        schema=FundSchema,
        resource_type="fund",
    )

    RoutersJSONAPI(
        router=router,
        path="/permissions",
        tags=["Permission"],
        class_detail=DetailViewBase,
        class_list=ListViewBase,
        model=Permission,
        schema=PermissionSchema,
        resource_type="permission",
    )

    RoutersJSONAPI(
        router=router,
        path="/series",
        tags=["Series"],
        class_detail=DetailViewBase,
        class_list=ListViewBase,
        model=Series,
        schema=SeriesSchema,
        resource_type="series",
    )

    RoutersJSONAPI(
        router=router,
        path="/uploads",
        tags=["Upload"],
        class_detail=DetailViewBase,
        class_list=ListViewBase,
        model=Upload,
        schema=UploadSchema,
        resource_type="upload",
    )

    atomic = AtomicOperations()

    app.include_router(router, prefix="")
    app.include_router(atomic.router, prefix="")
    return tags
