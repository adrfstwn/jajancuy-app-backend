from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'role'
        
    def __str__(self):
        return self.name
    
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Menyimpan ID User
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    assigned_at = models.DateTimeField(auto_now_add=True)  # Timestamp untuk relasi
    
    class Meta:
        db_table = 'role_user'
        constraints = [
            models.UniqueConstraint(fields=['user', 'role'], name='unique_user_role')
        ]

    def __str__(self):
        return f"User Id: {self.user}, Role: {self.role.name}"

    
class InfoUser(models.Model):
    
    class Meta:
        db_table = 'info_user'
        
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)