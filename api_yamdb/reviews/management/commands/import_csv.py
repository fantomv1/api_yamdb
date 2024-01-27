import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)


def find_data(csv_file):
    """Найти и открыть нужный файл csv."""
    csv_path = os.path.join(settings.BASE_DIR, "static/data", csv_file)
    return csv.reader(open(csv_path), delimiter=",")


class Command(BaseCommand):
    help = "Импортирует данные из csv файлов."

    def handle(self, *args, **options):
        reader = find_data("category.csv")
        next(reader, None)  # Пропускает первую строку
        for row in reader:
            data, status = Category.objects.get_or_create(
                id=row[0], name=row[1], slug=row[2]
            )

        reader = find_data("genre.csv")
        next(reader, None)
        for row in reader:
            data, status = Genre.objects.get_or_create(
                id=row[0], name=row[1], slug=row[2]
            )

        reader = find_data("titles.csv")
        next(reader, None)
        for row in reader:
            data, status = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=get_object_or_404(Category, id=row[3]),
            )

        reader = find_data("genre_title.csv")
        next(reader, None)
        for row in reader:
            obj, created = GenreTitle.objects.get_or_create(
                id=row[0], title_id=row[1], genre_id=row[2]
            )

        reader = find_data("review.csv")
        next(reader, None)
        for row in reader:
            data, status = Review.objects.get_or_create(
                id=row[0],
                title_id=get_object_or_404(Title, id=row[1]),
                text=row[2],
                author=get_object_or_404(User, id=row[3]),
                score=row[4],
                pub_date=row[5],
            )

        reader = find_data("comments.csv")
        next(reader, None)
        for row in reader:
            data, status = Comment.objects.get_or_create(
                id=row[0],
                review_id=get_object_or_404(Review, id=row[1]),
                text=row[2],
                author=get_object_or_404(User, id=row[3]),
                pub_date=row[4],
            )

        reader = find_data("users.csv")
        next(reader, None)
        for row in reader:
            data, status = User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6],
            )

        self.stdout.write(self.style.SUCCESS("Данные загружены!"))
