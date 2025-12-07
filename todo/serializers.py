from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',          
            'username',    
            'email',       
            'first_name',  
            'last_name',   
            'role',        
            'is_active',   
            'date_joined', 
        ]

class TaskSerializer(serializers.ModelSerializer):
    yaratgan = UserSerializer(read_only = True)
    tayinlajgan = UserSerializer(read_only = True)
    tayinlangan_id = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all(), source = 'tayinlangan', write_only = True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
