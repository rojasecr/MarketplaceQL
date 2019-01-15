# MarketplaceQL 

MarketplaceQL is a server side GraphQL web api for a barebones online marketplace. 

## Getting started

MarketplaceQL is written in Python with the help of Flask, Graphene, and SQLAlchemy. In what follows, we will walk through the capabilities of MarketplaceQL. You are encouraged to test the inputs using the sample fruit vendor marketplace.  

#### Install dependencies

```
$ pip3 install SQLAlchemy
$ pip3 install graphene_sqlalchemy
$ pip3 install Flask
$ pip3 install Flask-Graphql
```

#### Populate the product database

`$ python3 setup.py`

setup.py creates an SQLite database from the data in fruits.json. Once you're comftrable with MarketplaceQL, feel free to use your own data!
#### Launch the api
`$ python3 api.py`

Navigate to http://localhost:5000/graphql and let the fun begin! 

## Endpoints

At any point you can click Docs in the upper right hand corner of GraphiQL to see all possible queries and mutations. Copy the following inputs into GraphiQL to see how the api responds in our sample fruit vendor marketplace.  

### Querying Products  

#### All at once
View the id, title, price, and inventory count of each product. Note that price is given in cents and can be converted to dollars on the front end. 
```graphql

query {
  allProducts {
    edges { 
      node {
        id
	title
	price
	inventoryCount
      }
    }
  } 
}
```
We can pass an argument to allProducts so that it only returns products with available inventory.
```graphql

query {
  allProducts(inStock: true) {
    edges { 
      node {
        id
	title
	price
	inventoryCount
      }
    }
  } 
}
```

#### One at a time
We can create a feed for viewing products one at a time by querying the first product,
```graphql

query {
  allProducts(first: 1) {
    edges { 
      node {
        id
	title
	price
	inventoryCount
      }
      cursor
    }
  } 
}
```
and then passing the cursor to "before" or "after" arguments to get the previous or next item respectively.
```graphql

query {
  allProducts(first: 1, after: "{cursor}") {
    edges { 
      node {
        id
	title
	price
	inventoryCount
      }
      cursor
    }
  } 
}
```
Additionally, we can always fetch individual products using their id.
```graphql

query {
  product(id: "{prod_id}") {
    id
    title
    price
    inventoryCount
  } 
}
```

### Making a purchase 

#### Create a cart
In order to purchase anything, one must first create a cart.
```graphql

mutation {
  createCart {
    cart {
      id
    }
  } 
}
```
This command creates a cart and returns the global id of the new cart. As with everything in GraphQL,we could alter the input in order to return additional information about the cart. We will soon see examples of this.

#### Add an item
We can add items to the cart by passing the id of the cart and the id of the product we want to add.

```graphql

mutation {
  addItem(input:{
    cartID: "{cart_id}"
    productID: "{product_id}" 
  )} {
    cart {
      id
      total
    }
  } 
}
```

This command adds an item to the cart and then returns the cart's id and the total value of all the items in the cart. Alternatively we could input:

```graphql

mutation {
  addItem(input:{
    cartID: "{cart_id}"
    productID: "{product_id}" 
  )} {
    cart {
      id
      total
      items {
        edges {
          node {
            product {
              id 
              title
              price
            }
          }
        }
      }
    }
  } 
}
```
while significantly more verbose, adding an item in this case would return the cart's id and total, as well as a list of all the products in the cart including their id, title, and price. 

#### View the cart 
We can query a cart by its id to view the items in the cart and the total cost of all items.

```graphql

query {
  cart(id: "{cart_id}") {
    id
    total
    items {
      edges {
        node {
          product {
            id 
            title
            price
          }
        }
      }
    }
  } 
}
```

#### Complete the cart 
Once you have a cart full of items you can complete the cart in order to purchase the items.

```graphql

mutation {
  completeCart(input:{
    id: "{cart_id}"
  )} {
    success
    insufficientStock
  } 
}
```
This command will attempt to purchase all the items in the cart. If all products have sufficient inventory, then success will return true. Otherwise, success will return false and insufficientStock will return a list of all products that have insufficient stock.


## Play around

Use the sample fruit vendor marketplace and the commands you learned to buy your fill of fruit. Query products to see how the inventory changes as you complete purchases. Try to purchase out of stock products and products without enough stock for your quantity and see what happens!

## To add
* Remove item from cart 
* Delete cart 
* Secure payments
* Product search 

## Acknowledgements
This project was built with the help of many online resources, but especially https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial. 

Thanks!
