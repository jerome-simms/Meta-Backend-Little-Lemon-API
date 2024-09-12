# Little Lemon API Project for Meta Backend Developer Professional Certificate

## Summary
This is the final project for the APIs course which is a part of the Meta Backend Developer Professional Certificate Course that is hosted on Coursera.

## What I have learnt
This project has been a major learning opportunity for me. Whilst completing it, I have learnt the following:
- API routes with Django Rest Framework
- Django Rest Framework APIViews
- Django Rest Framework Generic Views
- How to access data within the url as well as using query parameters
- Djoser for token authentication
- How to make and check for authenticated requests in Django


## API Endpoints
### User registration and token generation
| Endpoint | Role  | Method | Purpose |
|----------|-------|--------|---------|
|/api/users/| No role | POST |Creates a new user with name, email, password |
|/auth/users/me/| Has valid username | GET | Display the current user |
|/auth/token/login/| Has valid email and password | POST | Generate account tokem for user |

### Menu-items endpoints
| Endpoint | Role  | Method | Purpose |
|----------|-------|--------|---------|
|/api/menu-items| Customer, delivery_crew | GET | List all menu items |
|/api/menu-items| Customer, delivery_crew | POST, PATCH, PUT, DELETE | Denies access, returns 403 |
|/api/menu-items/{menuItem} | Customer, delivery_crew | GET | List single menu item |
|/api/menu-items/{menuItem}| Customer, delivery_crew | POST, PATCH, PUT, DELETE | Denies access, returns 403 |
|/api/menu-items| manager | GET | List all menu items |
|/api/menu-items| manager | POST | Create new menu itek, return 201 |
|/api/menu-items/{menuItem} | manager | GET | List single menu item |
|/api/menu-items/{menuItem} | manager | PUT, PATCH | Update single menu item |
|/api/menu-items/{menuItem} | manager | DELETE | Delete single menu item |


### User group management endpoints
| Endpoint | Role  | Method | Purpose |
|----------|-------|--------|---------|
| /api/groups/manager/users | manager | GET | Returns a list of all managers |
| /api/groups/manager/users | manager | POST | Assigns the user in the payload to the manager group |
| /api/groups/manager/users/{userId} | manager | DELETE | Removes the user with userId from the manager group |
| /api/groups/delivery-crew/users | manager | GET | Returns a list of all delivery crew members |
| /api/groups/delivery-crew/users | manager | POST | Assigns the user in the payload to the delivery_crew group |
| /api/groups/delivery-crew/users/{userId} | manager | DELETE | Removes the user with userId from the delivery_crew group |

### Cart management endpoints
| Endpoint | Role  | Method | Purpose |
|----------|-------|--------|---------|
| /api/cart/menu-items | customer | GET | Returns current items in the cart for the current customer |
| /api/cart/menu-items | customer | POST | Adds a menu item to the cart for the current user |
| /api/cart/menu-items | customer | DELETE | Deletes the cart for the current user |

### Order management endpoints
| Endpoint | Role  | Method | Purpose |
|----------|-------|--------|---------|
| /api/orders | customer | GET | Returns all orders with order items created by this user |
| /api/orders | customer | POST | Creates a new order for the signed in user and emptys cart into order items table |
| /api/orders/{orderId} | customer | GET | Returns all the items that are apart of that order for this customer |
| /api/orders | manager | GET | Returns all orders from all users |
| /api/orders/{orderId} | manager | PATCH | Updates the order with that ID |
| /api/orders/{orderId} | manager | DELETE | Deletes this order |
| /api/orders | delivery_crew | GET | Returns all the orders assigned to that delievery crew |
| /api/orders/{orderId} | delivery_crew | PATCH | Allows the delivery crew to update the delivered status for that order |

## How to run
To run this project you should do the following:
1. Download the source code to your local machine (whether by zip or git)
2. Activate a pipenv environment by running the command `pipenv shell`
3. Install all the relevant dependencies using the command `pipenv install`
4. Run the development server by running `python manage.py runserver` from the project's root directory
5. In your browser you may explore the API by navigating from the root url `localhost:8000` to any of the routes listed above