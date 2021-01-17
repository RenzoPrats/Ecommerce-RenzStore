from django.contrib import admin
from core.models import Funcionario, CategoriaProduto, Cargo, Testimonial, Produto, TipoProduto, Newsletter, Avaliacao
from django.contrib import admin


@admin.register(Newsletter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email_registro', 'ativo')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'ativo', 'modificado')


@admin.register(TipoProduto)
class TipoProdutoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'ativo', 'modificado')


@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'ativo', 'modificado')


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'ativo', 'modificado')


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'preco_desconto', 'ativo', 'modificado', 'criados')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'modificado')


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'criados', 'ativo')
