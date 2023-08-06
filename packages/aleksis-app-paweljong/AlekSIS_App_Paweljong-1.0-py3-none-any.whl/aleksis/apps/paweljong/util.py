import os
from tempfile import mkstemp
from textwrap import wrap

from django import forms
from django.conf import settings

import requests


def subscribe_mailinglist(listname, mail):
    form_data = {
        "email": mail,
        "list": listname,
        "action": "subrequest",
        "via_subrequest": 1,
    }
    return requests.post(get_site_preferences()["paweljong__wws_post_url"], data=form_data)


def form_to_text_table(form, width=74, sep=" | "):
    output_list = []

    for field_name, field in form.fields.items():
        # Determine field value depending on field type
        if isinstance(field, forms.ModelMultipleChoiceField):
            value = "\n".join([choice.__str__() for choice in form.cleaned_data[field_name]])
        elif isinstance(field, forms.ModelChoiceField):
            value = dict(field.choices)[form.cleaned_data[field_name]]
        else:
            value = form.cleaned_data[field_name]
        value = str(value)

        # Store in output list
        output_list.append((field.label, value))

    # Determine maximum field widths
    max_label = max([len(_[0]) for _ in output_list])
    max_value = width - len(sep) - max_label

    # Generate result text
    res = []
    for label, value in output_list:
        # Wrap value to lines
        lines = wrap(value, max_value)

        if lines:
            # Output first line with label name
            res.append("%s%s%s" % (label.rjust(max_label), sep, lines.pop(0)))

            # Output following lines without label, if any
            for line in lines:
                res.append("%s%s%s" % (" " * max_label, sep, line))
        else:
            # Output empty label row
            res.append("%s%s" % (label.rjust(max_label), sep))

    # Build text block and return
    return "\n".join(res)


def upload_file_to_media_url(file, subdir="", prefix="upload_"):
    fileext = os.path.splitext(file.name)[-1]

    dest_abs = os.path.join(settings.MEDIA_ROOT, subdir)
    dest_fd, dest_path = mkstemp(prefix=prefix, suffix=fileext, dir=dest_abs)

    os.close(dest_fd)
    with open(dest_path, "wb+") as dest_file:
        for chunk in file.chunks():
            dest_file.write(chunk)

    basename = os.path.basename(dest_path)
    url = "%s/%s/%s" % (settings.MEDIA_URL, subdir, basename)

    return url
