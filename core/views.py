from django.views.generic import TemplateView, FormView, DeleteView, ListView
from .forms import ContatoForm, NewsletterForm, AvaliacaoForm
from django.urls import reverse_lazy
from django.contrib import messages
from core.models import Funcionario, Produto, Testimonial, Avaliacao
from accounts.models import Profile
from datetime import date, timedelta
from accounts.forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
import math


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['funcionarios'] = Funcionario.objects.order_by('?').all()
        return context


class ProfileView(LoginRequiredMixin, FormView):
    login_url = 'index'
    redirect_field_name = 'redirect_to'
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=ProfileForm):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return form_class(instance=profile, **self.get_form_kwargs())
        except Profile.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user_id=self.request.user.id)[0]
        return context

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Perfil atualizado!')
        return super(ProfileView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Não possível atualizar o perfil!')
        return super(ProfileView, self).form_invalid(form, *args, **kwargs)


class CodesView(TemplateView):
    template_name = 'codes.html'


class FaqView(TemplateView):
    template_name = 'faq.html'


class IconsView(TemplateView):
    template_name = 'icons.html'


class NewsLetterView(FormView):
    template_name = 'index.html'
    form_class = NewsletterForm

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        form.save()
        messages.success(self.request, 'Cadastrado ao Newsletter!')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Não foi possível cadastrar ao Newsletter')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'index.html'

    def form_valid(self, form, *args, **kwargs):
        request = self.request
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)

            if user.profile.nome:
                messages.success(self.request, f'Seja bem-vindo(a) {user.profile.nome}!')
            else:
                messages.success(self.request, f'Seja bem-vindo(a) {user.get_full_name()}!')

            return super(LoginView, self).form_valid(form, *args, **kwargs)
        else:
            messages.error(self.request, 'E-mail ou senha está incorreto!')
            return super(LoginView, self).form_invalid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'E-mail ou senha está incorreto!')
        return super(LoginView, self).form_invalid(form, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('index')


class RegisterView(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('index')
    template_name = 'index.html'

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Registro feito com sucesso!')
        form.save()
        return super(RegisterView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao registrar.')
        return super(RegisterView, self).form_invalid(form, *args, **kwargs)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        context['smartphones'] = Produto.objects.filter(tipo='1').order_by('?').all()
        context['audio'] = Produto.objects.filter(tipo='2').order_by('?').all()
        context['informatica'] = Produto.objects.filter(tipo='3').order_by('?').all()
        context['eletrodomestico'] = Produto.objects.filter(tipo='5').order_by('?').all()
        context['cozinha'] = Produto.objects.filter(tipo='4').order_by('?').all()
        context['testimonials'] = Testimonial.objects.order_by('?').all()
        context['novos_produtos'] = Produto.objects.order_by('-id').all()
        return context


class MailView(FormView):
    template_name = 'mail.html'
    form_class = ContatoForm
    success_url = reverse_lazy('mail')

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(MailView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        return super(MailView, self).form_invalid(form, *args, **kwargs)


class ProductsView(ListView):
    template_name = 'products.html'
    model =  Produto
    paginate_by = 9

    def get_queryset(self):
        self.queryset = Produto.objects.filter(tipo__tipo__in=['smartphones', 'audio']).order_by('?')

        order = self.request.GET.get('order', '?')
        preco = self.request.GET.get('preco', '?')
        if order == 'smartphone':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'mp3':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'tablets':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')

        if order == 'loja_de_verao':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(tipo__tipo__in=['smartphones','audio']).order_by('-id')

        if order == 'marcas_em_destaque':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(tipo__tipo__in=['smartphones','audio']).order_by('-id')

        if order == 'ofertas_do_dia':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(tipo__tipo__in=['smartphones','audio']).order_by('-id')

        # filtragem por preco
        if preco == '100':
            self.queryset = Produto.objects.filter(preco_desconto__range=(0, preco)).filter(categoria__categoria=order).order_by('preco_desconto')
        if preco == '500':
            self.queryset = Produto.objects.filter(preco_desconto__range=(101, preco)).filter(categoria__categoria=order).order_by('preco_desconto')
        if preco == '10000':
            self.queryset = Produto.objects.filter(preco_desconto__range=(501, preco)).filter(categoria__categoria=order).order_by('preco_desconto')
        if preco == '20000':
            self.queryset = Produto.objects.filter(preco_desconto__range=(10001, preco)).filter(categoria__categoria=order).order_by('preco_desconto')
        if preco == '20001':
            self.queryset = Produto.objects.filter(preco_desconto__range=(preco, 50000)).filter(categoria__categoria=order).order_by('preco_desconto')

        return self.queryset

    def get_context_data(self, **kwargs):
        order = self.request.GET.get('order', '?')
        preco = self.request.GET.get('preco', '?')
        context = super(ProductsView, self).get_context_data(**kwargs)
        context['prc'] = preco
        context['ord'] = order
        context['data'] = date.today() - timedelta(days=3)
        return context


class Products1View(ListView):
    template_name = 'products1.html'
    model = Produto
    paginate_by = 9

    def get_queryset(self):
        self.queryset = Produto.objects.filter(tipo__tipo__in=['informatica']).order_by('?')
        order = self.request.GET.get('order', '?')
        preco = self.request.GET.get('preco', '?')

        if order == 'desktops':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'notebooks':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'smartwatches':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')

        if order == 'loja_de_verao':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(
                tipo__tipo__in=['informatica']).order_by('-id')

        if order == 'marcas_em_destaque':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(
                tipo__tipo__in=['informatica']).order_by('-id')

        if order == 'ofertas_do_dia':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(
                tipo__tipo__in=['informatica']).order_by('-id')

        if order == 'novos_smartwatches':
            self.queryset = Produto.objects.filter(categoria__categoria='smartwatches').order_by('-id')

            # filtragem por preco
        if preco == '100':
            self.queryset = Produto.objects.filter(preco_desconto__range=(0, preco)).filter(
                categoria__categoria=order).order_by('preco_desconto')
        if preco == '500':
            self.queryset = Produto.objects.filter(preco_desconto__range=(101, preco)).filter(
                categoria__categoria=order).order_by('preco_desconto')
        if preco == '10000':
            self.queryset = Produto.objects.filter(preco_desconto__range=(501, preco)).filter(
                categoria__categoria=order).order_by('preco_desconto')
        if preco == '20000':
            self.queryset = Produto.objects.filter(preco_desconto__range=(10001, preco)).filter(
                categoria__categoria=order).order_by('preco_desconto')
        if preco == '20001':
            self.queryset = Produto.objects.filter(preco_desconto__range=(preco, 50000)).filter(
                categoria__categoria=order).order_by('preco_desconto')

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(Products1View, self).get_context_data(**kwargs)
        context['data'] = date.today() - timedelta(days=3)
        preco = self.request.GET.get('preco', '?')
        order = self.request.GET.get('order', '?')
        context['prc'] = preco
        context['ord'] = order
        return context


class Products2View(ListView):
    template_name = 'products2.html'
    model = Produto
    paginate_by = 9

    def get_queryset(self):
        # filtragem por tipo de produto
        self.queryset = Produto.objects.filter(tipo__tipo__in=['eletrodomesticos, cozinha']).order_by('?')
        order = self.request.GET.get('order', '?')
        preco = self.request.GET.get('preco', '?')

        if order == 'cafeteiras':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'tv':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'refrigeradores':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'eletrodomesticos':
            self.queryset = Produto.objects.filter(tipo__tipo=order).order_by('-id')

        if order == 'loja_de_verao':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(
                tipo__tipo__in=['cozinha', 'eletrodomesticos']).order_by('-id')

        if order == 'marcas_em_destaque':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(
                tipo__tipo__in=['cozinha', 'eletrodomesticos']).order_by('-id')

        if order == 'ofertas_do_dia':
            self.queryset = Produto.objects.filter(categoria__categoria=order).filter(
                tipo__tipo__in=['cozinha', 'eletrodomesticos']).order_by('-id')

        if order == 'trituradores':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'aquecedores':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'brinquedos_infantis':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'filtros':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')
        if order == 'ac':
            self.queryset = Produto.objects.filter(categoria__categoria=order).order_by('-id')

        # filtragem por preco
        if order == 'eletrodomesticos':
            if preco == '100':
                self.queryset = Produto.objects.filter(preco_desconto__range=(0, preco)).filter(
                    tipo__tipo=order).order_by('preco_desconto')
            if preco == '500':
                self.queryset = Produto.objects.filter(preco_desconto__range=(101, preco)).filter(
                    tipo__tipo=order).order_by('preco_desconto')
            if preco == '10000':
                self.queryset = Produto.objects.filter(preco_desconto__range=(501, preco)).filter(
                    tipo__tipo=order).order_by('preco_desconto')
            if preco == '20000':
                self.queryset = Produto.objects.filter(preco_desconto__range=(10001, preco)).filter(
                    tipo__tipo=order).order_by('preco_desconto')
            if preco == '20001':
                self.queryset = Produto.objects.filter(preco_desconto__range=(preco, 50000)).filter(
                    tipo__tipo=order).order_by('preco_desconto')
        else:
            if preco == '100':
                self.queryset = Produto.objects.filter(preco_desconto__range=(0, preco)).filter(
                    categoria__categoria=order).order_by('preco_desconto')
            if preco == '500':
                self.queryset = Produto.objects.filter(preco_desconto__range=(101, preco)).filter(
                    categoria__categoria=order).order_by('preco_desconto')
            if preco == '10000':
                self.queryset = Produto.objects.filter(preco_desconto__range=(501, preco)).filter(
                    categoria__categoria=order).order_by('preco_desconto')
            if preco == '20000':
                self.queryset = Produto.objects.filter(preco_desconto__range=(10001, preco)).filter(
                    categoria__categoria=order).order_by('preco_desconto')
            if preco == '20001':
                self.queryset = Produto.objects.filter(preco_desconto__range=(preco, 50000)).filter(
                    categoria__categoria=order).order_by('preco_desconto')

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(Products2View, self).get_context_data(**kwargs)
        context['data'] = date.today() - timedelta(days=3)
        order = self.request.GET.get('order', '?')
        preco = self.request.GET.get('preco', '?')
        context['prc'] = preco
        context['ord'] = order

        return context


class SingleView(FormView):
    template_name = 'single.html'
    form_class = AvaliacaoForm

    def get_context_data(self, **kwargs):
        context = super(SingleView, self).get_context_data(**kwargs)
        obj_nome = Avaliacao.objects.filter(produto=Produto.objects.get(id=self.kwargs['pk']))
        z = 0
        for i in obj_nome:
            z = z + int(i.nota)
        try:
            media = math.ceil(z/len(obj_nome))
        except:
            media = 5

        context['produtos'] = Produto.objects.all().order_by('?')
        context['produto'] = Produto.objects.get(id=self.kwargs['pk'])
        context['avaliacoes'] = Avaliacao.objects.filter(produto=self.kwargs['pk'])
        context['media'] = media
        return context

    def form_valid(self, form, *args, **kwargs):
        form.instance.usuario = self.request.user
        form.instance.produto = Produto.objects.get(id=self.kwargs['pk'])
        form.save()
        messages.success(self.request, 'Avaliação feita com sucesso!')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao avaliar!')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class AvaliacaoDeleteView(DeleteView):
    template_name = 'single.html'
    success_url = reverse_lazy('single')

    def get_object(self):
        id_ = self.kwargs['pk']
        return get_object_or_404(Avaliacao, id=id_)

    def get_success_url(self):
        proximo = self.request.POST.get('next', '/')
        messages.success(self.request, 'Avaliação deletada com sucesso!')
        return proximo


class SearchView(ListView):
    template_name = 'search.html'
    model = Produto
    paginate_by = 9

    def get_queryset(self):
        nome = self.request.GET.get('nome')
        self.queryset = Produto.objects.all()
        if nome:
            self.queryset = Produto.objects.filter(nome__icontains=nome)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nome = self.request.GET.get('nome')
        context['nome'] = nome
        context['produtos_relacionados'] = Produto.objects.all().order_by('?')
        return context

