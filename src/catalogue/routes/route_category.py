from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.catalogue.schemas.sch_category import CategoryCreate, CategoryRead, CategoryUpdate
from src.catalogue.services.ser_category import CategoryService
from src.db.main import get_session
import uuid
from typing import List

category_router = APIRouter()
Category_service = CategoryService()


@category_router.post("/create", response_model=CategoryRead)
async def create_category(data: CategoryCreate, session: AsyncSession = Depends(get_session)):
    return await Category_service.create(session, data)


@category_router.get("/getCategoryByID/{uid}", response_model=CategoryRead)
async def get_category(uid: uuid.UUID, session: AsyncSession = Depends(get_session)):
    return await Category_service.get_by_uid(str(uid), session)


@category_router.get("/getCategory", response_model=List[CategoryRead])
async def list_categories(session: AsyncSession = Depends(get_session)):
    return await Category_service.get_all(session)


@category_router.put("/update/{uid}", response_model=CategoryRead)
async def update_category(uid: uuid.UUID, data: CategoryUpdate, session: AsyncSession = Depends(get_session)):
    return await Category_service.update(str(uid), data, session)


@category_router.delete("/{uid}")
async def delete_category(uid: uuid.UUID, session: AsyncSession = Depends(get_session)):
    await Category_service.delete(str(uid), session)
    return {"detail": "Category deleted"}
