# Little Lemon API Project for Meta Backend Developer Professional Certificate

## Summary
This is the final project for the APIs course which is a part of the Meta Backend Developer Professional Certificate Course that is hosted on Coursera.

## What I have learnt


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

### Cart management endpoints
| Endpoint | Role  | Method | Purpose |
|----------|-------|--------|---------|

### Order management endpoints
| Endpoint | Role  | Method | Purpose |
|----------|-------|--------|---------|

## How to run