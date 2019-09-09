import os
import django
import datetime
from django.db import connection
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MSCproject.settings")
django.setup()

from project.models import User, Student, Patch, Submission, Script, Round, Judgement

# ========= USER & STUDENT ===========
users = [
    {
        'username': 'theteacher',
        "email": "myteacher@a.com",
        "is_teacher": True,
        "is_student": False,
    }, {
        'username': 'student1',
        "email": "mystudent1@a.com",
        "is_teacher": False,
        "is_student": True,
    }, {
        'username': 'student2',
        "email": "mystudent2@a.com",
        "is_teacher": False,
        "is_student": True,
    }, {
        'username': 'student3',
        "email": "mystudent3@a.com",
        "is_teacher": False,
        "is_student": True,
    },
    {
        'username': 'student4',
        "email": "mystudent4@a.com",
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
    'patch_title': 'Patch1',
    'patch_description': 'This is the instruction for the first patch',
    'submission_date': datetime.datetime(2019, 7, 5),
    'peer_review_date': datetime.datetime(2019, 7, 15),
    'is_final': False,
}, {
    'patch_title': 'Patch2',
    'patch_description': 'This is the instruction for the second patch',
    'submission_date': datetime.datetime(2019, 9, 5),
    'peer_review_date': datetime.datetime(2019, 9, 15),
    'is_final': False,
},
 {
    'patch_title': 'Final quilt',
    'patch_description': 'This is the instruction for final quilt',
    'submission_date': datetime.datetime(2019, 9, 5),
    'peer_review_date': datetime.datetime(2019, 9, 15),
    'is_final': True,
}]

# ========= SUBMISSION ===========
submissions = [{
    'patch': 'Patch1',
    'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent1@a.com",
    'is_original': True,
}, {
    'patch': 'Patch1',
    'content': 'Nullam vehicula ipsum a arcu cursus vitae congue. Tellus cras adipiscing enim eu turpis egestas pretium aenean. Est lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque. Aenean vel elit scelerisque mauris pellentesque pulvinar pellentesque habitant. Adipiscing elit duis tristique sollicitudin nibh sit amet commodo nulla. Sed ullamcorper morbi tincidunt ornare massa. Aliquam vestibulum morbi blandit cursus risus at. ',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent2@a.com",
    'is_original': True,
}, {
    'patch': 'Patch1',
    'content': 'At tellus at urna condimentum mattis pellentesque id. Sed cras ornare arcu dui vivamus arcu felis bibendum ut. Aliquam ultrices sagittis orci a scelerisque purus semper eget. Elit duis tristique sollicitudin nibh sit amet. At lectus urna duis convallis convallis tellus. Quis risus sed vulputate odio. Id neque aliquam vestibulum morbi blandit.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent3@a.com",
    'is_original': True,
}, {
    'patch': 'Patch1',
    'content': 'Sed felis eget velit aliquet sagittis id consectetur. Mattis nunc sed blandit libero volutpat sed cras. Blandit aliquam etiam erat velit. Nibh venenatis cras sed felis. Viverra accumsan in nisl nisi. Enim blandit volutpat maecenas volutpat blandit. Augue eget arcu dictum varius duis at. Amet volutpat consequat mauris nunc congue. Morbi leo urna molestie at elementum eu facilisis sed odio. Massa tincidunt nunc pulvinar sapien.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent4@a.com",
    'is_original': True,
}, {
    'patch': 'Patch2',
    'content': 'Vitae congue eu consequat ac felis donec et odio. Congue nisi vitae suscipit tellus mauris a diam maecenas sed. Metus dictum at tempor commodo ullamcorper a. Dictum non consectetur a erat nam at lectus. Adipiscing at in tellus integer feugiat. Egestas fringilla phasellus faucibus scelerisque. Fringilla est ullamcorper eget nulla facilisi etiam dignissim.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent3@a.com",
    'is_original': True,
}, {
    'patch': 'Patch2',
    'content': 'Enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac. Rhoncus urna neque viverra justo. Vitae congue eu consequat ac felis donec et odio. Congue nisi vitae suscipit tellus mauris a diam maecenas sed. Metus dictum at tempor commodo ullamcorper a. Dictum non consectetur a erat nam at lectus. Adipiscing at in tellus integer feugiat. Egestas fringilla phasellus faucibus scelerisque.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent1@a.com",
    'is_original': True,
}, {
    {
    'patch': 'Patch2',
    'content': 'Enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac. Rhoncus urna neque viverra justo. Vitae congue eu consequat ac felis donec et odio. Congue nisi vitae suscipit tellus mauris a diam maecenas sed. Metus dictum at tempor commodo ullamcorper a. Dictum non consectetur a erat nam at lectus. Adipiscing at in tellus integer feugiat. Egestas fringilla phasellus faucibus scelerisque.',
    'published_date': datetime.datetime(2019, 2, 5),
    'student': "mystudent1@a.com",
    'is_original': True,
}
}
]


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
    # with connection.cursor() as cursor:
    #     cursor.execute("ALTER TABLE project_judgement AUTO_INCREMENT=1;")
    # subprocess.call("python manage.py sqlsequencereset project".split())


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
    print("Starting population script...")
    populate()
    print("DONE !")