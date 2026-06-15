from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Register your models here.
@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == "your_app_name":  # Replace "your_app_name" with your actual app name
        admin_group, created_admin = Group.objects.get_or_create(name='Admin')
        user_group, created_user = Group.objects.get_or_create(name='User')

        # Assign permissions to Admin group only if it was newly created
        if created_admin:
            content_type = ContentType.objects.get_for_model(User)
            permissions = Permission.objects.filter(content_type=content_type)
            admin_group.permissions.set(permissions)
            admin_group.save()