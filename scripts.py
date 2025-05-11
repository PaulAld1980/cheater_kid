import random
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

commendations = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def get_schoolkid_by_name(full_name):
    try:
        return Schoolkid.objects.get(full_name__icontains=full_name)
    except Schoolkid.DoesNotExist:
        raise ValueError("Ученик с таким именем не найден!")
    except Schoolkid.MultipleObjectsReturned:
        raise ValueError("Найдено несколько учеников с таким именем.")


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_random_commendation(schoolkid, subject_title):
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__icontains=subject_title
    ).order_by('date').last()

    if not lesson:
        print(f"Ошибка: Урок по предмету '{subject_title}' не найден.")
        return

    commendation_text = random.choice(commendations)
    Commendation.objects.create(
        text=commendation_text,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )

    print(f'Добавлена похвала по предмету "{subject_title}": "{commendation_text}"')


def main():
    schoolkid_name = input("Введите имя ученика: ")
    subject_title = input("Введите название предмета: ")

    try:
        schoolkid = get_schoolkid_by_name(schoolkid_name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_random_commendation(schoolkid, subject_title)
    except ValueError as error:
        print(f"Ошибка: {error}")


main()
