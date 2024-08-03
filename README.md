# Simple Twitter Clone Backend Solution

### Features

Every requirement from the PDF file. Nothing more, nothing less.

### Installation

1. Clone the repository with
   `git clone https://github.com/tBogoyski/HackSoft.git` and navigate to the new directory.
2. Create a virtual environment in the project root and activate it.
3. Install dependencies with `pip install -r requirements.txt`.
4. Apply migrations with `python manage.py migrate`.
5. Generate dummy data with `python manage.py generate_dummy_data`. This is a custom management command, which will
   populate the database with some dummy users, superusers and posts for easier manual testing of the functionality.
6. Run the server with `python manage.py runserver`.

### Usage

* The authentication is Token-based (`rest_framework.authentication.TokenAuthentication`). Which means that if you are
  using API testing software like Postman, you need to include the Authorization header in every request except the
  Login and Register, because they can be accessible by everyone. The token is extracted from the response body of a
  successful login. After that, every other request must have `Authorization` as key
  and `Token {{auth_token_from_login}}` as value in the headers of the request.
* The admin panel is the default django one, with slight modifications requested from the requirements. You can find a
  superuser email for loging in the admin panel from the logs of the `python manage.py generate_dummy_data` command (
  there is a log message for displaying a random superuser email). For simplicity reasons every user has the same
  password, which is `123456`.
* For running the automatic process of hard-deleting posts that were soft-deleted more than 10 days ago, you will need
  to set up a cron job on the machine hosting the project. To run the command manually
  use: `python manage.py delete_old_posts`.

### Testing

Every custom logic is covered with test cases.

- To run tests use: `python manage.py test`.
- To run standalone test use: `python manage.py test app_name.test_file_name.test_class.test_function`



