from django.contrib.auth import authenticate                     # Django funksiyasi: username va password orqali foydalanuvchini tekshiradi
from rest_framework.views import APIView                          # DRF class-based view yaratish uchun
from rest_framework.request import Request                        # DRF request obyekti
from rest_framework.response import Response                      # DRF JSON javob uchun
from rest_framework import status                                 # HTTP status kodlari
from rest_framework.authtoken.models import Token                 # DRF token modeli
from rest_framework.authentication import TokenAuthentication     # DRF token bilan autentifikatsiya

from .serializers import RegisterSerializer, UserSerializer , LoginSerializer  # Serializerlar

class RegisterView(APIView):                      # User ro‘yxatdan o‘tish viewsi
    def post(self, request: Request) -> Response: # POST metodi
        serializer = RegisterSerializer(data=request.data)  # Serializer orqali ma’lumotlarni tekshiradi

        if serializer.is_valid(raise_exception=True):       # Agar ma’lumot to‘g‘ri bo‘lsa davom etadi
            user = serializer.save()                        # Yangi foydalanuvchi yaratadi
            user_json = UserSerializer(user).data           # Userni JSON formatga o‘tkazadi
            return Response(user_json, status=status.HTTP_201_CREATED)  # 201 — muvaffaqiyatli yaratildi
        
        return Response(status=status.HTTP_400_BAD_REQUEST) # 400 — noto‘g‘ri ma’lumot

class LoginView(APIView):                             # Foydalanuvchi login qiladigan view
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)  # Login ma’lumotlarini tekshiradi

        if serializer.is_valid(raise_exception=True):    # Agar validatsiya to‘g‘ri bo‘lsa
            data = serializer.validated_data             # Validatsiyadan o‘tgan ma’lumot
            user = authenticate(username=data['username'], password=data['password'])  
            # Foydalanuvchi mavjudligini va parol to‘g‘riligini tekshiradi

            if user is not None:                         # Agar foydalanuvchi topilsa
                token, created = Token.objects.get_or_create(user=user)  
                # Foydalanuvchiga token beradi yoki mavjud tokenni oladi
                return Response({'token': token.key}, status=status.HTTP_200_OK)  
                # Tokenni JSON formatda qaytaradi
            
            return Response(status=status.HTTP_401_UNAUTHORIZED)  
            # 401 — noto‘g‘ri login/parol

        return Response(status=status.HTTP_404_NOT_FOUND)  
        # 404 — serializer ma’lumotni topa olmasa

class LogoutView(APIView):                           # Foydalanuvchi logout qiladigan view
    authentication_classes = [TokenAuthentication]   # Token orqali autentifikatsiya talab qilinadi

    def post(self, request: Request) -> Response:
        request.user.auth_token.delete()             # Foydalanuvchining tokenini o‘chiradi
        return Response(status=status.HTTP_204_NO_CONTENT)  
        # 204 — muvaffaqiyatli logout, body yo‘q
