# Generated by Django 3.2.19 on 2023-06-20 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banque', '0002_remove_compte_client_delete_personnel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=100)),
                ('solde', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Virement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('compte_destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='virements_recus', to='banque.compte')),
                ('compte_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='virements_envoyes', to='banque.compte')),
            ],
        ),
        migrations.CreateModel(
            name='Prelevement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('compte_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banque.compte')),
            ],
        ),
    ]
