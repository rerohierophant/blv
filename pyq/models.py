# coding = utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    pyq = models.ForeignKey('Pyq', models.DO_NOTHING, blank=True, null=True)
    commenter = models.CharField(max_length=20, blank=True, null=True)
    comment_content = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Img(models.Model):
    img_id = models.AutoField(primary_key=True)
    pyq = models.ForeignKey('Pyq', models.DO_NOTHING, blank=True, null=True)
    img_url = models.CharField(max_length=2048, blank=True, null=True)
    type = models.CharField(max_length=40, blank=True, null=True)
    sorted_objs = models.CharField(max_length=2048, blank=True, null=True)
    # elements = models.CharField(max_length=2000, blank=True, null=True)
    # elements_cn = models.CharField(max_length=2000, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'img'


class Pyq(models.Model):
    pyq_id = models.AutoField(primary_key=True)
    poster = models.CharField(max_length=20, blank=True, null=True)
    poster_avatar = models.CharField(max_length=2048, blank=True, null=True)
    content = models.CharField(max_length=2048, blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pyq'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description_style = models.CharField(max_length=20, blank=True, null=True)
    aesthetics = models.BooleanField(default=False)
    emotional = models.BooleanField(default=False)
    Confidence = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'user_profile'