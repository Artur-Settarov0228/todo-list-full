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

1. MODEL MA'LUMOTLARI
Task (Vazifa) Modeli maydonlari:
id - unikal raqam

title - sarlavha (max 200 belgi)

description - tavsif (ixtiyoriy)

status - holat: pending, in_progress, completed

priority - daraja: low, medium, high

category - kategoriya: work, personal, home, study

due_date - muddat (sana formatida)

created_by - kim yaratgan (foydalanuvchi ID)

assigned_to - kimga topshirilgan (foydalanuvchi ID)

created_at - yaratilgan vaqt

updated_at - yangilangan vaqt

2. ASOSIY ENDPOINT'LAR
2.1. VAZIFALAR RO'YXATINI OLISH (FILTRLAR BILAN)
text
GET /api/todos/
Headers:
text
Authorization: Token abc123def456
Content-Type: application/json
Query Parameters (FILTRLAR):
status=pending|in_progress|completed (holat bo'yicha)

priority=low|medium|high (daraja bo'yicha)

category=work|personal|home|study (kategoriya bo'yicha)

search=kitob (qidiruv matni)

due_date=2024-12-20 (muddati bo'yicha)

assigned_to=me|others|all (kimga topshirilgan)

page=1 (sahifa raqami)

page_size=10 (har sahifadagi elementlar soni)

Responselar:
a) Oddiy foydalanuvchi uchun (faqat o'zi yaratgan vazifalar):

json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Kitob o'qish",
      "description": "Python darsligini 50 bet o'qish",
      "status": "pending",
      "priority": "high",
      "category": "study",
      "due_date": "2024-12-20",
      "created_at": "2024-12-15T10:30:00Z",
      "updated_at": "2024-12-15T10:30:00Z",
      "created_by": 1,
      "assigned_to": null
    }
  ]
}
b) Menejer uchun (o'zi va jamoasining vazifalari):

json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "title": "Kitob o'qish",
      "description": "Python darsligini o'qish",
      "status": "pending",
      "priority": "high",
      "category": "study",
      "due_date": "2024-12-20",
      "created_at": "2024-12-15T10:30:00Z",
      "created_by": {
        "id": 1,
        "email": "ali@example.com",
        "first_name": "Ali"
      },
      "assigned_to": {
        "id": 2,
        "email": "vali@example.com",
        "first_name": "Vali"
      }
    }
  ]
}
2.2. YANGI VAZIFA YARATISH
text
POST /api/todos/
Headers:
text
Authorization: Token abc123def456
Content-Type: application/json
Request Body:
json
{
  "title": "Mashina yuvish",
  "description": "Mashinani tozalash va yuvish",
  "priority": "medium",
  "category": "home",
  "due_date": "2024-12-18"
}
Response (201 Created):
json
{
  "id": 10,
  "title": "Mashina yuvish",
  "description": "Mashinani tozalash va yuvish",
  "status": "pending",
  "priority": "medium",
  "category": "home",
  "due_date": "2024-12-18",
  "created_at": "2024-12-15T11:00:00Z",
  "created_by": 1,
  "assigned_to": null
}
Menejer uchun (boshqaga topshirish):
json
{
  "title": "Hisobot tayyorlash",
  "description": "Oy hisobotini tayyorlash",
  "priority": "high",
  "category": "work",
  "due_date": "2024-12-20",
  "assigned_to": 3
}
2.3. BITTA VAZIFANI OLISH
text
GET /api/todos/{id}/
Headers:
text
Authorization: Token abc123def456
Response (200 OK):
json
{
  "id": 1,
  "title": "Kitob o'qish",
  "description": "Python darsligini 50 bet o'qish",
  "status": "pending",
  "priority": "high",
  "category": "study",
  "due_date": "2024-12-20",
  "created_at": "2024-12-15T10:30:00Z",
  "updated_at": "2024-12-15T10:30:00Z",
  "created_by": {
    "id": 1,
    "email": "ali@example.com",
    "first_name": "Ali",
    "role": "USER"
  },
  "assigned_to": null
}
2.4. VAZIFANI YANGILASH
text
PUT /api/todos/{id}/
Headers:
text
Authorization: Token abc123def456
Content-Type: application/json
Request Body:
json
{
  "title": "Kitob o'qish (yangilandi)",
  "description": "Python darsligini 100 bet o'qish",
  "status": "in_progress",
  "priority": "high",
  "category": "study",
  "due_date": "2024-12-25"
}
Response (200 OK): Yangilangan vazifa ma'lumotlari
2.5. VAZIFANI O'CHIRISH
text
DELETE /api/todos/{id}/
Headers:
text
Authorization: Token abc123def456
Response (204 No Content): Hech qanday content qaytmaydi
3. MAXSUS OPERATSIYALAR
3.1. VAZIFA HOLATINI O'ZGARTIRISH
text
PATCH /api/todos/{id}/status/
Headers:
text
Authorization: Token abc123def456
Content-Type: application/json
Request Body:
json
{
  "status": "completed"
}
Response (200 OK):
json
{
  "id": 1,
  "title": "Kitob o'qish",
  "status": "completed",
  "updated_at": "2024-12-15T12:00:00Z"
}
3.2. VAZIFANI BOSHQA FOYDALANUVCHIGA TOPSHIRISH
text
PATCH /api/todos/{id}/assign/
Headers:
text
Authorization: Token abc123def456
Content-Type: application/json
Request Body:
json
{
  "assigned_to": 5
}
Response (200 OK):
json
{
  "id": 1,
  "title": "Hisobot tayyorlash",
  "assigned_to": {
    "id": 5,
    "email": "guli@example.com",
    "first_name": "Guli"
  },
  "updated_at": "2024-12-15T13:00:00Z"
}
3.3. VAZIFA DARAJASINI O'ZGARTIRISH
text
PATCH /api/todos/{id}/priority/
Request Body:
json
{
  "priority": "high"
}
4. STATISTIKA VA FILTRLAR
4.1. VAZIFALAR STATISTIKASI
text
GET /api/todos/statistics/
Response:
json
{
  "total": 15,
  "completed": 8,
  "pending": 5,
  "in_progress": 2,
  "completion_rate": 53.3,
  "by_priority": {
    "high": 3,
    "medium": 8,
    "low": 4
  },
  "by_category": {
    "work": 5,
    "personal": 4,
    "home": 3,
    "study": 3
  }
}
4.2. BUGUNGI VAZIFALAR
text
GET /api/todos/today/
Query Parameters:
priority=high (faqat yuqori darajali)

