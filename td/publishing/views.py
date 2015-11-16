from copy import deepcopy

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView)

from account.decorators import login_required
from account.mixins import LoginRequiredMixin

from td.models import Language
from td.publishing.forms import (
    RecentComForm, ConnectionForm, OfficialResourceForm, PublishRequestForm)
from td.publishing.models import (
    Contact, Chapter, OfficialResource, PublishRequest, OfficialResourceType)
from td.publishing.signals import published
from td.publishing.tasks import send_request_email, approve_publish_request


def resource_language_json(request, kind, lang):
    """
    Return the last published (approved) version of a resource by resource_type
    and language.
    """
    resource_type = get_object_or_404(OfficialResourceType, short_name=kind)
    language = get_object_or_404(Language, code=lang)

    published = PublishRequest.objects.filter(
        resource_type=resource_type,
        language=language
    ).order_by(
        "resource_type__short_name",
        "language__code",
        "-approved_at"
    ).first()

    data = {"chapters": []}
    # If no published chapter_set exists, revert to the previous dumping
    # of all chapters with the language code and resource type.
    if published and published.chapter_set.count():
        for chapter in published.chapter_set.order_by("number"):
            data["chapters"].append(chapter.data)
    else:
        chapters = Chapter.objects.filter(
            resource_type=resource_type,
            language=language
        ).order_by("number")
        for chapter in chapters:
            data["chapters"].append(chapter.data)
    return JsonResponse(data)


def resource_catalog_json(request, kind=None):
    # Catalog will be of official resources by language, eg:
    # [ { title: Open Bible Story, slug: obs, languages: [] } ]
    catalog = []
    # List all resources if a 'kind' isn't specified
    if kind is None:
        # @TODO - move this out of the view
        published_requests = PublishRequest.objects.filter(
            approved_at__isnull=False
        ).order_by(
            "resource_type__short_name",
            "language__code",
            "-approved_at",
        )

        # langs will contain a list of languages for the catalog item, while
        # listing all of the versions for the language + resource type
        resource = {"title": None, "slug": None, "langs": []}
        languages = {}
        for pub_req in published_requests:
            # If the resource type changes, copy the previous to the catalog,
            # set the new resource title, slug and reset langs
            if resource["title"] != pub_req.resource_type.long_name:
                if resource["title"] is not None:
                    resource["langs"] = [
                        lang for code, lang in languages.items()
                    ]
                    catalog.append(deepcopy(resource))
                resource["title"] = pub_req.resource_type.long_name
                resource["slug"] = pub_req.resource_type.short_name
                resource["langs"] = []
            else:
                # If this is the newest published version, set the date
                # mod(ified), append current data as first of the ver(sion)s
                if pub_req.language.code not in languages.keys():
                    languages[pub_req.language.code] = {
                        "lc": pub_req.language.code,
                        "mod": pub_req.created_at,
                        "vers": [pub_req.data, ],
                    }
                else:
                    # Append all other items to the vers list
                    languages[pub_req.language.code]["vers"].append(
                        pub_req.data
                    )
        if resource["title"] is not None:
            catalog.append(resource)
        return JsonResponse({"cat": catalog}, safe=False)

    # @TODO change the format for published requests by resource type
    resource_type = get_object_or_404(OfficialResourceType, short_name=kind)
    return JsonResponse(resource_type.data, safe=False)


@login_required
def api_contact(request):
    q = request.GET.get("term", "")
    data = [
        dict(
            id=o.pk,
            label=o.name,
            value=o.pk,
            url=reverse("contact_detail", args=[o.pk])
        )
        for o in Contact.objects.filter(name__icontains=q)[:10]
    ]
    return JsonResponse(data, safe=False)


