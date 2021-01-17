from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import AboutView, logout_view, NewsLetterView, RegisterView, ProfileView, CodesView, FaqView, IconsView, IndexView, MailView, Products1View, Products2View, ProductsView, SingleView, LoginView
from .views import AvaliacaoDeleteView, SearchView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout/', logout_view, name='logout'),
    path('newsletter', NewsLetterView.as_view(), name='newsletter'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('about', AboutView.as_view(), name='about'),
    path('codes', CodesView.as_view(), name='codes'),
    path('faq', FaqView.as_view(), name='faq'),
    path('icons', IconsView.as_view(), name='icons'),
    path('mail', MailView.as_view(), name='mail'),
    path('products.html', ProductsView.as_view(), name='products'),
    path('products', ProductsView.as_view(), name='products'),
    path('products1', Products1View.as_view(), name='products1'),
    path('products2', Products2View.as_view(), name='products2'),
    path('search', SearchView.as_view(), name='search'),
    path('single/<int:pk>/', SingleView.as_view(), name='single'),
    path('<int:pk>/delete/', AvaliacaoDeleteView.as_view(), name='del_avaliacao'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

admin.AdminSite.site_header = "Renz System"
admin.AdminSite.site_title = "Renz"