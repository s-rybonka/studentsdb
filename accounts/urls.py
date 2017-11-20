from django.conf.urls import url
from allauth.account import views
from accounts import views as account_views

urlpatterns = [
    url(r"^signup/$", account_views.SignUpView.as_view(), name="account_signup"),
    url(r"^login/$", account_views.SignInView.as_view(), name="account_login"),
    url(r"^logout/$", account_views.SignOutView.as_view(), name="account_logout"),
    url(r"^password/change/$", views.password_change, name="account_change_password"),
    url(r"^password/set/$", views.password_set, name="account_set_password"),
    url(r"^inactive/$", views.account_inactive, name="account_inactive"),

    # E-mails URLs
    url(r"^email/$", views.email, name="account_email"),
    url(r"^confirm-email/$", views.email_verification_sent,
        name="account_email_verification_sent"),
    url(r"^confirm-email/(?P<key>[-:\w]+)/$", views.confirm_email,
        name="account_confirm_email"),

    # Reset Password
    url(r"^password/reset/$", views.password_reset, name="account_reset_password"),
    url(r"^password/reset/done/$", views.password_reset_done,
        name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key, name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$", views.password_reset_from_key_done,
        name="account_reset_password_from_key_done"),

    # Accounts
    url(r"^account-list/$", account_views.AccountListView.as_view(),
        name="account_list"),
    url(r"^account/(?P<pk>\d+)/detail/$", account_views.AccountDetailView.as_view(),
        name="account_detail"),
]
