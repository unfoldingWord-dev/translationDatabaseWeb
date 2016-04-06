from django.http import JsonResponse

from td.models import TempLanguage
from td.resources.models import Questionnaire


def questionnaire_json(request):
    # In the future, when we're ready to accommodate translations of the questionnaires, we should iterate through the
    #    queryset and construct the data content appropriately.
    questionnaire = Questionnaire.objects.latest('created_at')
    data = {
        "languages": [
            {
                "name": questionnaire.language.ln,
                "dir": questionnaire.language.direction,
                "slug": questionnaire.language.lc,
                "questionnaire_id": questionnaire.id,
                "questions": questionnaire.questions,
            }
        ]
    }
    return JsonResponse(data, safe=False)


def templanguages_json(request):
    return JsonResponse(TempLanguage.lang_assigned_data(), safe=False)


def lang_assignment_json(request):
    return JsonResponse(TempLanguage.lang_assigned_map(), safe=False)


def lang_assignment_changed_json(request):
    return JsonResponse(TempLanguage.lang_assigned_changed_map(), safe=False)
