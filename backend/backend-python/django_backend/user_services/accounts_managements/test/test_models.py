from django.test import TestCase
from ..models import Role, UserRole
from django.contrib.auth.models import User
from django.db import IntegrityError
        
class InputRoleModelTest(TestCase):
    
    def setUp(self):
        self.role = Role.objects.create(name="Developer", description="Developer Internal Role")
        
    def test_role_success_create(self):
        role = Role.objects.get(id=self.role.id)
        self.assertEqual(role.name, "Developer")
        self.assertEqual(role.description, "Developer Internal Role")
        
    def test_role_str_method(self):
        self.assertEqual(str(self.role), "Developer")
        
    def test_role_missing_fields(self):
        with self.assertRaises(IntegrityError):
            Role.objects.create()
        
    
class InputUserRoleModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="johndoe", password="password123")
        self.role = Role.objects.create(name="Developer", description="Developer Internal Role")
        
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        
    def test_user_role_create(self):
        user_role = UserRole.objects.get(id=self.user_role.id)
        self.assertEqual(user_role.user, self.user)
        self.assertEqual(user_role.role, self.role)
        
    def test_user_role_str_method(self):
        self.assertEqual(str(self.user_role), f"User Id: {self.user.id}, Role: {self.role.name}")
        
class RelationUserRoleModelTestCase(TestCase):

    def setUp(self):
        # Membuat User dan Role
        self.user = User.objects.create(username="johndoe", password="password123")
        self.role1 = Role.objects.create(name="Admin", description="Administrator role")
        self.role2 = Role.objects.create(name="Editor", description="Editor role")

        # Membuat UserRole untuk menghubungkan User dengan Role
        self.user_role1 = UserRole.objects.create(user=self.user, role=self.role1)
        self.user_role2 = UserRole.objects.create(user=self.user, role=self.role2)

    def test_user_roles_relation(self):
        # Memastikan user memiliki 2 roles
        user_roles = UserRole.objects.filter(user=self.user)
        self.assertEqual(user_roles.count(), 2)
        self.assertTrue(user_roles.filter(role=self.role1).exists())
        self.assertTrue(user_roles.filter(role=self.role2).exists())
    
class RemoveUserRoleModelTestCase(TestCase):

    def setUp(self):
        # Membuat User dan Role
        self.user = User.objects.create(username="johndoe", password="password123")
        self.role = Role.objects.create(name="Admin", description="Administrator role")
        # Membuat UserRole
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)

    def test_user_role_deletion_on_role_delete(self):
        # Menghapus Role
        self.role.delete()
        # Memastikan UserRole juga terhapus
        with self.assertRaises(UserRole.DoesNotExist):
            UserRole.objects.get(id=self.user_role.id)
            
    def test_user_role_deletion_on_user_delete(self):
        self.user.delete()
        with self.assertRaises(UserRole.DoesNotExist):
            UserRole.objects.get(id=self.user_role.id)

class UniqueUserRoleModelTestCase(TestCase):

    def setUp(self):
        # Membuat User dan Role
        self.user = User.objects.create(username="johndoe", password="password123")
        self.role = Role.objects.create(name="Admin", description="Administrator role")

    def test_user_role_unique_constraint(self):
        # Membuat UserRole pertama
        UserRole.objects.create(user=self.user, role=self.role)
        
        # Memastikan bahwa duplikat tidak bisa dibuat
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(user=self.user, role=self.role)
            
    def test_user_role_with_invalid_data(self):
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(user_id=999, role=self.role)  # Non-existent user
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(user=self.user, role_id=999)