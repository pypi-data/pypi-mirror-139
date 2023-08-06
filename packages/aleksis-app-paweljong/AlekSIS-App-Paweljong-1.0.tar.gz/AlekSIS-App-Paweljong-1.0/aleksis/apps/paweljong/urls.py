from django.urls import path

from aleksis.apps.postbuero.forms import MailAddForm

from . import views
from .forms import (
    RegisterEventAccount,
    RegisterEventAdditional,
    RegisterEventConsent,
    RegisterEventContactDetails,
    RegisterEventFinancial,
    RegisterEventGuardians,
)

register_forms = [
    ("email", MailAddForm),
    ("register", RegisterEventAccount),
    ("contact_details", RegisterEventContactDetails),
    ("guardians", RegisterEventGuardians),
    ("additional", RegisterEventAdditional),
    ("financial", RegisterEventFinancial),
    ("consent", RegisterEventConsent),
]
condition_dict = {
    "email": views.is_email_needed,
    "register": views.is_person_anonymous,
}

urlpatterns = [
    path("event/<slug:slug>/edit", views.EditEventView.as_view(), name="edit_event_by_slug"),
    path(
        "event/<slug:slug>/register",
        views.RegisterEventWizardView.as_view(register_forms, condition_dict=condition_dict),
        name="register_event_by_slug",
    ),
    path("event/<slug:slug>", views.EventFullView.as_view(), name="event_by_name"),
    path(
        "event/<slug:slug>/start",
        views.RegisterEventStart.as_view(),
        name="register_event_by_slug_start",
    ),
    path("misc/set_email_needed/<slug:slug>", views.set_email_needed, name="set_email_needed"),
    path("events/create", views.CreateEventView.as_view(), name="create_event"),
    path("events/manage", views.manage_events, name="manage_events"),
    path("vouchers/create", views.VoucherCreateView.as_view(), name="create_vouchers"),
    path(
        "vouchers/<int:pk>/delete", views.VoucherDeleteView.as_view(), name="delete_voucher_by_pk"
    ),
    path("vouchers/<int:pk>/edit", views.VoucherEditView.as_view(), name="edit_voucher_by_pk"),
    path("vouchers/<int:pk>/print", views.print_voucher, name="print_voucher_by_pk"),
    path("vouchers/", views.vouchers, name="vouchers"),
    path("event/lists/generate", views.generate_lists, name="generate_lists"),
    path("event/registrations/list", views.registrations, name="registrations"),
    path(
        "event/registrations/<int:pk>",
        views.EventRegistrationDetailView.as_view(),
        name="registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>/edit",
        views.EventRegistrationEditView.as_view(),
        name="edit_registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>/delete",
        views.EventRegistrationDeleteView.as_view(),
        name="delete_registration_by_pk",
    ),
    path(
        "event/terms/list",
        views.TermListView.as_view(),
        name="terms",
    ),
    path(
        "event/terms/create",
        views.TermCreateView.as_view(),
        name="create_term",
    ),
    path(
        "event/terms/<int:pk>/edit",
        views.TermEditView.as_view(),
        name="edit_term_by_pk",
    ),
]
