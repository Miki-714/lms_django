# Generated by Django 5.0.7 on 2024-08-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_book_barcode_alter_book_cl_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='Barcode',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Cl_No',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Description',
            field=models.CharField(default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Keyword',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Language',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Page_count',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Price',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Profile_pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='book_images/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='Publication_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Publication_place',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Publisher',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Subject',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Subtitle',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='Title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('History', 'History')], default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='dimensions',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]
