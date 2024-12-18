# Django Blog and Dashboard Application

This project is a Django-based web application that includes a blog and user dashboard with authentication, post management, and profile editing features.

## Features
- **User Authentication**
  - Custom User Model ( registration with phone and email)
  - Signup, login, and logout functionality.
  - Verify Registration with OTP Code
  - Creates user information based on the session
- **User Dashboard**
  - Manage posts (create, update, delete).
  - Edit user profiles.
- **Blog**
  - Article creation, Like Article, FavoriteArticle, commenting and reply comment.
  - Article, comment and reply comment management in the admin interface.
- **Admin Panel**
  - Manage users, posts, and profiles.
  - Custom admin model configuration.
- **Profile Management**
  - Users can edit their profiles with form validation.
  - Automatic profile creation on user registration.

## Project Structure

```bash
.
├── accounts
│   ├── admin.py                    # Accounts admin configuration
│   ├── apps.py                     # Accounts apps configuration
│   ├── forms.py                    # Accounts Form (user creation and registration form, change info, profile, login, verify)
│   ├── models.py                   # Accounts models (User, Profile, OTPCode)
│   ├── templates
│   │   └── accounts
│   │       ├── profile.html
│   │       ├── register.html
│   │       ├── user_login.html
│   │       └── verify_code.html
│   ├── urls.py                     # Accounts URL configuration
│   └── views.py                    # Accounts views
├── blog
│   ├── admin.py                    # Blog admin configuration
│   ├── apps.py                     # Blog apps configuration
│   ├── forms.py                    # Blog forms (Comment, CommentReply, ArticleEditForm)
│   ├── models.py                   # BLog models (Article, Category, tag, FavoriteArticle, Comment, Vote)
│   ├── templates
│   │   └── blog
│   │       ├── articles.html
│   │       ├── detail.html
│   │       └── edit.html
│   ├── urls.py                     # Blog URL configuration
│   └── views.py                    # Blog views
├── core
│   ├── asgi.py
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Main URL configuration
│   └── wsgi.py                     # WSGI entry point
├── db.sqlite3                      # SQLite database file
├── LICENSE
├── manage.py                       # Django's command-line utility
├── media                           # Media files (user uploads)
├── README.md
├── requirements.txt                # Python dependencies
├── templates
│   ├── 404.html
│   ├── base.html
│   └── inc
│       └── messages.html
└── utils.py                    # Send OTP code
```

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone git@github.com:cyhssin/DialogueCode.git
   ```

2. Install dependencies:

   ```bash
   python -m venv .env
   source ./.env/bin/activate
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Access the site at `http://127.0.0.1:8000/`.

## Custom Commands

- **Populate Data**: Use the custom management command to generate fake data for testing:

  ```bash
  python manage.py populate_data
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Developed by [cyhssin](https://github.com/cyhssin)