class ContactList(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contacts.html"


class ContactDetail(LoginRequiredMixin, DetailView):
    template_name = "contact_detail.html"
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        context.update({
            "form_com": RecentComForm(user=self.request.user, contact=self.object),
            "recent_coms": self.object.recent_communications.all().order_by("-created"),
            "form_con": ConnectionForm(contact=self.object),
            "connections": self.object.source_connections.all().order_by("con_type")
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print self.object
        print request.user
        print request.POST
        context = self.get_context_data(object=self.object)
        if "recent_com" in request.POST:
            form_com = RecentComForm(
                request.POST,
                user=request.user,
                contact=self.object
            )
            if form_com.is_valid():
                form_com.save()
                messages.info(request, "Entry added.")
                return redirect("contact_detail", self.object.pk)
            else:
                context["form_com"] = form_com
        if "con" in request.POST:
            form_con = ConnectionForm(request.POST, contact=self.object)
            if form_con.is_valid():
                form_con.save()
                messages.info(request, "Connection created.")
                return redirect("contact_detail", self.object.pk)
            else:
                context["form_con"] = ConnectionForm(contact=self.object)
        return self.render_to_response(context)


class ContactMixin(LoginRequiredMixin):
    model = Contact
    fields = ["name", "email", "d43username", "location", "phone", "languages", "org", "other"]

    def get_success_url(self):
        return reverse("contact_detail", args=[self.object.pk])


class ContactUpdate(ContactMixin, UpdateView):
    template_name = "contact_update.html"


class ContactCreate(ContactMixin, CreateView):
    template_name = "contact_create.html"


class OfficialResourceCreateView(LoginRequiredMixin, CreateView):
    form_class = OfficialResourceForm
    model = OfficialResource
    template_name = "publishing/oresource_form.html"

    def get_success_url(self):
        return reverse("oresource_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        if form.cleaned_data["publish"]:
            self.object.publish_date = timezone.now().date()
        self.object.save()
        form.save_m2m()
        # @@@ Publish forms used to:
        # for contrib in get_contrib(self.lang):
        #     entry.contributors.add(contrib)
        if self.object.publish_date is not None:
            published.send(sender=self, official_resource=self.object)
        return redirect(self.get_success_url())


class OfficialResourceUpdateView(LoginRequiredMixin, UpdateView):
    form_class = OfficialResourceForm
    model = OfficialResource
    template_name = "publishing/oresource_form.html"

    def get_form(self, form_class):
        form = super(OfficialResourceUpdateView, self).get_form(form_class)
        del form.fields["language"]
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        published_flag = False
        if form.cleaned_data["publish"] and self.object.publish_date is None:
            self.object.publish_date = timezone.now().date()
            published_flag = True
        self.object.save()
        form.save_m2m()
        # @@@ Publish forms used to:
        # for contrib in get_contrib(self.lang):
        #     entry.contributors.add(contrib)
        if published_flag:
            published.send(sender=self, official_resource=self.object)
        return redirect("oresource_list")


class OfficialResourceListView(LoginRequiredMixin, ListView):
    model = OfficialResource
    template_name = "publishing/oresource_list.html"

    def get_context_data(self, **kwargs):
        context = super(OfficialResourceListView, self).get_context_data(**kwargs)
        context["publish_requests"] = PublishRequest.objects.filter(approved_at=None)
        return context

    def get_queryset(self, **kwargs):
        qs = super(OfficialResourceListView, self).get_queryset(**kwargs)
        qs = qs.order_by("resource_type__short_name", "language__name", "-created")
        qs = qs.distinct("language__name", "resource_type__short_name")
        return qs


class OfficialResourceDetailView(LoginRequiredMixin, DetailView):
    model = OfficialResource
    template_name = "publishing/oresource_detail.html"


class PublishRequestCreateView(CreateView):
    model = PublishRequest
    form_class = PublishRequestForm

    def form_valid(self, form):
        self.object = form.save()
        for each in form.cleaned_data["license_agreements"]:
            self.object.licenseagreement_set.create(document=each)
        # to do:
        # check validity of request
        messages.info(self.request, "Thank you for your request")
        send_request_email(self.object.pk)
        # TODO if the user is not logged in, redirect to the home page
        return redirect("oresource_list")


class PublishRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = PublishRequest
    form_class = PublishRequestForm

    def form_valid(self, form):
        # to do:
        # check validity of request...
        self.object = form.save()
        approve_publish_request(self.object.pk, self.request.user.pk)
        messages.info(self.request, "Publish Request Approved")
        return redirect("oresource_list")

    def get_object(self):
        request = get_object_or_404(
            self.model,
            id=self.kwargs.get('pk')
        )
        return request


class PublishRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = PublishRequest
    success_url = reverse_lazy("oresource_list")

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, "Publish Request Rejected/Deleted")
        # todo: when we figure out how to indicate the request is rejected... send an email
        # pr = self.get_object()
        # notify_requestor_rejected(pr.pk)
        return super(PublishRequestDeleteView, self).delete(request, *args, **kwargs)


def languages_autocomplete(request):
    term = request.GET.get("q").lower().encode("utf-8")
    langs = Language.objects.filter(Q(code__icontains=term) | Q(name__icontains=term))
    d = [
        {"pk": x.id, "ln": x.langname, "lc": x.langcode, "gl": x.gateway_flag}
        for x in langs
    ]
    return JsonResponse({"results": d, "count": len(d), "term": term})


def source_languages_autocomplete(request):
    term = request.GET.get("q")
    langs = PublishRequest.objects.filter(
        Q(language__code__icontains=term)
        | Q(language__name__icontains=term),
        checking_level=3
    ).order_by("language__code", "-approved_at").distinct("language__code")
    d = [
        {
            "pk": x.id,
            "ln": x.language.name,
            "lc": x.language.code,
            "gl": x.language.gateway_flag,
            "ver": x.version
        }
        for x in langs
    ]
    return JsonResponse({"results": d, "count": len(d), "term": term})


def ajax_language_version(request):
    search_lang = request.GET.get("q").lower().encode("utf-8")
    lang = get_object_or_404(Language, pk=search_lang)
    return JsonResponse({"current_version": lang.version})
