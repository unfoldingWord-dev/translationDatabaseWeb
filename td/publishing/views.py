from django.core.urlresolvers import reverse, reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from django.contrib import messages

from account.decorators import login_required
from account.mixins import LoginRequiredMixin

from td.models import Language

from .forms import RecentComForm, ConnectionForm, OfficialResourceForm, PublishRequestForm
from .models import Contact, OfficialResource, PublishRequest, OfficialResourceType
from .signals import published
from .tasks import send_request_email, approve_publish_request


def resource_language_json(request, kind, lang):
    resource_type = get_object_or_404(OfficialResourceType, short_name=kind)
    language = get_object_or_404(Language, code=lang)
    chapters = resource_type.chapter_set.filter(language=language).order_by("number")
    data = {
        "chapters": [chapter.data for chapter in chapters]
    }
    return JsonResponse(data)


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

    @property
    def lang(self):
        if not hasattr(self, "_lang"):
            if self.kwargs.get("code"):
                self._lang = get_object_or_404(Language, code=self.kwargs.get("code"))
            else:
                self._lang = None
        return self._lang

    def get_context_data(self, **kwargs):
        context = super(OfficialResourceUpdateView, self).get_context_data(**kwargs)
        context.update(dict(lang=self.lang))
        return context

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

    def get_object(self):
        return get_object_or_404(OfficialResource, language=self.lang)


class OfficialResourceListView(LoginRequiredMixin, ListView):
    model = OfficialResource
    template_name = "publishing/oresource_list.html"

    def get_context_data(self, **kwargs):
        context = super(OfficialResourceListView, self).get_context_data(**kwargs)
        context["publish_requests"] = PublishRequest.objects.filter(approved_at=None)
        return context

    def get_queryset(self, **kwargs):
        qs = super(OfficialResourceListView, self).get_queryset(**kwargs)
        qs = qs.order_by("language__name", "-created")
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
        return redirect("publish_request")


class PublishRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = PublishRequest
    form_class = PublishRequestForm

    def form_valid(self, form):
        # to do:
        # check validity of request...
        self.object = form.save()
        messages.info(self.request, "Publish Request Approved")
        approve_publish_request(self.object.pk, self.request.user.id)
        return redirect("oresource_update", code=self.object.language.code)


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
    langs = Language.objects.filter(Q(langcode__icontains=term) | Q(langname__icontains=term))
    d = [
        {"pk": x.id, "ln": x.langname, "lc": x.langcode, "gl": x.gateway_flag}
        for x in langs
    ]
    return JsonResponse({"results": d, "count": len(d), "term": term})


def source_languages_autocomplete(request):
    term = request.GET.get("q").lower().encode("utf-8")
    langs = Language.objects.filter(checking_level=3).filter(Q(langcode__icontains=term) | Q(langname__icontains=term))
    d = [
        {"pk": x.id, "ln": x.langname, "lc": x.langcode, "gl": x.gateway_flag, "ver": x.version}
        for x in langs
    ]
    return JsonResponse({"results": d, "count": len(d), "term": term})


def ajax_language_version(request):
    search_lang = request.GET.get("q").lower().encode("utf-8")
    lang = get_object_or_404(Language, pk=search_lang)
    return JsonResponse({"current_version": lang.version})
