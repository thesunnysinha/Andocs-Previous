from django.urls import path
from AndocsApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('',views.ProductView.as_view(),name = "home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('cart/',views.cart,name='cart'),
    path('update_item/',views.updateItem,name='update_item'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),
    path('add_address/',views.add_address,name ='addaddress'),
    path('delete_address/',views.deleteAddress,name='delete_address'),

    path("about_us/",views.aboutus,name ='aboutus'),
#    path('removeaddress/',views.remove_address,name='removeaddress'),

    path('orders/', views.orders, name='orders'),

    path('team/',views.team,name='team'),
    path('services/',views.services,name='services'),


    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name = 'passwordchangedone'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),


    path('password-rest/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name="password_reset"),
    path('password-rest/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name="password_reset_done"),
    path('password-rest-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name="password_reset_confirm"),
    path('password-rest-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name="password_reset_complete"),


    path('cosmetics/', views.cosmetics, name='cosmetics'),
    path('cosmetics/<slug:data>', views.cosmetics, name='cosmeticsdata'),

    path('petproducts/', views.petproducts, name='petproducts'),
    path('petproducts/<slug:data>', views.petproducts, name='petproductsdata'),

    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),

    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('user/resendOTP/',views.resend_otp),

    path('search/',views.search,name = 'search'),
    path('contactus/',views.contacts,name = 'contactus'),
    path('helpdesk/',views.helpdesk,name = 'helpdesk'),
    path('edit_profile/',views.editprofile,name = 'edit_profile'),

    path('wishlist/',views.wishlist,name = 'wishlist'),
    path('update_wishlist/',views.updateWishlist,name='update_wishlist'),

    path('product-detail/addcomment/<int:id>',views.addcomment,name = 'addcomment'),


] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
