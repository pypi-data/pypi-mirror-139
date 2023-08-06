from django import forms
from django.forms import fields
from django.utils.translation import ugettext_lazy as _

from allauth.account.views import SignupForm
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from material import Fieldset, Layout, Row
from phonenumber_field.formfields import PhoneNumberField

from aleksis.core.mixins import ExtensibleForm
from aleksis.core.models import Group, Person

from .models import Event, EventRegistration, Terms, Voucher

COMMENT_CHOICES = [
    ("first", _("Only first name")),
    ("first_age", _("First name and age")),
    ("first_last_age", _("First name, last name and age")),
]

TEMPLATE_CHOICES = [
    ("list_sign", _("Signature list")),
    ("list_participants", _("Participants list")),
    ("corona", _("Corona attendance list")),
]

LICENCE_CHOICES = [
    ("CC-BY-4.0+", _("Creative Commons with attribution, 4.0 or later")),
    (
        "CC-BY-SA-4.0+",
        _(
            "Creative Commons with attribution and distribution only "
            "under the same conditions, 4.0 or later"
        ),
    ),
]


class EditEventForm(ExtensibleForm):
    """Form to create or edit an event."""

    layout = Layout(
        Fieldset(
            _("Base data"),
            "linked_group",
            Row("display_name", "description"),
            Row("place", "published"),
            Fieldset(_("Date data"), Row("date_event", "date_registration", "date_retraction")),
            Fieldset(_("Event details"), Row("cost", "max_participants"), "information"),
            Fieldset(_("Terms"), "terms"),
        ),
    )

    class Meta:
        model = Event
        fields = [
            "linked_group",
            "display_name",
            "description",
            "place",
            "published",
            "date_event",
            "date_registration",
            "date_retraction",
            "cost",
            "max_participants",
            "terms",
            "information",
        ]
        widgets = {
            "linked_group": ModelSelect2Widget(
                search_fields=["name__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
            "terms": ModelSelect2MultipleWidget(
                search_fields=["aspect__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
        }


class EditVoucherForm(forms.ModelForm):
    """Form to edit and create vouchers."""

    class Meta:
        model = Voucher
        exclude = ["code", "used_person_uid", "used", "deleted"]
        widgets = {
            "event": ModelSelect2Widget(
                search_fields=["display_name__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
            "person": ModelSelect2Widget(
                search_fields=["first_name__icontains", "last_name__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
        }
        help_texts = {
            "event": _("Event the voucher is valid for"),
            "person": _("Person the voucher is valid for"),
            "discount": _("Voucher discount"),
        }


class GenerateListForm(forms.Form):
    """Form to create a list of participants of a group."""

    group = forms.ModelChoiceField(
        label=_("Group"),
        queryset=Group.objects.all(),
        help_text=_("Select group to generate list"),
    )

    template = forms.ChoiceField(
        label=_("Template"),
        choices=TEMPLATE_CHOICES,
        help_text=_("Select template to generate list"),
    )

    landscape = forms.BooleanField(
        label=_("Landscape"),
        help_text=_("Select if output should be in landscape"),
        required=False,
    )


class RegisterEventGuardians(ExtensibleForm):
    class Meta:
        model = EventRegistration
        fields = []

    layout = Layout(
        Fieldset(
            _("Guardians personal data"),
            Row("guardian_first_name", "guardian_last_name"),
        ),
        Fieldset(
            _("Guardians contact details"),
            Row("guardian_email", "guardian_mobile_number"),
        ),
    )

    guardian_first_name = forms.CharField(
        label=_("Guardian's first name"),
        help_text=_(
            "Please enter the first name of the legal guardian who will fill in the registration "
            "with you and who can be reached during the event in an emergency."
        ),
    )

    guardian_last_name = forms.CharField(
        label=_("Guardian's last name"),
        help_text=_(
            "Please enter the last name of the legal guardian who will fill in the registration "
            "with you and who can be reached during the event in an emergency."
        ),
    )

    guardian_mobile_number = PhoneNumberField(
        label=_("Guardian's mobile number"),
        help_text=_(
            "We need the mobile phone number for emergencies if we "
            "urgently need to reach your parents during the event."
        ),
    )

    guardian_email = forms.EmailField(
        label=_("Guardian's email address"),
    )


class RegisterEventContactDetails(ExtensibleForm):
    class Meta:
        model = Group
        fields = []

    layout = Layout(
        Fieldset(
            _("Personal data"),
            Row("first_name", "last_name"),
            Row("date_of_birth", "sex"),
        ),
        Fieldset(
            _("Address data"),
            Row("street", "housenumber"),
            Row("postal_code", "place"),
        ),
        Fieldset(
            _("Contact details"),
            Row("mobile_number", "email"),
        ),
        Fieldset(
            _("School details"),
            Row("school", "school_place", "school_class"),
        ),
    )

    first_name = forms.CharField(
        label=_("First name"),
        disabled=True,
    )

    last_name = forms.CharField(
        label=_("Last name"),
        disabled=True,
    )

    street = forms.CharField(
        label=_("Street"),
    )

    housenumber = forms.CharField(
        label=_("Housenumber"),
    )

    postal_code = forms.CharField(
        label=_("Postal code"),
    )

    place = forms.CharField(
        label=_("Place"),
    )

    mobile_number = PhoneNumberField(
        label=_("Mobile number"),
        required=False,
        help_text=_(
            "Your mobile number helps us to reach you in an emergency during the event, e.g. "
            "if you are alone with your group at a conference or similar. If you don't have a "
            "cell phone, you can leave the field blank."
        ),
    )

    date_of_birth = forms.DateField(
        label=_("Date of birth"),
    )

    sex = forms.ChoiceField(
        label=_("Sex"),
        help_text=_(
            "For various reasons, e.g. because we have to keep gender segregation during the night "
            "for legal reasons, we need to know if you are a boy or a girl."
        ),
        choices=Person.SEX_CHOICES,
        initial=None,
    )

    email = forms.EmailField(
        label=_("Email address"),
        help_text=_(
            "Please use your personal e-mail address here, which you will check "
            "personally. Important information will always be sent to your parents "
            "as well. Do not use an e-mail address owned by your parents here."
        ),
    )

    school = forms.CharField(
        label=_("School"),
        help_text=_("Please enter the name of your school."),
    )

    school_place = forms.CharField(
        label=_("School place"),
        help_text=_("Enter the place (city) where your school is located."),
    )

    school_class = forms.CharField(
        label=_("School class"),
        help_text=_("Please enter the class you are in (e.g. 8a)."),
    )


class RegisterEventAdditional(ExtensibleForm):

    layout = Layout(
        Fieldset(
            _("Medical information / intolerances"),
            Row("medical_information"),
        ),
        Fieldset(
            _("Other remarks"),
            Row("comment"),
        ),
    )

    class Meta:
        model = EventRegistration
        fields = ["medical_information", "comment"]
        help_texts = {
            "medical_information": _(
                "If there are any medically important things we need to "
                "consider, e.g. when making food or to make sure you take "
                "prescribed medication, please enter it here."
            ),
            "comment": _("You can write down any remarks you want to tell us here."),
        }

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in event.linked_group.additional_fields.all():
            field_instance = getattr(fields, field.field_type)(
                required=field.required,
                help_text=field.help_text,
            )
            self.fields[field.title] = field_instance
            node = Fieldset(f"{field.title}", f"{field.title}")
            self.add_node_to_layout(node)


class RegisterEventFinancial(ExtensibleForm):
    """Form to register for an event."""

    layout = Layout(
        Fieldset(
            _("Financial data"),
            "voucher_code",
            Row("accept_sepa", "iban"),
            "donation",
        ),
    )

    voucher_code = forms.CharField(
        label=_("Voucher code"),
        help_text=_("If you have a voucher code, type it in here."),
        required=False,
    )

    def clean(self):
        if self.cleaned_data["accept_sepa"]:
            if not self.cleaned_data["iban"]:
                raise forms.ValidationError(_("Please enter your IBAN"))

    class Meta:
        model = EventRegistration
        fields = ["voucher_code", "iban", "donation", "accept_sepa"]
        help_texts = {
            "donation": _(
                "Our association would like to offer all children and young "
                "people the opportunity to participate in our events. Sometimes, "
                "however, families cannot afford the full fee. We therefore have a "
                "budget from which we can promote participation after we have "
                "carefully examined the necessity and eligibility. We rely on "
                "donations for this budget. If you would like to donate a voluntary "
                "additional amount for this budget, please indicate this here."
            ),
            "accept_sepa": _(
                "Parents: I authorize the creditor Teckids e.V., Kennedyallee 18, 53175 Bonn with "
                "creditor ID DE70ZZZ00001497650, to collect the participant fee from my account "
                "once using the SEPA core direct debit. At the same time, I instruct my bank to "
                "redeem the SEPA core direct debit withdrawn from my account by Teckids e.V."
            ),
            "iban": _(
                "If your parents want to pay by SEPA direct debit, "
                "please let them fill out this field."
            ),
        }


class RegisterEventConsent(ExtensibleForm):
    class Meta:
        model = EventRegistration
        fields = []

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in event.terms.all():
            field_instance = forms.BooleanField(
                required=True,
                label=field.confirmation_text,
            )
            self.fields[f"consent_{field.pk}"] = field_instance
            node = Row(f"consent_{field.pk}")
            self.add_node_to_layout(node)


class EditEventRegistrationForm(forms.ModelForm):

    layout = Layout(
        Fieldset(
            _("General event information"),
            Row("event", "person"),
            Row("comment"),
        ),
        Fieldset(
            _("Financial data"),
            "voucher_code",
            Row("iban", "donation", "accept_sepa"),
        ),
        Fieldset(
            _("Declaration of consent"),
            Row("accept_terms", "accept_data", "accept_general_terms"),
        ),
    )

    class Meta:
        model = EventRegistration
        help_texts = {
            "voucher": _(
                "If you have a voucher for the event, enter the code here."
                "It will be charged automatically."
            ),
            "donation": (
                "Our association would like to offer all children and young "
                "people the opportunity to participate in our events. Often, "
                "however, the family fee cannot be paid. We therefore have a "
                "budget from which we can promote participation after we have "
                "carefully examined the necessity and eligibility. We rely on "
                "donations for this budget. If you would like to donate a voluntary "
                "additional amount for this budget, please indicate this here. We do not "
                "permanently save whether and if so in what amount donations are made "
                "and also not within the association, e.g. passed on to leisure supervisors. "
            ),
            "accept_sepa": _(
                "Parents: I authorize the creditor  e.V., Rochusstr. 2-4, 53123 Bonn with "
                "creditor ID DE70FZT00001497650, to collect the participant fee from my account "
                "once using the SEPA core direct debit. At the same time, I instruct my bank "
                "to redeem the SEPA core direct debit withdrawn from my account by  e.V."
            ),
            "iban": _(
                "If your parents want to pay by SEPA direct debit, "
                "please let them fill out this field."
            ),
            "accept_terms": _(
                "Parents: My child filled out the registration form together with me, but myself, "
                "and I agree to the participation, the terms of use and the terms and conditions. "
                "I am aware that the registration is binding and that withdrawal is only possible "
                "in exceptional cases with a valid reason. In addition, I agree to pay the "
                "participation fee in advance and agree to the reimbursement "
                "guidelines mentioned above."
            ),
            "accept_data": _(
                "I consent to the processing of my data as stated in the "
                "terms of use and all the data provided is correct. If I am under "
                "the age of 16, my parents also agree to this and I can prove this on "
                "request (e.g. by making contact with my parents)."
            ),
            "accept_general_terms": _("I agree with the" "AGB and have read them."),
        }
        exclude = []


class EditTermForm(forms.ModelForm):
    class Meta:
        model = Terms
        exclude = []


class RegisterEventAccount(SignupForm, ExtensibleForm):
    """Form to register new user accounts."""

    class Meta:
        model = EventRegistration
        fields = []

    layout = Layout(
        Fieldset(
            _("Base data"),
            Row("first_name", "last_name", "date_of_birth"),
        ),
        Fieldset(
            _("Account data"),
            "username",
            Row("email", "email2"),
            Row("password1", "password2"),
        ),
    )

    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    date_of_birth = forms.DateField(label=_("Date of birth"))
