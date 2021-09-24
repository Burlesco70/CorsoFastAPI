from typing import Optional, List

from sqlmodel import Field, SQLModel, Session, Relationship, create_engine, select

# Tabella di associazione n:n
class TagProductLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )    

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    products: List["Product"] = Relationship(back_populates="tags", link_model=TagProductLink)

class ProductType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_type: Optional[int] = Field(default=None, foreign_key="producttype.id")
    tags: List["Tag"] = Relationship(back_populates="products", link_model=TagProductLink)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_products():
    with Session(engine) as session:
        tag_offerta = Tag(name="Offerta")
        tag_maionese = Tag(name="Con Maionese")
        tipo_panino = ProductType(name="panino")
        tipo_bibita = ProductType(name="bibita")     
        session.add(tag_offerta)
        session.add(tag_maionese)
        session.add(tipo_panino)
        session.add(tipo_bibita)
        session.commit()

        hamburger = Product(
            name="hamburger", 
            product_type=tipo_panino.id,
            tags=[tag_offerta, tag_maionese]
        )
        coke = Product(
            name="Coca Cola",
            product_type=tipo_bibita.id,
            tags=[tag_offerta]
        )

        session.add(hamburger)
        session.add(coke)
        session.commit()

        session.refresh(hamburger)
        session.refresh(coke)

        print("Created :", hamburger)
        print("Created :", coke)

def select_products():
    with Session(engine) as session:
        statement = select(Product, ProductType).where(Product.product_type == ProductType.id)
        results = session.exec(statement)
        for product, product_type in results:
            print("product:", product, "product_type:", product_type, "tags:", product.tags )        

def main():
    create_db_and_tables()
    #create_products()
    select_products()



if __name__ == "__main__":
    main()