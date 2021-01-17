# Generated by Django 3.0.8 on 2020-08-19 16:10

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profanity.validators
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('cargo', models.CharField(max_length=100, verbose_name='Cargo')),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
            },
        ),
        migrations.CreateModel(
            name='CategoriaProduto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('categoria', models.CharField(max_length=50, verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Categoria Produto',
                'verbose_name_plural': 'Categoria Produtos',
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('email_registro', models.EmailField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Newsletter',
                'verbose_name_plural': 'Newsletters',
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=50)),
                ('testemunho', models.CharField(max_length=100)),
                ('foto', stdimage.models.StdImageField(upload_to=core.models.get_file_path, verbose_name='Foto')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
            },
        ),
        migrations.CreateModel(
            name='TipoProduto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('tipo', models.CharField(max_length=50, verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Tipo Produto',
                'verbose_name_plural': 'Tipos Produtos',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=30)),
                ('descricao', models.CharField(max_length=100)),
                ('informacao', models.CharField(max_length=200)),
                ('imagem1', stdimage.models.StdImageField(upload_to=core.models.get_file_path, verbose_name='Imagem1')),
                ('imagem2', stdimage.models.StdImageField(blank=True, null=True, upload_to=core.models.get_file_path, verbose_name='Imagem2')),
                ('imagem3', stdimage.models.StdImageField(blank=True, null=True, upload_to=core.models.get_file_path, verbose_name='Imagem3')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8)),
                ('preco_desconto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CategoriaProduto', verbose_name='Categoria')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TipoProduto', verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('imagem', stdimage.models.StdImageField(upload_to=core.models.get_file_path, verbose_name='Imagem')),
                ('facebook', models.CharField(default='#', max_length=100, verbose_name='Facebook')),
                ('twitter', models.CharField(default='#', max_length=100, verbose_name='Twitter')),
                ('google', models.CharField(default='#', max_length=100, verbose_name='Google')),
                ('pinterest', models.CharField(default='#', max_length=100, verbose_name='Pinterest')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Cargo', verbose_name='Cargo')),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criados', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('comentario', models.CharField(max_length=100, validators=[profanity.validators.validate_is_profane])),
                ('nota', models.CharField(choices=[('1', 'rating1'), ('2', 'rating2'), ('3', 'rating3'), ('4', 'rating4'), ('5', 'rating5')], max_length=1)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Produto', verbose_name='Produto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
