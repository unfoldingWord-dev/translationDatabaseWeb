import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from td.models import TempLanguage, Country
from td.resources.models import Questionnaire


# I admit this is not the best solution nor a good practice. Our goal is to use the django REST framework to receive
#    temporary language submission in the future.
@csrf_exempt
def questionnaire_json(request):
    if request.method == "GET":
        # In the future, when we're ready to accommodate translations of the questionnaires, we should iterate through
        #    the queryset and construct the data content appropriately.
        questionnaire = Questionnaire.objects.latest("created_at")
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
    elif request.method == "POST":
        # First pass only. Will need more validation and refactoring
        try:
            message = ""
            data = request.POST
            questionnaire = Questionnaire.objects.get(pk=data.get("questionnaire_id"))
            field_mapping = questionnaire.field_mapping

            obj = TempLanguage(code=data.get("temp_code"), questionnaire=questionnaire, app=data.get("app"),
                               request_id=data.get("request_id"), requester=data.get("requester"),
                               answers=json.loads(data.get("answers")))

            for a in json.loads(data.get("answers")):
                qid = a.get("question_id")
                if qid is not None and qid in field_mapping:
                    if field_mapping[qid] == "country":
                        obj.country = Country.objects.get(name__iexact=a["text"])
                    else:
                        obj.__dict__[field_mapping[qid]] = a["text"]

            obj.save()

        except Exception as e:
            message = e.message

        return JsonResponse({"status": "error" if message else "success", "message": message or "Request submitted"})


def templanguages_json(request):
    return JsonResponse(TempLanguage.lang_assigned_data(), safe=False)


def lang_assignment_json(request):
    return JsonResponse(TempLanguage.lang_assigned_map(), safe=False)


def lang_assignment_changed_json(request):
    return JsonResponse(TempLanguage.lang_assigned_changed_map(), safe=False)
