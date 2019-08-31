import os
import django
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MSCproject.settings")
django.setup()

from project.models import User, Student, Patch, Submission, Script, Round, Judgement

# ========= USER & STUDENT ===========
users = [
    {
        'username': 'theteacher',
        "email": "myteacher@trimit.com",
        "is_teacher": True,
        "is_student": False,
    }, {
        'username': 'student1',
        "email": "mystudent1@trimit.com",
        "is_teacher": False,
        "is_student": True,
    }, {
        'username': 'student2',
        "email": "mystudent2@trimit.com",
        "is_teacher": False,
        "is_student": True,
    }, {
        'username': 'student3',
        "email": "mystudent3@trimit.com",
        "is_teacher": False,
        "is_student": True,
    },
    {
        'username': 'student4',
        "email": "mystudent4@trimit.com",
        "is_teacher": False,
        "is_student": True,
    },
]
students = [{
    'username': 'student1',
    "group": 1,
}, {
    'username': 'student2',
    "group": 1,
}, {
    'username': 'student3',
    "group": 1,
}, {
    'username': 'student4',
    "group": 1,
},
 ]

# ========= PATCHES ===========
patches = [{
    'patch_title': 'MyPatch1',
    'patch_description': '1111111',
    'submission_date': datetime.datetime(2019, 2, 5),
    'peer_review_date': datetime.datetime(2019, 2, 15),
    'is_final': False,
}, {
    'patch_title': 'MyPatch2',
    'patch_description': '22222222222',
    'submission_date': datetime.datetime(2019, 2, 5),
    'peer_review_date': datetime.datetime(2019, 2, 15),
    'is_final': False,
}, {
    'patch_title': 'MyPatch3',
    'patch_description': '333333333',
    'submission_date': datetime.datetime(2019, 2, 5),
    'peer_review_date': datetime.datetime(2019, 2, 15),
    'is_final': True,
}]

# ========= SUBMISSION ===========
submissions = [{
    'patch': 'MyPatch2',
    'content': 'I got hit in the head with a can of soda yesterday. Luckily for me, it was a soft drink.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent1@trimit.com",
    'is_original': True,
}, {
    'patch': 'MyPatch2',
    'content': 'I’m super friendly with 25 letters of the alphabet.I just don’t know why.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent2@trimit.com",
    'is_original': True,
}, {
    'patch': 'MyPatch2',
    'content': 'My girlfriend broke up with me so I took her wheelchair. Guess who came crawling back.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent1@trimit.com",
    'is_original': True,
}, {
    'patch': 'MyPatch2',
    'content': 'My boss is going to fire the employee with the worst posture. I have a hunch it might be me.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent2@trimit.com",
    'is_original': True,
}, {
    'patch': 'MyPatch3',
    'content': 'C',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent3@trimit.com",
    'is_original': True,
}, {
    'patch': 'MyPatch3',
    'content': 'mysubmission3',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent3@trimit.com",
    'is_original': True,
}]


def add_stuff(model, info_dict):
    stuff, created = model.objects.get_or_create(**info_dict)
    if created: stuff.save()


def add_user(**kwargs):
    kwargs['password'] = 'h$iog892f'
    user = User.objects.create_user(**kwargs)
    user.save()


def add_student(username, group):
    user = User.objects.get(username=username)
    item, created = Student.objects.get_or_create(user=user, group=group)
    if created: item.save()


def add_submission(patch, content, published_date, student, is_original):
    item, created = Submission.objects.get_or_create(
        patch=Patch.objects.get(patch_title=patch),
        content=content,
        published_date=published_date,
        student=Student.objects.get(user__email=student),
        is_original=is_original
    )
    if created: item.save()


def clean_db():
    for tbl in (User, Script, Round, Judgement):
        tbl.objects.all().delete()


def populate():
    clean_db()
    User.objects.create_superuser('a', 'admin@example.com', 'a')

    for user in users:
        add_user(**user)

    for student in students:
        add_student(**student)

    for patch in patches:
        add_stuff(Patch, patch)

    for submission in submissions:
        add_submission(**submission)


if __name__ == '__main__':
    print("Starting trimit population script...")
    populate()
    print("DONE !")