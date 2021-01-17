from django.db import models
from stdimage.models import StdImageField
import uuid
from profanity.validators import validate_is_profane


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class Base(models.Model):
    criados = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Cargo(Base):
    cargo = models.CharField('Cargo', max_length=100)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.cargo


class Funcionario(Base):
    nome = models.CharField('Nome', max_length=100)
    cargo = models.ForeignKey('core.Cargo', verbose_name='Cargo', on_delete=models.CASCADE)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 150, 'height': 150, 'crop': True}})
    facebook = models.CharField('Facebook', max_length=100, default='#')
    twitter = models.CharField('Twitter', max_length=100, default='#')
    google = models.CharField('Google', max_length=100, default='#')
    pinterest = models.CharField('Pinterest', max_length=100, default='#')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return self.nome


class TipoProduto(Base):
    tipo = models.CharField('Tipo', max_length=50)

    class Meta:
        verbose_name = 'Tipo Produto'
        verbose_name_plural = 'Tipos Produtos'

    def __str__(self):
        return self.tipo


class CategoriaProduto(Base):
    categoria = models.CharField('Categoria', max_length=50)

    class Meta:
        verbose_name = 'Categoria Produto'
        verbose_name_plural = 'Categoria Produtos'

    def __str__(self):
        return self.categoria


class Produto(Base):
    tipo = models.ForeignKey('core.TipoProduto', verbose_name='Tipo', on_delete=models.CASCADE)
    categoria = models.ForeignKey('core.CategoriaProduto', verbose_name='Categoria', on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    informacao = models.TextField(max_length=2000)
    imagem1 = StdImageField('Imagem1', upload_to=get_file_path, variations={'thumb': {'width': 300, 'height': 400, 'crop': True}, 'test': {'width': 220, 'height': 250, 'crop': True}, 'single': {'width': 306, 'height': 400, 'crop': True}})
    imagem2 = StdImageField('Imagem2', null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 300, 'height': 400, 'crop': True}, 'test': {'width': 220, 'height': 250, 'crop': True}, 'single': {'width': 306, 'height': 400, 'crop': True}})
    imagem3 = StdImageField('Imagem3', null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 300, 'height': 400, 'crop': True}, 'test': {'width': 220, 'height': 250, 'crop': True}, 'single': {'width': 306, 'height': 400, 'crop': True}})
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    preco_desconto = models.DecimalField(max_digits=8, decimal_places=2)


    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


class Testimonial(Base):
    nome = models.CharField(max_length=50)
    testemunho = models.CharField(max_length=100)
    foto = StdImageField('Foto', upload_to=get_file_path, variations={'thumb': {'width': 80, 'height': 80, 'crop': True}})

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.nome


class Newsletter(Base):
    email_registro = models.EmailField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.email_registro


class Avaliacao(Base):
    ESTRELAS_CHOICES = (
        ('1', "rating1"),
        ('2', "rating2"),
        ('3', "rating3"),
        ('4', "rating4"),
        ('5', "rating5"),
    )
    usuario = models.ForeignKey('accounts.User', verbose_name='Usuário', on_delete=models.CASCADE)
    comentario = models.CharField(max_length=100, validators=[validate_is_profane])
    nota = models.CharField(max_length=1, choices=ESTRELAS_CHOICES)
    produto = models.ForeignKey('core.Produto', verbose_name='Produto', on_delete=models.CASCADE)
