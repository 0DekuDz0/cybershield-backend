from django.test import TestCase
from api.models import Admin

admin = Admin.objects.create_user(email="root2@gmail.com", name="root", password="root")
print(f"Admin Created: {admin.email}  admin password {admin.password} is staff {admin.is_staff} is superuser {admin.is_superuser}")