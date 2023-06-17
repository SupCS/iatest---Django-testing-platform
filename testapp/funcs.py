from random import randint

from .models import Answer


def create_random_chars(nbr_of_chars):
    return "".join(chr(randint(97, 122)) for i in range(nbr_of_chars))


def get_correct(quetion):
    corrects = []
    answers = Answer.objects.filter(quetion=quetion)
    for answer in answers:
        if answer.is_correct:
            corrects.append(answer.id)
    if len(corrects) == 1:
        return corrects[0]
    return corrects


def cut_by_page(queryset, page):
    s, e = page * 5 - 5, page * 5
    if len(queryset) >= 5:
        try:
            out = queryset[s:e]
        except IndexError:
            out = queryset[:5]
        return out
    return queryset
