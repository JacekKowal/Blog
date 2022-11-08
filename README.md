# Blog site using Django framework

## Screenshots

| Main page | Business tag | Post detail |
| -------|--------------|-----------------|
| <img src="./screenshots/main_page.png" width="200"> | <img src="./screenshots/business_tag.png" width="200"> | <img src="./screenshots/post_detail.png" width="200"> |

## Functionality

- custom manager
- tags(django-taggit) - filtering, recommendations
- email posts recommendations

## Installing

### Clone the project

```
git clone https://github.com/JacekKowal/Blog.git
```

### Install dependencies & activate virtualenv

```
pip install pipenv

pipenv install
pipenv shell
```

### Configure the settings (connection to the databasee)

1. Edit `Blog/settings.py` for database settings.

### Apply migrations

```
python Blog/manage.py migrate
```

### Running a development server

```
python Blog/manage.py runserver
```
