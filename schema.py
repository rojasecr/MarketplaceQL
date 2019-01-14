from typing import Union
from collections import Counter
from graphql_relay.node.node import to_global_id

# flask_sqlalchemy/schema.py
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Product as ProductModel, Cart as CartModel, Item as ItemModel

import utils

class Item(SQLAlchemyObjectType):
    class Meta:
        model = ItemModel
        interfaces = (relay.Node, )

class ItemsConnection(relay.Connection):
    class Meta:
        node = Item

class AddItemInput(graphene.InputObjectType):
    cart_id = graphene.ID(required=True,description="Global id of cart that item will be added to.")
    product_id = graphene.ID(required=True, description="Global id of the desired product.")

class AddItem(graphene.Mutation):
    cart = graphene.Field(lambda: Cart, description="Cart including added item")

    class Arguments:
        input=AddItemInput(required=True)

    def mutate(self,info,input):
        data = utils.input_to_dictionary(input)
        item = ItemModel(**data)
        db_session.add(item)
        db_session.commit()
        return AddItem(cart=item.cart)

class Cart(SQLAlchemyObjectType):
    class Meta:
        model = CartModel
        interfaces = (relay.Node, )

    def resolve_total(self,info):
        return sum([item.product.price for item in self.items])

class CreateCart(graphene.Mutation):
    cart = graphene.Field(lambda: Cart)

    def mutate(self, info):
        cart = CartModel(total=0)
        db_session.add(cart)
        db_session.commit()
        return CreateCart(cart=cart)

class CompleteCartInput(graphene.InputObjectType):
    id=graphene.ID(required=True,description="Global ID of cart to be completed")

class CompleteCart(graphene.Mutation):
    success = graphene.Boolean(description="True if and only if all products have succifient inventory.")
    insufficient_stock=graphene.List(graphene.ID,description="List of items that have insufficient inventory.")

    class Arguments:
        input=CompleteCartInput(required=True)

    def mutate(self,info,input):
        data = utils.input_to_dictionary(input)
        cart=db_session.query(CartModel).filter_by(id=data['id']).scalar()
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
            return CompleteCart(success=False,insufficient_stock=insufficient_stock)
        db_session.query(CartModel).filter_by(id=data['id']).delete()
        db_session.commit()
        return CompleteCart(success=True)

class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
        interfaces = (relay.Node, )
            
class ProductConnection(relay.Connection):
    class Meta:
        node = Product

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_products = SQLAlchemyConnectionField(ProductConnection, in_stock=graphene.Boolean(description="Only return in stock products when true."))

    def resolve_all_products(self, info, in_stock=False, **args):
        q=Product.get_query(info)
        if in_stock:
            return q.filter(ProductModel.inventory_count > 0)
        return q.all()

    #Make a parameter for all_products
    product = relay.Node.Field(Product)
    cart = relay.Node.Field(Cart)


class Mutation(graphene.ObjectType):
    createCart = CreateCart.Field()
    addItem = AddItem.Field()
    completeCart = CompleteCart.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
