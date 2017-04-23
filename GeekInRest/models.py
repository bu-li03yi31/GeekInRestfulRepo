# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import datetime


class Comments(models.Model):
    cid = models.AutoField(db_column='Cid', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pid = models.ForeignKey('Posts', db_column='Pid', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='TimeStamp',default=datetime.datetime.now, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Comments'


class Following(models.Model):
    fid = models.IntegerField(db_column='Fid', primary_key=True)  # Field name made lowercase.
    follower = models.CharField(db_column='Follower', max_length=100, blank=True, null=True)  # Field name made lowercase.
    followee = models.CharField(db_column='Followee', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp',default=datetime.datetime.now,blank=True)
    class Meta:
        managed = True
        db_table = 'Following'


class Likes(models.Model):
    lid = models.AutoField(db_column='Lid', primary_key=True)  # Field name made lowercase.
    pid = models.IntegerField(db_column='Pid', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp', default=datetime.datetime.now,blank=True)

    class Meta:
        managed = True
        db_table = 'Likes'


class PostTags(models.Model):
    ptid = models.IntegerField(db_column='PTid', primary_key=True)  # Field name made lowercase.
    pid = models.ForeignKey('Posts', db_column='Pid', blank=True, null=True)  # Field name made lowercase.
    tid = models.ForeignKey('Tags', db_column='Tid', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Post_Tags'


class Tags(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    tag = models.CharField(db_column='Tag', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Tags'

#TID FOREIGN KEY
class UserTags(models.Model):
    utid = models.IntegerField(db_column='UTid', primary_key=True)  # Field name made lowercase.
    email = models.ForeignKey('Users', db_column='Email', blank=True, null=True)  # Field name made lowercase.
    #tid = models.IntegerField(db_column='Tid', blank=True, null=True)  # Field name made lowercase.
    tid = models.ForeignKey(Tags)
    class Meta:
        managed = True
        db_table = 'User_Tags'


class Users(models.Model):
    email = models.CharField(db_column='Email', primary_key=True, max_length=100)  # Field name made lowercase.
    photo = models.CharField(db_column='Photo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=20, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Users'



class Posts(models.Model):
    pid = models.AutoField(db_column='Pid', primary_key=True)  # Field name made lowercase.
    #email should be foreign key
    #email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    email = models.ForeignKey(Users)
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(db_column='Photo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='TimeStamp',default=datetime.datetime.now,  blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Posts'



class Notification(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    HostEmail = models.ForeignKey(Users,null=True,related_name='host')
    GuestEmail = models.ForeignKey(Users,null=True,related_name='guest')
    Pid = models.ForeignKey(Posts)
    type = models.IntegerField()

# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'django_migrations'
