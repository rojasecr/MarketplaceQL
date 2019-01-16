from typing import Union
from collections import Counter
from graphql_relay.node.node import to_global_id
from graphql_relay.node.node import from_global_id

# flask_sqlalchemy/schema.py
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Product as ProductModel, Cart as CartModel, Item as ItemModel


## Product schema
class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
        interfaces = (relay.Node, )
            
class ProductConnection(relay.Connection):
    class Meta:
        node = Product

##Cart schema
class Cart(SQLAlchemyObjectType):
    class Meta:
        model = CartModel
        interfaces = (relay.Node, )

    def resolve_total(self,info):
        return sum([item.product.price for item in self.items])

## Item schema
class Item(SQLAlchemyObjectType):
    class Meta:
        model = ItemModel
        interfaces = (relay.Node, )

class ItemsConnection(relay.Connection):
    class Meta:
        node = Item


## Cart mutations
class CartCreate(graphene.Mutation):
    cart = graphene.Field(lambda: Cart)

    def mutate(self, info):
        cart = CartModel(total=0)
        db_session.add(cart)
        db_session.commit()
        return CartCreate(cart=cart)


class CartAdd(graphene.Mutation):
    cart = graphene.Field(lambda: Cart, description="Cart including added item")

    class Arguments:
        cart_id = graphene.ID(required=True,description="Global id of cart that item will be added to.")
        product_id = graphene.ID(required=True, description="Global id of the desired product.")

    def mutate(self,info,cart_id,product_id):
        local_cart_id, local_product_id = from_global_id(cart_id)[1], from_global_id(product_id)[1] 
        item = ItemModel(cart_id=local_cart_id,product_id=local_product_id)
        db_session.add(item)
        db_session.commit()
        return CartAdd(cart=item.cart)


class CartComplete(graphene.Mutation):
    success = graphene.Boolean(description="True if and only if all products have succifient inventory.")
    insufficient_stock=graphene.List(graphene.ID,description="List of items that have insufficient inventory.")

    class Arguments:
        id=graphene.ID(required=True,description="Global ID of cart to be completed.")

    def mutate(self,info,id):
        local_id=from_global_id(id)[1]
        cart=db_session.query(CartModel).filter_by(id=local_id).scalar()
        in_cart=Counter([item.product for item in cart.items])
        insufficient_stock=[]
        for prod in in_cart:
            new_inventory= prod.inventory_count - in_cart[prod]
            if new_inventory < 0:
                insufficient_stock.append(to_global_id("Product",prod.id))
            else:   
                db_session.query(ProductModel).filter_by(id=prod.id).update(dict(inventory_count=new_inventory))
        if insufficient_stock:
            db_session.rollback()
            return CartComplete(success=False,insufficient_stock=insufficient_stock)
        db_session.commit()
        return CartComplete(success=True)


## Root types
class Query(graphene.ObjectType):
    node = relay.Node.Field()

    productView = relay.Node.Field(Product)
    productViewAll = SQLAlchemyConnectionField(ProductConnection, in_stock=graphene.Boolean(description="Only return in stock products when true."))
    def resolve_productViewAll(self, info, in_stock=False, **args):
        q=Product.get_query(info)
        if in_stock:
            return q.filter(ProductModel.inventory_count > 0)
        return q.all()

    cartView = relay.Node.Field(Cart)


class Mutation(graphene.ObjectType):
    cartCreate = CartCreate.Field()
    cartAdd = CartAdd.Field()
    cartComplete = CartComplete.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
