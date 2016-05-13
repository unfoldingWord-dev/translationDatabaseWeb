from django.core.urlresolvers import reverse
from django.template.defaulttags import register

from td.models import WARegion


@register.inclusion_tag("tracking/_event_count_form.html", takes_context=True)
def show_event_count_form(context, **kwargs):
    # Look for wa_region in the context first, which means that the tag is called from page that is already working with
    # a single wa_region (e.g. WA Region detail page).If that's not found, then look for "selected_region" kwarg with ""
    # as the fallback.
    selected_region = context.get("wa_region").slug if "wa_region" in context else kwargs.get("selected_region", "")
    # If called from a page that's working with a specific wa_region, only put that region in the list. If not, put all
    # regions objects in the list.
    regions = WARegion.objects.filter(slug=selected_region) if "wa_region" in context else WARegion.objects.all()
    #
    selected_fy = kwargs.get("selected_fy", "0")
    financial_years = [("0", "this"), ("1", "next"), ("-1", "last")]
    #
    container = kwargs.get("container", "")
    # If "container" is not specified, then the assumption is that this form is displayed on a page that has no
    # table for the event count and implies that this form will have have to be submitted to another page that does. The
    # default page to display the event count table is the Event Count page.
    form_action = kwargs.get("form_action", reverse("tracking:event_count")) if not container else ""
    #
    return {"selected_region": selected_region, "selected_fy": selected_fy, "form_action": form_action,
            "regions": regions, "financial_years": financial_years, "container": container}
