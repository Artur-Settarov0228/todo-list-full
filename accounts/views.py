from django.contrib.auth.hashers import check_password

from django.contrib.auth import authenticate                     # Django funksiyasi: username va password orqali foydalanuvchini tekshiradi
from rest_framework.views import APIView                          # DRF class-based view yaratish uchun
from rest_framework.request import Request                        # DRF request obyekti
from rest_framework.response import Response                      # DRF JSON javob uchun
from rest_framework import status                                 # HTTP status kodlari
from rest_framework.authtoken.models import Token                 # DRF token modeli
from rest_framework.authentication import TokenAuthentication     # DRF token bilan autentifikatsiya
from .permissions import Is_Admin, Is_User, Is_Manager, IsStaff

from .serializers import RegisterSerializer, UserSerializer , LoginSerializer, Profileserializer, ChangePasswordSerializer# Serializerlar

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
class ProfileView(APIView):  # ProfileView – foydalanuvchi profilini ko‘rsatish va yangilash uchun APIView
    authentication_classes = [TokenAuthentication]  # Foydalanuvchi token orqali tizimga kirgan bo‘lishi kerak

    def post(self, request: Request) -> Response:  # POST so‘rovi – foydalanuvchi ma’lumotlarini olish
        user = request.user  # Token orqali tizimga kirgan foydalanuvchini oladi
        serializer = UserSerializer(user)  # Foydalanuvchi ma’lumotlarini JSON shakliga o‘tkazadi
        return Response(serializer.data)  # Seriyalizatsiya qilingan ma’lumotlarni qaytaradi
    
    def put(self, request: Request) -> Response:  # PUT so‘rovi – foydalanuvchi profilini yangilash
        user = request.user  # Token orqali foydalanuvchi obyektini oladi
        serializer = Profileserializer(data=request.data, partal=True)  # Ma’lumotlarni serializer orqali tekshiradi
        if serializer.is_valid(raise_exception=True):  # Agar ma’lumotlar to‘g‘ri bo‘lsa davom etadi
            update_user = serializer.update(user , serializer.validated_data)  # Foydalanuvchi ob’ektini yangilaydi
        
        serializer = UserSerializer(update_user)  # Yangilangan ma’lumotlarni JSON shakliga o‘tkazadi
        return Response(serializer.data)  # Yangilangan ma’lumotlarni qaytaradi

class PasswordChangeView(APIView):  # PasswordChangeView – foydalanuvchi parolini o‘zgartirish
    authentication_classes = [TokenAuthentication]  # Foydalanuvchi token orqali tizimga kirgan bo‘lishi kerak

    def post(self, request:Request) -> Response:  # POST so‘rovi – parolni o‘zgartirish
        serializer = ChangePasswordSerializer(data = request.data)  # Kelgan ma’lumotlarni serializer orqali tekshiradi

        if serializer.is_valid(raise_exception=True):  # Agar ma’lumotlar to‘g‘ri bo‘lsa davom etadi
            user = request.user  # Token orqali foydalanuvchi ob’ektini oladi

            if not check_password(serializer.validated_data['password'], user.password):  # Hozirgi parolni tekshiradi
                return Response('parol xato qaytadan kiriting!', status=status.HTTP_400_BAD_REQUEST)  # Xato xabar qaytaradi
            
            user.set_password(serializer.validated_data['new_password'])  # Yangi parolni hash qilib saqlaydi
            user.save()  # Foydalanuvchi ob’ektini bazaga saqlaydi
            
            return Response("parol o'zgardi ", status=status.HTTP_204_NO_CONTENT)  # Muvaffaqiyatli xabar qaytaradi


class AdminPanelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Is_Admin]

    def get(self, request: Request) -> Response:
        return Response('xush kelibsiz adminlikga', status=status.HTTP_200_OK)
    
class ManagmentPanelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Is_Manager]

    def get(self, requestz: Request) -> Response:
        return Response('xush keibsiz managerlikga ')

class StaffzoneUserPanelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Is_User]

    def get(self, request:Request) -> Response:
        return Response("xush kelibsiz")  

class Staffzone(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsStaff]
    def get(self, request: Request) -> Response:
        
        return Response(' Xush kelibsiz jamoga tabriklaymiz endi birga ishlaymiz ')
     

              