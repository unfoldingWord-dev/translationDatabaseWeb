from django.http import JsonResponse

from td.models import TempLanguage
from td.resources.models import Questionnaire


def questionnaire_json(request):
    return JsonResponse(Questionnaire.objects.latest('created_at').questions, safe=False)


def templanguages_json(request):
    return JsonResponse(TempLanguage.lang_assigned_data(), safe=False)


def lang_assignment_json(request):
    return JsonResponse(TempLanguage.lang_assigned_map(), safe=False)


def lang_assignment_changed_json(request):
    return JsonResponse(TempLanguage.lang_assigned_changed_map(), safe=False)
