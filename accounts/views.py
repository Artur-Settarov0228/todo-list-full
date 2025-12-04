
from rest_framework.views import APIView          # DRF APIView — oddiy class-based view
from rest_framework.request import Request        # Request tipi
from rest_framework.response import Response      # JSON javob qaytarish
from rest_framework import status                 # HTTP status kodlari
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from .serializers import RegisterSerializer, UserSerializer , LoginSerializer  # Kerakli serializerlar


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

class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data = request.data)   

        if serializer.is_valid(raise_exception= True):

            data = serializer.validated_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                token = Token.objects.create(user=user)
                print(token.key) 
                return Response({'token': token.key },status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)    

