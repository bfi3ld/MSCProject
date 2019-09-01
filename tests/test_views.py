import django
from django.test import Client
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MSCproject.settings")
django.setup()

from project.views import *


def create_student():
    student_password = 'h$iog892f'
    user = User.objects.create_user(
        username='test_student',
        email="test_student@trimit.com",
        is_teacher=False,
        is_student=True,
        password=student_password,
    )
    user.save()
    student = Student.objects.create(user=user, group=99)
    student.save()
    return student, student_password


def create_patch():
    patch = Patch.objects.create(
        patch_title='TestPatch',
        patch_description='1111111',
        submission_date=datetime(2019, 2, 5),
        peer_review_date=datetime(2019, 2, 15),
        is_final=False,
    )
    patch.save()
    return patch


def test_make_submission():
    student, student_password = create_student()
    patch = create_patch()
    url = '/project/student_home/patch_view/{}/make_submission'.format(patch.id)

    c = Client()
    c.login(username=student.user.username, password=student_password)
    c.post(url, data={'content': "test_content"})

    last_submission = Submission.objects.latest('id')
    assert last_submission.content == "test_content"
    assert last_submission.student.id == student.id
    assert last_submission.student.user.username == student.user.username

    student.user.delete()
    patch.delete()



