from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import json
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from datetime import timedelta
from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Management System API",
    description="A RESTful API for managing products and categories with token-based authentication",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "authentication",
            "description": "Operations related to authentication"
        },
        {
            "name": "categories",
            "description": "CRUD operations for product categories"
        },
        {
            "name": "products",
            "description": "CRUD operations for products"
        },
        {
            "name": "export",
            "description": "Data export operations"
        }
    ]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication endpoints
@app.post("/token", response_model=schemas.Token, tags=["authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token
    
    - **username**: Email address of the user
    - **password**: User's password
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Category endpoints
@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Product endpoints
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    name: str = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))
    products = query.offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Export endpoints
@app.get("/export/products/json")
def export_products_json(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    products = db.query(models.Product).all()
    products_list = []
    for product in products:
        products_list.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "category_id": product.category_id
        })
    return products_list

@app.get("/export/products/csv")
def export_products_csv(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    products = db.query(models.Product).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "description", "price", "quantity", "category_id"])
    
    for product in products:
        writer.writerow([
            product.id,
            product.name,
            product.description,
            product.price,
            product.quantity,
            product.category_id
        ])
    
    response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=products.csv"
    return response
