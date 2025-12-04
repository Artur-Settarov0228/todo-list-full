from rest_framework.views import APIView          # DRF APIView — oddiy class-based view
from rest_framework.request import Request        # Request tipi
from rest_framework.response import Response      # JSON javob qaytarish
from rest_framework import status                 # HTTP status kodlari

from .serializers import RegisterSerializer, UserSerializer   # Kerakli serializerlar


class RegisterView(APIView):                      # User ro‘yxatdan o‘tish viewsi
    def post(self, request: Request) -> Response: # POST metodi
        serializer = RegisterSerializer(data=request.data)  
        # Kelgan ma'lumotlardan serializer yaratamiz

        if serializer.is_valid(raise_exception=True):  
            # validatsiya — agar xato bo‘lsa DRF avtomatik exception chiqaradi

            user = serializer.save()              # valid bo‘lsa, yangi userni yaratamiz

            user_json = UserSerializer(user).data
            # Yaratilgan userni JSON formatga o‘tkazamiz (kerak bo‘lsa qaytarish uchun)

            return Response(user_json, status=status.HTTP_201_CREATED)
            # 201 — muvaffaqiyatli yaratildi
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
        # Valid bo‘lmasa, 400 (yomon so‘rov) qaytaramiz

