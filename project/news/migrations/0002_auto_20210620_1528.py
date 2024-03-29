# Generated by Django 3.2.3 on 2021-06-20 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classTrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('userTrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscriver',
            field=models.ManyToManyField(through='news.CategorySubscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]
