from rest_framework import serializers          # DRF serializerlarini import qilamiz
from django.contrib.auth import get_user_model  # User modelini olish uchun funktsiya

User = get_user_model()                         # Django'dagi User modelini dinamik tarzda olamiz

class RegisterSerializer(serializers.ModelSerializer):   # Ro'yxatdan o'tish uchun serializer
    confirm = serializers.CharField(max_length=128)     # Parolni qayta kiritish uchun maydon (modelda yo'q)

    class Meta:
        model = User                                     # Qaysi model bilan ishlashini ko'rsatamiz
        fields = ['username', 'password', 'confirm', 'email', 'first_name', 'last_name']  
        # Foydalanuvchi kiritadigan maydonlar ro'yxati

    def validate(self, attrs):                           # Validatsiya metodini override qilamiz
        if attrs['password'] != attrs['confirm']:        # Password va Confirm teng emasligini tekshiramiz
            raise serializers.ValidationError('password bilan confirm qismi teng emas') 
            # Agar teng bo'lmasa xatolik chiqaradi
            
        return super().validate(attrs)                   # Qolgan DRF validatsiyalarini ham ishlatadi

    def create(self, validated_data):                    # Yangi user yaratish jarayoni
        validated_data.pop('confirm')                    # Confirm passwordni o'chirib tashlaymiz (modelda yo'q)
        password = validated_data.pop('password')        # Passwordni ajratib olamiz
        user = User(**validated_data)                    # Qolgan ma'lumotlar bilan User obyektini yaratamiz
        user.set_password(password)                      # Parolni hash qilib saqlaymiz (oddiy matn emas!)
        user.save()                                      # Userni DB ga saqlaymiz

        return user                                      # Yaratilgan user obyektini qaytaramiz
    

class UserSerializer(serializers.ModelSerializer):       # Oddiy User serializer
    class Meta:
        model = User                                     # Qaysi modeldan foydalanishni ko'rsatish
        fields = '__all__'                               # Barcha model maydonlarini chiqaradi


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)    # Login uchun username maydoni
    password = serializers.CharField(max_length=128)    # Login uchun password maydoni


class Profileserializer(serializers.Serializer):
    class Meta:
        model = User
        exclude = ["password",'role', 'groups', 'user_permissions', 'is_staff', 'is_superuser']                            # Parol maydonini chiqarishdan chiqarib tashlaymiz
        extra_kwargs = {
            'username' :{
                "required": False
            }
        }

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confirm = serializers.CharField(max_length=128)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm']:
            raise serializers.ValidationError("yangi parol bilan confirm parol teng emas qaytdan urinib kuring")
        
        return super().validate(attrs)

