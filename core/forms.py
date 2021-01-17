from django import forms
from django.core.mail.message import EmailMessage
from phonenumber_field.formfields import PhoneNumberField
from core.models import Newsletter, Avaliacao


class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    phone = PhoneNumberField()
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        mensagem = self.cleaned_data['mensagem']

        n = 'Nome'
        e = 'E-mail'
        a = 'Phone'
        m = 'Mensagem'

        conteudo = f'{n}: {nome}\n{e}: {email}\n{a}: {phone}\n{m}: {mensagem}'

        mail = EmailMessage(
            subject=f'Contato {email}',
            body=conteudo,
            from_email='renzstore2@gmail.com',
            to=['renzo.prats321@gmail.com'],
            headers={'Reply-To': email}
        )
        mail.send()


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('email_registro',)

    def send_mail(self):
        email = self.cleaned_data['email_registro']

        conteudo = f'Olá! Seu e-mail foi cadastrado em nosso site Renz Store, seja muito bem-vindo(a)!'

        mail = EmailMessage(
            subject=f'Bem-vindo(a) ao Renz Store!',
            body=conteudo,
            from_email='renzstore2@gmail.com',
            to=[email],
            headers={'Reply-To': email}
        )
        mail.send()


class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao
        fields = ('nota', 'comentario')










