from django.test import Client
import django
import os
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MSCproject.settings")
django.setup()


def get_allow_redirect(c, url, redirect_url, expect):
    url = '/project/' + url
    if redirect_url is None:
        response = c.get(url)
        assert response.status_code == expect
    else:
        response = c.get(url, follow=True)
        last_url, status_code = response.redirect_chain[-1]
        assert last_url.startswith(redirect_url)
        

@pytest.mark.parametrize('url, redirect_url', [
    ('teacher_home', None),
    ('teacher_home/teacher_patch_view/1', None),
    ('teacher_home/teacher_patch_view/1/add_rubric', None),
    ('teacher_home/add_student', None),
    ('teacher_home/add_patch', None),
    # ('teacher_home/teacher_patch_view/1/new_judge_session', '/project/teacher_home/teacher_patch_view/1/acj'),
    # ('teacher_home/teacher_patch_view/1/acj/1/1', ''),
])
def test_teacher_allowed_pages(url, redirect_url):
    c = Client()

    # teacher gets in
    c.login(username='theteacher', password='h$iog892f')
    get_allow_redirect(c, url, redirect_url, expect=200)
    c.logout()

    # student redirected
    c.login(username='student1', password='h$iog892f')
    get_allow_redirect(c, url, redirect_url='/', expect=302)
    c.logout()

    # anonymous redirected
    get_allow_redirect(c, url, redirect_url='/', expect=302)
    c.logout()


@pytest.mark.parametrize('url, redirect_url', [
    ('student_home', None),
    ('student_home/patch_view/1', None),
    ('student_home/patch_view/1/give_feedback', None),
    # ('student_home/patch_view/1/give_feedback/group_submission/1', None),
    # ('student_home/patch_view/1/give_feedback/group_submission/1/submit_peer_review/<int:rubrik>', None),
    ('student_home/patch_view/1/view_feedback', None),
    ('student_home/patch_view/1/view_feedback/edit_submission', None),
    ('student_home/patch_view/1/make_submission', None),
    ('student_home/final_patch_view', None),
    ('student_home/final_patch_view/stitch_patches', None),
])
def test_student_allowed_pages(url, redirect_url):
    c = Client()

    # teacher gets in
    c.login(username='theteacher', password='h$iog892f')
    get_allow_redirect(c, url, redirect_url='/', expect=302)
    c.logout()

    # student redirected
    c.login(username='student1', password='h$iog892f')
    get_allow_redirect(c, url, redirect_url, expect=200)
    c.logout()

    # anonymous redirected
    get_allow_redirect(c, url, redirect_url='/', expect=302)
    c.logout()
