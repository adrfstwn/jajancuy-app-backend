from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
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
        return f"User Id: {self.user_id}, Role: {self.role.name}"

    
class InfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relasi one-to-one dengan user
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)  # Untuk menyimpan link media sosial dalam format JSON
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    class Meta:
        db_table = 'info_user'

    def __str__(self):
        return f"Info for {self.user.username}"