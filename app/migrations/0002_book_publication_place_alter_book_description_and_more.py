# Generated by Django 5.0.7 on 2024-08-21 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='Publication_place',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Description',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Keyword',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Language',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Page_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Publisher',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Subject',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Subtitle',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('History', 'History')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='dimensions',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
