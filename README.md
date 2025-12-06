# todo-list-full
# Django REST Framework - Role-Based Access Control Backend

A production-ready Django REST Framework backend implementing custom user authentication with role-based access control (RBAC).

## Features

- Custom User model with role field (ADMIN, MANAGER, STAFF, USER)
- Token-based authentication using DRF's built-in token auth
- Complete authentication flow (register, login, logout, profile management, password change)
- Custom permission classes for role-based access control
- Example protected endpoints demonstrating RBAC
- No external auth dependencies (no JWT, no OAuth)

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout and delete token
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/` - Update profile
- `POST /api/auth/change-password/` - Change password

### Protected Endpoints (Examples)
- `GET /api/admin-panel/` - ADMIN only
- `GET /api/management/` - ADMIN or MANAGER
- `GET /api/staff-zone/` - ADMIN, MANAGER, or STAFF
- `GET /api/public/` - Public (no auth required)
