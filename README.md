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
  productViewAll {
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
  productViewAll(inStock: true) {
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

Thanks to power of GraphQL connections, we can create a feed for viewing products in segments. Indeed the "first" argument controls how many products are returned and the "hasNextPage" attribute tells us if there are more products to see.
```graphql

query {
  productViewAll(first: {segment_size}) {
    edges { 
      cursor
      node {
        id
	title
	price
	inventoryCount
      }
    }
    pageInfo {
      hasNextPage
    }
  } 
}
```
The previous or next segment is returned by passing the cursor to the "before" or "after" arguments respectively.
```graphql

query {
  productViewAll(first: {segment_size}, after: "{cursor}") {
    edges { 
      cursor
      node {
        id
	title
	price
	inventoryCount
      }
    }
    pageInfo {
      hasNextPage
    }
  } 
}

#### One at a time
```
We can fetch individual products using their id.
```graphql

query {
  productView(id: "{prod_id}") {
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
  cartCreate {
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
  cartAdd(productId:"{prod_id}", cartId:"{cart_id}") {
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
  cartAdd(productId:"{prod_id}", cartId:"{cart_id}") {
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
  cartView(id: "{cart_id}") {
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
  cartComplete(id: "{cart_id}") {
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
