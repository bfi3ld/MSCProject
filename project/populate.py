import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django; django.setup()

from project.models import User, Student, Patch, Submission, Submission_edits, 
    Peer_review_rubrik, Feedback, Judgement, Script, Round

from django.contrib.auth.models import User
from django.conf import settings
from django_countries import countries
from django.core.files import File
import os

POPULATE_DIR = os.path.join(settings.STATIC_DIR, 'population')

def add_user(username, password, email):
    user, created = User.objects.get_or_create(
        username=username, 
        password=password, 
        email=email)
    if created:
        user.save()

def populate():
    users = [
        {
            "username": "user1",
            "password": "1",
            "email": "user1@trimit.com",
        },
        {
            "username": "user2",
            "password": "2",
            "email": "user2@trimit.com",
        },
        {
            "username": "user3",
            "password": "3",
            "email": "user3@trimit.com",
        },
        {
            "username": "user4",
            "password": "4",
            "email": "user4@trimit.com",
        },
    ]

    page_pictures = {
        "dir": os.path.join(POPULATE_DIR, 'page_pictures'),
        "pic": [
            {
                'user': stylists[0]['username'],
                'img': 'page1.jpg',
            },
            {
                'user': stylists[0]['username'],
                'img': 'page2.jpg',
            },
            {
                'user': stylists[0]['username'],
                'img': 'page3.jpg',
            },
        ]
    }



    def add_userprofile(username):
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.save()

    def get_standardized_country(country):
        for c in list(countries):
            if country.lower() == c[1].lower() or country.lower == c[0].lower:
                matched_country = country
        return matched_country

    def add_page(username, hairdresser):
        user = User.objects.get(username=username)

        standardized_country = get_standardized_country(hairdresser['country'])

        page_info = dict(
            name=hairdresser['name'],
            street_address=hairdresser['str'], 
            city=hairdresser['city'], 
            country=standardized_country
        )

        page = Page.objects.update_or_create(
            user=user, 
            defaults=page_info,
        )[0]

        page.save()

    def add_review(username, pagename, ratings, comment, img):
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        page = Page.objects.get(user=User.objects.get(username=pagename))
        atmosphere_rating, price_rating, service_rating = ratings
        review = Review.objects.get_or_create(
            page=page, user=user, atmosphere_rating=atmosphere_rating, 
            price_rating=price_rating, service_rating=service_rating,
            comment=comment
        )[0]
        if img is not None:
            filedir = os.path.join(review_pictures_dir, img)
            review.picture.save(img, File(open(filedir, 'rb')))

        review.save()

    def delete_user(username):
        user = User.objects.get(username=username)
        user.delete()

    def add_profile_picture(dir, username, filename):
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        filedir = os.path.join(dir, filename)
        user.profile_picture.save(filename, File(open(filedir, 'rb')))

    def add_hair_picture(dir, username, filename):
        filedir = os.path.join(dir, filename)
        hairimage = UserHairImage.objects.create(user=UserProfile.objects.get(user=User.objects.get(username=username)))
        hairimage.image.save(filename, File(open(filedir, 'rb')))
        hairimage.save()

    def add_page_picture(dir, username, filename):
        filedir = os.path.join(dir, filename)
        pageimage = PageImage.objects.create(page=Page.objects.get(user=User.objects.get(username=username)))
        pageimage.image.save(filename, File(open(filedir, 'rb')))
        pageimage.save()

    def delete_duplicatable_objects():
        hairimages = UserHairImage.objects.all()
        pageimages = PageImage.objects.all()
        reviews = Review.objects.filter(user__isnull=True)

        for hi in hairimages:
            hi.delete()

        for pi in pageimages:
            pi.delete()

        for r in reviews:
            r.delete()

    delete_duplicatable_objects()

    for us in users:
        add_user(us['username'], us['password'], us['email'])
        add_userprofile(us['username'])

    i = 0

    for hs in stylists:
        add_user(hs['username'], hs['password'], hs['email'])
        hairdresser = hairdresser_pages[i]
        u = User.objects.get(username=hs['username'])
        add_page(u, hairdresser)
        i += 1

    for rev in reviews:
        add_review(rev['user'], rev['page'], rev['rating'], rev['comment'], rev['img'])

    for u in User.objects.all():
        for p in UserProfile.objects.filter(user=u):
            print("- {0} - UserProfile {1}".format(str(u), str(p)))
            for r in Review.objects.filter(user=UserProfile.objects.filter(user=u)):
                print("\t - Review {0}".format(str(r)))
        for p in Page.objects.filter(user=u):
            print("- {0} - HairdresserPage {1}".format(str(u), str(p)))
        for p in Page.objects.filter(user=u):
            for r in Review.objects.filter(page=p):
                print("\t- Review {0}".format(str(r)))

    for u in deleting_users:
        delete_user(username=u['username'])
        print("- DELETED - {0}".format(u['username']))

    for pp in profile_pictures['pic']:
        add_profile_picture(profile_pictures['dir'], pp['user'], pp['img'])

    for hp in hair_pictures['pic']:
        add_hair_picture(hair_pictures['dir'], hp['user'], hp['img'])

    for pp in page_pictures['pic']:
        add_page_picture(page_pictures['dir'], pp['user'], pp['img'])

    for treatment in hairdresser_treatments:
        slug = treatment.pop('hairdresser_slug')
        page = Page.objects.get(slug=slug)

        Treatment.objects.get_or_create(
            page=page,
            **treatment
        )[0].save()

if __name__ == '__main__':
    print("Starting trimit population script...")
    populate()
