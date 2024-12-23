from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class UserRole(models.Model):
    user_id = models.PositiveIntegerField()  # Menyimpan ID User
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    assigned_at = models.DateTimeField(auto_now_add=True)  # Timestamp untuk relasi

    def __str__(self):
        return f"User ID: {self.user_id}, Role: {self.role.name}"