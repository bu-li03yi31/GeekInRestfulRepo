# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('cid', models.AutoField(serialize=False, primary_key=True, db_column='Cid')),
                ('email', models.CharField(max_length=100, null=True, db_column='Email', blank=True)),
                ('content', models.TextField(null=True, db_column='Content', blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, null=True, db_column='TimeStamp', blank=True)),
            ],
            options={
                'db_table': 'Comments',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('fid', models.AutoField(serialize=False, primary_key=True, db_column='Fid')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, db_column='TimeStamp', blank=True)),
            ],
            options={
                'db_table': 'Following',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('lid', models.AutoField(serialize=False, primary_key=True, db_column='Lid')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, db_column='TimeStamp', blank=True)),
            ],
            options={
                'db_table': 'Likes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('auto_increment_id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('pid', models.AutoField(serialize=False, primary_key=True, db_column='Pid')),
                ('email', models.CharField(max_length=100, null=True, db_column='Email', blank=True)),
                ('content', models.TextField(null=True, db_column='Content', blank=True)),
                ('photo', models.CharField(max_length=100, null=True, db_column='Photo', blank=True)),
                ('title', models.CharField(max_length=100, null=True, db_column='Title', blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, null=True, db_column='TimeStamp', blank=True)),
            ],
            options={
                'db_table': 'Posts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PostTags',
            fields=[
                ('ptid', models.AutoField(serialize=False, primary_key=True, db_column='PTid')),
                ('pid', models.ForeignKey(db_column='Pid', blank=True, to='GeekInRest.Posts', null=True)),
            ],
            options={
                'db_table': 'Post_Tags',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('tid', models.AutoField(serialize=False, primary_key=True, db_column='Tid')),
                ('tag', models.CharField(max_length=50, null=True, db_column='Tag', blank=True)),
            ],
            options={
                'db_table': 'Tags',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('email', models.CharField(max_length=100, serialize=False, primary_key=True, db_column='Email')),
                ('photo', models.CharField(max_length=100, null=True, db_column='Photo', blank=True)),
                ('password', models.CharField(max_length=20, null=True, db_column='Password', blank=True)),
                ('username', models.CharField(max_length=100, null=True, db_column='Username', blank=True)),
            ],
            options={
                'db_table': 'Users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserTags',
            fields=[
                ('utid', models.AutoField(serialize=False, primary_key=True, db_column='UTid')),
                ('email', models.ForeignKey(db_column='Email', blank=True, to='GeekInRest.Users', null=True)),
                ('tid', models.ForeignKey(to='GeekInRest.Tags', db_column='Tid')),
            ],
            options={
                'db_table': 'User_Tags',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='posttags',
            name='tid',
            field=models.ForeignKey(db_column='Tid', blank=True, to='GeekInRest.Tags', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='GuestEmail',
            field=models.ForeignKey(related_name='guest', to='GeekInRest.Users', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='HostEmail',
            field=models.ForeignKey(related_name='host', to='GeekInRest.Users', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='Pid',
            field=models.ForeignKey(to='GeekInRest.Posts'),
        ),
        migrations.AddField(
            model_name='likes',
            name='email',
            field=models.ForeignKey(to='GeekInRest.Users', db_column='Email'),
        ),
        migrations.AddField(
            model_name='likes',
            name='pid',
            field=models.ForeignKey(to='GeekInRest.Posts', db_column='Pid'),
        ),
        migrations.AddField(
            model_name='following',
            name='followee',
            field=models.ForeignKey(related_name='user2', db_column='Followee', to='GeekInRest.Users'),
        ),
        migrations.AddField(
            model_name='following',
            name='follower',
            field=models.ForeignKey(related_name='user1', db_column='Follower', to='GeekInRest.Users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='pid',
            field=models.ForeignKey(db_column='Pid', blank=True, to='GeekInRest.Posts', null=True),
        ),
    ]
