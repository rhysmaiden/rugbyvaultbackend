# The Rugby Vault

A rugby union website highlight that collects match and try highlights.

## Environments

The application was developed on MacOS Catalina and has been tested on all newer versions of MacOS.

### Prerequisites

* python3
* pip3



### Installing

How to get started with the rugby vault back-end

1. Clone Repository

```
git clone https://github.com/rhysmaiden/rugbyvaultbackend.git
```

2. Download all project dependencies

```
pip3 install -r requirements.txt
```

### Usage Instructions

Start server

```
python3 manage.py runserver
```

### Scheduled Scripts

Fetch the matches from ESPN and put them in the database for processing - Runs daily
```
python3 scraper_v2.py
```

Fetch youtube links for each of the matches created from the script above. - Runs daily

```
python3 find_youtube_links.py
```

### Manual Processing

The tool for finding the time of tries in match highlights can be found at ```/tryprocessing```

1. Click the set current time button every time there is a transition between tries. This will populate the time from the youtube video into the form fields. 
2. Manually adjust times if there are any issues such as:
- Videos of non-tries in the highlights
- In large score games they don't always include every try
3. If the video is not displaying or the video is from the incorrect match, click the error button.

**Future Development**
- [] Remove database from git repository
- [] Convert database to postgresql
- [] Split api into multiple files
- [] Find a way to split video files without human input

### Built With

* [Django](https://docs.djangoproject.com/en/3.0/) - The web framework used


### Authors

* **Rhys Maiden** - *Sole contributor* - [rhysmaiden](https://github.com/rhysmaiden)
