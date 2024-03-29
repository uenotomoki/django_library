# Generated by Django 2.2.4 on 2019-08-24 04:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Docindex',
            fields=[
                ('isbn', models.CharField(max_length=13, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('[0-9]{13}', 'isbn番号は13桁の数字で入力してください')])),
                ('name', models.CharField(max_length=100)),
                ('type_code', models.IntegerField(validators=[django.core.validators.RegexValidator('[0-9]{1}', '分類コードは1桁の数字を入力してください')])),
                ('author', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('publication_day', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Doclist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_day', models.DateField(auto_now_add=True)),
                ('disposal_day', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('docindex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Docindex')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('post_number', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator('[0-9]{3}-[0-9]{4}', '正しい形式(ooo-oooo)で入力してください。')])),
                ('address', models.CharField(max_length=60)),
                ('tel_number', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('[0-9]{2,4}-[0-9]{3,4}-[0-9]{3,4}', '[-]つきの形式で入力してください。')])),
                ('email', models.EmailField(max_length=30)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('entry_day', models.DateField(auto_now_add=True)),
                ('quit_day', models.DateField(blank=True, null=True)),
                ('password', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('[a-zA-Z0-9]{8,16}')])),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Reservelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve_day', models.DateField(auto_now_add=True)),
                ('lent', models.BooleanField(default=False)),
                ('cancel', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('docindex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Docindex')),
                ('doclist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.Doclist')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Lendlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lend_day', models.DateField(auto_now_add=True)),
                ('return_limit', models.DateField()),
                ('return_day', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('doclist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Doclist')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.CharField(max_length=144)),
                ('docindex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Docindex')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Member')),
            ],
        ),
    ]
