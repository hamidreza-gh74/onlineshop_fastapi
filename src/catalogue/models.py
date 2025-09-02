from sqlmodel import SQLModel,Field, Relationship, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import event
from core.model.zero_model import ZeroModel
from typing import Optional
import uuid
import enum
from sqlalchemy import Index, func
from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey




class AttributeType(enum.IntEnum):  
    INTEGER = 1
    STRING = 2
    FLOAT = 3


class ProductType(ZeroModel, table=True):

    __tablename__ = "product_types"
    title : str = Field(max_length=32)

    attributes: list["ProductAttribute" ] = Relationship(back_populates="product_type",
                                                         passive_deletes=True)
    
    products: list["Product"] = Relationship(back_populates="product_type",
                                             passive_deletes=True)



class ProductAttribute(ZeroModel, table=True):

    __tablename__ = "product_attributes"
    title : str = Field(max_length=32)
    product_type_uid: uuid.UUID = Field(sa_column=ForeignKey("product_types.uid", ondelete="CASCADE"))

    attribute_type: AttributeType = Field(
        sa_column_kwargs={"nullable": False}, default=AttributeType.INTEGER
    )    
    product_type: "ProductType" = Relationship(back_populates="attributes")
    attributes_values: list["ProductAttributeValue"] = Relationship(back_populates="attribute",
                                                                    passive_deletes=True)



class ProductCategoryLink(ZeroModel, table=True):
    __tablename__ = "product_category_link"
    product_uid: uuid.UUID = Field(foreign_key="products.uid", primary_key=True)
    category_uid: uuid.UUID = Field(foreign_key="categories.uid", primary_key=True)





class Category(ZeroModel, table=True):
    __tablename__ = "categories"

    name: str
    image_url: Optional[str] = Field(default=None, max_length=255) 
    parent_uid: Optional[uuid.UUID] = Field(
        sa_column=ForeignKey("categories.uid", ondelete="CASCADE")
    )
    depth: int = Field(default=0, nullable=False)  


    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "categories.uid"}
    )
    children: list["Category"] = Relationship(back_populates="parent")
    products: list["Product"] = Relationship(
        back_populates="categories",
        link_model=ProductCategoryLink
    )

# listoner for considering depth
@event.listens_for(Session, "before_flush")
def update_category_depth(session, flush_context, instances):
    for obj in session.new.union(session.dirty):
        if isinstance(obj, Category):
            old_depth = obj.depth
            obj.depth = obj.parent.depth + 1 if obj.parent else 0
            if obj.depth != old_depth:
                update_children_depth(obj)

def update_children_depth(category: Category):
    for child in category.children:
        child.depth = category.depth + 1
        update_children_depth(child)





class Brand(ZeroModel, table=True):
    __tablename__ = "brands"
    name: str = Field(max_length=32)
    logo_url: Optional[str] = Field(default=None)  
    products: list["Product"] = Relationship(back_populates="brand",
                                             passive_deletes=True)




class Product(ZeroModel, table=True):

    __tablename__ = "products"
    product_type_uid: uuid.UUID = Field(
        sa_column=ForeignKey("product_types.uid", ondelete="CASCADE")
                )
    title: str = Field(max_length=32)
    description: Optional[str] = Field(default=None)
    brand_uid: uuid.UUID = Field(
    sa_column=ForeignKey("brands.uid", ondelete="CASCADE")
    )

    product_type: ProductType = Relationship(back_populates="products")
    categories: list["Category"] = Relationship(
        back_populates="products",
        link_model=ProductCategoryLink
    )   
    brand: Brand = Relationship(back_populates="products")
    attributes_values: list["ProductAttributeValue"]  = Relationship(back_populates="product",
                                                                     passive_deletes=True)
    images: list["ProductImage"] = Relationship(
    back_populates="product",
    passive_deletes=True
)
    



class ProductAttributeValue(ZeroModel, table=True):
        __tablename__ = "product_attributes_values"
        value: str = Field(max_length=32)

        product_uid: uuid.UUID = Field(
        sa_column=ForeignKey("products.uid", ondelete="CASCADE")
        )
        product_attribute_uid: uuid.UUID = Field(
        sa_column=ForeignKey("product_attributes.uid", ondelete="CASCADE")
        )

        product: "Product" = Relationship(back_populates="attributes_values")
        attribute: "ProductAttribute" = Relationship(back_populates="attributes_values")

        __table_args__ = (
            UniqueConstraint("product_uid", "product_attribute_uid"),
            Index(
                "ix_unique_attr_value_ci",
                func.lower("value"),  
                unique=True
            ),
        )


class ProductImage(ZeroModel, table=True):
    __tablename__ = "product_images"

    product_uid: uuid.UUID = Field(
        sa_column=ForeignKey("products.uid", ondelete="CASCADE"),
        )
    url: str = Field(max_length=255)   
    alt_text: str = Field(default="", max_length=128)  


    product: "Product" = Relationship(
        back_populates="images",
        passive_deletes=True
    )