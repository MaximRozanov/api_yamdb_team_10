from csv import DictReader

from django.core.management.base import BaseCommand

from reviews.models import (Category,
                            Genre,
                            Title,
                            GenreTitle,
                            User,
                            Review,
                            Comment
                            )

PATH = 'static/data/'

class Command(BaseCommand):

    def handle(self, *args, **options):
        for row in DictReader(open(f'{PATH}category.csv',
                                   encoding="utf8")):
            category = Category(id=row['id'],
                                name=row['name'],
                                slug=row['slug'])
            category.save()
        for row in DictReader(open(f'{PATH}genre.csv',
                                   encoding="utf8")):
            genre = Genre(id=row['id'],
                          name=row['name'],
                          slug=row['slug'])
            genre.save()
        for row in DictReader(open(f'{PATH}titles.csv',
                                   encoding="utf8")):
            title = Title(id=row['id'],
                          name=row['name'],
                          year=row['year'],
                          category=Category.objects.get(pk=row['category']),
                          )
            title.save()
        for row in DictReader(open(f'{PATH}users.csv',
                                   encoding="utf8")):
            users = User(id=row['id'],
                         username=row['username'],
                         email=row['email'],
                         role=row['role'],
                         bio=row['bio'],
                         first_name=row['first_name'],
                         last_name=row['last_name'],
                         )
            users.save()
        for row in DictReader(open(f'{PATH}review.csv',
                                   encoding="utf8")):
            review = Review(id=row['id'],
                            title=Title.objects.get(pk=row['title_id']),
                            text=row['text'],
                            author=User.objects.get(pk=row['author']),
                            score=row['score'],
                            pub_date=row['pub_date']
                            )
            review.save()
        for row in DictReader(open(f'{PATH}comments.csv',
                                   encoding="utf8")):
            comments = Comment(id=row['id'],
                               review=Review.objects.get(pk=row['review_id']),
                               text=row['text'],
                               author=User.objects.get(pk=row['author']),
                               pub_date=row['pub_date']
                               )
            comments.save()
        for row in DictReader(open(f'{PATH}genre_title.csv',
                                   encoding="utf8")):
            genre_title = GenreTitle(id=row['id'],
                                     title=Title.objects.get(
                                         pk=row['title_id']),
                                     genre=Genre.objects.get(
                                         pk=row['genre_id']),
                                     )
            genre_title.save()
