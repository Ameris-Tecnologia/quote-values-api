"""Route creator"""
from typing import (
    Any,
    Dict,
    List,
)

from fastapi import (
    APIRouter,
    FastAPI,
    Security
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
from settings import Settings
from modules.auth import VerifyToken


settings = Settings()
auth = VerifyToken()


class RouterBuilder:
    """Class to construct routers"""

    def __init__(self, name, model, schema) -> None:
        self.name = name
        self.model = model
        self.schema = schema

    def build(self, router: APIRouter) -> None:
        """Method to build route"""
        name_path = self.name
        if name_path[-1] != "s":
            name_path = f"{self.name}s"
        path_build = f"/{name_path}"
        tag_name = f"{self.name[0].upper()}{self.name[1:]}"
        RoutersJSONAPI(
            router=router,
            path=path_build,
            tags=[tag_name],
            class_detail=DetailViewBase,
            class_list=ListViewBase,
            model=self.model,
            schema=self.schema,
            resource_type=self.name,
        )


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

    router: APIRouter = APIRouter(
        dependencies=[Security(auth.verify)]
    )
    RouterBuilder("fund", Fund, FundSchema).build(router)
    RouterBuilder("permission", Permission, PermissionSchema).build(router)
    RouterBuilder("series", Series, SeriesSchema).build(router)
    RouterBuilder("upload", Upload, UploadSchema).build(router)

    atomic = AtomicOperations()

    app.include_router(router, prefix="")
    app.include_router(atomic.router, prefix="")
    return tags
