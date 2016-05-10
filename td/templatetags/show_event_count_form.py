from django.core.urlresolvers import reverse
from django.template.defaulttags import register

from td.models import WARegion, Country, Language


@register.inclusion_tag("tracking/_event_count_form.html", takes_context=True)
def show_event_count_form(context, **kwargs):
    mode = kwargs.get("mode") or\
           "language" if "language" in context else\
           "country" if "country" in context else\
           "region" if "wa_region" in context else\
           "dashboard"
    #
    if mode == "region":
        selected_option = kwargs.get("selected_option", context.get("wa_region").slug)
        options = [(r.slug, r.name) for r in WARegion.objects.filter(slug__iexact=selected_option)]
    elif mode == "country":
        selected_option = kwargs.get("selected_option", context.get("country"))
        options = [(c.code, c.name) for c in Country.objects.filter(code__iexact=selected_option)]
    elif mode == "language":
        selected_option = kwargs.get("selected_option", context.get("language"))
        options = [(l.code, l.name) for l in Language.objects.filter(code__iexact=selected_option)]
    else:
        selected_option = kwargs.get("selected_option", "")
        options = [(r.slug, r.name) for r in WARegion.objects.all()]
    #
    selected_fy = kwargs.get("selected_fy", "0")
    fiscal_years = [("0", "this"), ("1", "next"), ("-1", "last")]
    #
    container = kwargs.get("container", "")
    # If "container" is not specified, then the assumption is that this form is displayed on a page that has no
    # table for the event count and implies that this form will have have to be submitted to another page that does. The
    # default page to display the event count table is the Event Count page.
    form_action = kwargs.get("form_action", reverse("tracking:event_count")) if not container else ""
    #
    return {"mode": mode, "selected_option": selected_option, "selected_fy": selected_fy, "form_action": form_action,
            "options": options, "fiscal_years": fiscal_years, "container": container}
