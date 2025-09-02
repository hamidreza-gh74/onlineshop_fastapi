from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from src.catalogue.models import Category
from src.catalogue.schemas.sch_category import CategoryCreate, CategoryUpdate


class CategoryService:

    async def create(self, session: AsyncSession, data: CategoryCreate) -> Category:
        db_obj = Category.model_validate(data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_uid(self, uid: str, session: AsyncSession) -> Category:
        statement = select(Category).where(Category.uid == uid)
        result = await session.exec(statement)
        category = result.first()
        if category:
            return category
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    async def get_all(self, session: AsyncSession) -> list[Category]:
        statement = select(Category)
        result = await session.exec(statement)
        return result.all()

    async def update(self, uid: str, data: CategoryUpdate, session: AsyncSession) -> Category:
        category = await self.get_by_uid(uid, session)
        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(category, key, value)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

    async def delete(self, uid: str, session: AsyncSession) -> None:
        category = await self.get_by_uid(uid, session)
        await session.delete(category)
        await session.commit()
