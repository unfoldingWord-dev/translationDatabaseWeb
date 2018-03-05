import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from djcelery.models import PeriodicTask

from td.models import TempLanguage, Country
from td.resources.models import Questionnaire


logger = logging.getLogger(__name__)


class QuestionnaireView(View):

    # I admit this is not the best solution nor a good practice. Our goal is to use the django REST framework to receive
    #     temporary language submission in the future.
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionnaireView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # In the future, when we're ready to accommodate translations of the questionnaires, we should iterate through
        #    the queryset and construct the data content appropriately.
        questionnaire = Questionnaire.objects.latest("created_at")
        data = {
            "languages": [
                {
                    "name": questionnaire.language.ln,
                    "dir": questionnaire.language.get_direction_display(),
                    "slug": questionnaire.language.lc,
                    "questionnaire_id": questionnaire.id,
                    "language_data": questionnaire.language_data,
                    "questions": questionnaire.questions,
                }
            ]
        }
        return JsonResponse(data, safe=False)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # First pass only. Will need more validation and refactoring
        data = list()
        answers = list()
        answer_list = list()
        answer_text_list = list()
        obj_list = list()
        try:
            message = ""
            data = request.POST if len(request.POST) else json.loads(request.body)
            questionnaire = Questionnaire.objects.get(pk=data.get("questionnaire_id"))
            field_mapping = questionnaire.field_mapping
            answers = json.loads(data.get("answers")) if len(request.POST) else data.get("answers")

            obj = TempLanguage(code=data.get("temp_code"), questionnaire=questionnaire, app=data.get("app"),
                               request_id=data.get("request_id"), requester=data.get("requester"),
                               answers=answers)

            for answer in answers:
                answer_list.append(answer)
                qid = str(answer.get("question_id"))
                if qid is not None and qid in field_mapping:
                    answer_text = answer.get("text")
                    answer_text_list.append(answer_text)
                    if field_mapping[qid] == "country":
                        obj.country = Country.objects.get(name__iexact=answer_text)
                        obj_list.append(obj.country and obj.country.name)
                    elif field_mapping[qid] == "direction":
                        obj.direction = "l" if answer_text.lower() == "yes" else "r"
                        obj_list.append(obj.direction)
                    else:
                        obj.__dict__[field_mapping[qid]] = answer_text
                        obj_list.append(obj.__dict__[field_mapping[qid]])

            obj.save()

        except Questionnaire.DoesNotExist:
            message = "questionnaire_id given does not return a matching Questionnaire object"
        except Country.DoesNotExist:
            message = "The answer for country results in an invalid lookup"
        except Exception as e:
            message = e.message

        return JsonResponse(
            {
                "status": "error" if message else "success",
                "message": message or "Request submitted",
                "debug": {
                    "data": data or "no data",
                    "answers": answers or "no answers",
                    "answer_list": answer_list or "no answer_list",
                    "answer_text_list": answer_text_list or "no answer_text_list",
                    "obj_list": obj_list or "no obj_list"
                }
            }
        )


def templanguages_json(request):
    return JsonResponse(TempLanguage.lang_assigned_data(), safe=False)


def lang_assignment_json(request):
    return JsonResponse(TempLanguage.lang_assigned_map(), safe=False)


def lang_assignment_changed_json(request):
    return JsonResponse(TempLanguage.lang_assigned_changed_map(), safe=False)


def celerybeat_healthz(request):
    if request.GET.get("key") != settings.CELERYBEAT_HEALTHZ_AUTH_KEY:
        return JsonResponse({"message": "Not authorized."}, status=403)

    succesful_tasks = []
    failing_tasks = []

    past_sixty_seconds = -60
    for task in PeriodicTask.objects.filter(enabled=True):
        # retrieve the estimated number of seconds until the next time the task should be ran
        seconds_until_next_execution = task.schedule.remaining_estimate(task.last_run_at).total_seconds()

        if seconds_until_next_execution > past_sixty_seconds:
            succesful_tasks.append(task.name)
        else:
            # the task should have been scheduled already
            failing_tasks.append(task.name)

    healthy = True
    status_code = 200
    if failing_tasks:
        healthy = False
        status_code = 503

    data = {
        "healthy": healthy,
        "failing": failing_tasks,
        "succesful": succesful_tasks,
    }
    return JsonResponse(data, status=status_code)
