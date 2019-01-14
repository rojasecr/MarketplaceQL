# MarketplaceQL 

MarketplaceQL is a server side web GraphQL api designed to be the backend of a barebones online marketplace. 

## Getting started

MarketplaceQL is written in Python with the help of Flask, Graphene, and SQLAlchemy. In what follows, we will walk through the capabilities of MarketplaceQL via a sample fruit vendor marketplace. 

### Install dependencies

`$ pip3 install SQLAlchemy
 $ pip3 install graphene_sqlalchemy
 $ pip3 install Flask
 $ pip3 install Flask-Graphql
`
### Populate the product inventory

`$ python3 setup.py`

setup.py creates an SQLite database from the data in fruits.json. Once you're comftrable with MarketplaceQL, feel free to use your own data!
### Launch the api
`$ python3 api.py`

Navigate to http://localhost:5000/graphql and let the fun begin! 

## Endpoints

At any point you can click Docs in the upper right hand corner of GraphiQL to see all possible queries and mutations. 

### Querying products  

View all products along with the id, title, price, and inventory count of each product. Note that price is given in cents and can be converted to dollars on the front end. 
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
We can pass an argument to allProducts to only return products with available inventory.
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
Additionally we can create a feed for viewing products one at a time by querying the first product,
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
and then using the "before" or "after" arguments to get the next or previous or item respectively.
```graphql

query {
  allProducts(first: 1,after: "{prev_cursor}") {
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
Also we can always fetch products one at a time using their id.
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

## Acknowledgements
Thank you!
