from django import template
from msc.questionnaire.models import Questionnaire
from msc.organisation.models import Organisation
from msc.authentication.models import Share

from django.template.loader import get_template
from django.conf import settings

register = template.Library()


@register.filter
def keyvalue(dict, key):
    try:
        return dict[key]
    except KeyError:
        return ''

@register.filter
def split_timeuntil(duration):
    return duration.split(",")[0]

@register.filter
def submitted_questionnaires(questionnaire, user):
    submitted_responses = questionnaire.response_set.filter(
        is_submitted=True
    )
    total_count = 0

    organisation_shares = Share.objects.filter(
        relationship="viewer",
        target_content_type__model="questionnaire",
        sharer_content_type__model="organisation",
        target_object_id=questionnaire.id
    ).order_by("sharer_object_id").distinct()

    if user.is_national:
        total_count = organisation_shares.count()
    elif user.is_provincial:

        sharer_ids = [
            share.sharer_object_id for share in organisation_shares if share.sharer.parent == user.organisation
        ]
        total_count = len(sharer_ids)
        submitted_responses = submitted_responses.filter(
            organisation_id__in=sharer_ids
        )

    submitted_response_count = submitted_responses.count()
    #TODO: Better way to prevent division by zero
    perc = 0.0
    if total_count:
        perc = round((float(submitted_response_count)/total_count)*100,1)

    html = get_template(f"subtemplate/progress_bar.html").render({
        "text": f'{submitted_response_count}/{total_count}',
        "per": perc,
    })

    return html


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def reminder_options(questionnaire, user):
    return questionnaire.get_reminder_options(user)


@register.filter
def question_summary(question, user):
    if question.input_type in settings.SUMMARY_INPUT_TYPES:
        questionnaire = question.section.questionnaire

        response_filters = {"is_submitted": True}
        if user.is_provincial:
            child_organisations = user.organisation.get_children(
                False
            ).values_list("id", flat=True)
            response_filters["organisation_id__in"] = child_organisations

        submitted_responses = questionnaire.response_set.filter(**response_filters)
        summary = question.get_summary_results(submitted_responses)
        per = "0%"
        try:
            max_count = summary["max"]["count"]
            total = summary["total_response_count"]
            max_choice = summary["max"]["choice"]
            per = round((float(max_count)/total)*100,1)
            return f'{max_count}/{total} ({per}%) - {max_choice}'
        except:
            pass

    return "-"
