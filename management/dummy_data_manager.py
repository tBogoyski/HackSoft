import logging
import random

from faker import Faker

from posts.models import Post
from users.models import CustomUser

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

# Set faker's logging level to WARNING to suppress DEBUG messages
logging.getLogger('faker').setLevel(logging.WARNING)


class GenerateDummyDataManager:
    """
    Class used to generate dummy data for testing purposes.
    To use it, create an instance of the class and then call the desired methods.
    """
    fake = None

    def __init__(self):
        self.fake = Faker('en_US')

    @staticmethod
    def _generate_random_email(is_admin: bool = False) -> str:
        if is_admin:
            return f'{random.randint(1000000000, 9999999999)}@admin.com'
        return f'{random.randint(1000000000, 9999999999)}@example.com'

    def generate_users(self) -> None:
        PASSWORD_FOR_USERS = '123456'

        # Generate 10 random users
        for i in range(10):
            random_email = self._generate_random_email()

            if CustomUser.objects.filter(email=random_email).exists():
                logging.error(f'{random_email} already exists')
                continue

            user = CustomUser.objects.create_user(email=random_email, password=PASSWORD_FOR_USERS)
            user.name = f'{self.fake.first_name()} {self.fake.last_name()}'
            user.short_description = self.fake.text(max_nb_chars=35)
            user.profile_picture = f'images/{user.id}_profile_picture.png'
            user.save()
            logging.info(f'User {random_email} created')

        # Set 7 users to be valid
        for i in range(7):
            random_user = random.choice(CustomUser.objects.filter(is_superuser=False))
            random_user.is_valid = True
            random_user.save()
            logging.info(f'User {random_user.email} is set to be VALID')

        # Generate 3 superusers
        for i in range(3):
            random_email = self._generate_random_email(is_admin=True)

            if CustomUser.objects.filter(email=random_email).exists():
                logging.error(f'{random_email} already exists')
                continue

            CustomUser.objects.create_superuser(email=random_email, password=PASSWORD_FOR_USERS)
            logging.info(f'SuperUser {random_email} created')

    def generate_posts(self) -> None:
        # Generate 35 random posts
        for i in range(35):
            post = Post.objects.create(
                author=random.choice(CustomUser.objects.filter(is_valid=True)),
                content=self.fake.text(max_nb_chars=100),
            )
            liked_by_users = random.choices(CustomUser.objects.filter(is_valid=True), k=random.randint(0, 10))
            post.liked_by.set(liked_by_users)
            logging.info(f'Post with id {post.id} created')

        # Make 10 posts to be soft-deleted
        for i in range(10):
            post = random.choice(Post.objects.filter(deleted_at__isnull=True))
            post.soft_delete()
            logging.info(f'Post with id {post.id} is soft-deleted')
