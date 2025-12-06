from rest_framework.permissions import BasePermission

class Is_Admin(BasePermission):
    message = "siz admin emasiz foydalanish mumkim. emas!"

    def has_permission(self, request, view):
        return request.user and request.user.is_admin
    
class Is_Manager(BasePermission):
     mesage = "siz manager emasiz foydalamish mumkim emas"

     def has_permission(self, request, view):
         return request.user and request.user.is_manager 

class Is_User(BasePermission):
    mesager = "siz usersiz. "

    def has_permission(self, request, view):
        return request.user and request.user.is_user   
    

class IsStaff(BasePermission):
    message = 'siz staff emassiz'

    def has_permission(self, request, view):
        return request.user and not (request.user.is_amdin or request.user.is_manager)
    
        