category=work (faqat ish kategoriyasi)

Response: Bugun muddati bor vazifalar ro'yxati
4.3. KECHIKKAN VAZIFALAR
text
GET /api/todos/overdue/
Response: Muddati o'tgan lekin bajarilmagan vazifalar
4.4. YAQIN KELGUSI VAZIFALAR
text
GET /api/todos/upcoming/
Query Parameters:
days=7 (keyingi 7 kun ichidagi vazifalar)

5. ROL BO'YICHA CHEKLAR
5.1. USER (Oddiy foydalanuvchi)
Ko'ra oladi: Faqat o'zi yaratgan vazifalarni

Yarata oladi: Yangi vazifa

Yangilay oladi: Faqat o'z vazifalarini

O'chira oladi: Faqat o'z vazifalarini

Topshira oladi: Kimsaga topshira OLMAYDI

5.2. STAFF (Xodim)
Ko'ra oladi: O'ziga topshirilgan vazifalarni

Yangilay oladi: Faqat o'ziga topshirilgan vazifalarning holatini

5.3. MANAGER (Menejer)
Ko'ra oladi: O'zi va jamoasining barcha vazifalarini

Yarata oladi: O'zi uchun va jamoa a'zolari uchun

Yangilay oladi: Jamoaning barcha vazifalarini

Topshira oladi: Jamoa a'zolariga vazifa topshirishi mumkin

O'chira oladi: Jamoaning barcha vazifalarini

5.4. ADMIN (Administrator)
Ko'ra oladi: BARCHA vazifalarni (hamma foydalanuvchilarniki)

Yarata oladi: Kimga istasa vazifa yarata oladi

Yangilay oladi: BARCHA vazifalarni

O'chira oladi: BARCHA vazifalarni

Boshqara oladi: Barcha operatsiyalar

6. XATOLIK RESPONSE LARI
401 Unauthorized
json
{
  "error": "Authentication required",
  "detail": "Token not provided or invalid"
}
403 Forbidden
json
{
  "error": "Permission denied",
  "detail": "You can only access your own tasks",
  "your_id": 1,
  "task_owner_id": 3
}
404 Not Found
json
{
  "error": "Task not found",
  "detail": "Task with id 999 does not exist"
}
400 Bad Request
json
{
  "error": "Validation error",
  "detail": {
    "title": ["This field is required"],
    "priority": ["Must be one of: low, medium, high"],
    "due_date": ["Date cannot be in the past"]
  }
}
429 Too Many Requests
json
{
  "error": "Rate limit exceeded",
  "detail": "Maximum 100 requests per minute allowed"
}
7. QUERY MISOL QIDIRUVLARI
Faqat bajarilmagan yuqori darajali vazifalar:
text
GET /api/todos/?status=pending&priority=high
Ish kategoriyasida "hisobot" so'zini qidirish:
text
GET /api/todos/?category=work&search=hisobot
Menejer uchun jamoaning vazifalari:
text
GET /api/todos/?assigned_to=team&status=in_progress
Keyingi haftadagi vazifalar:
text
GET /api/todos/?due_date=2024-12-16&due_date=2024-12-22
Faqat o'zimga topshirilgan vazifalar:
text
GET /api/todos/?assigned_to=me
Barcha vazifalar (faqat Admin):
text
GET /api/todos/?all=true
