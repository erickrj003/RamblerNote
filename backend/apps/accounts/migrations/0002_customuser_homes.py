from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('notes', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='homes',
            field=models.ManyToManyField(blank=True, to='notes.home'),
        ),
    ] 