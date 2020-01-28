
## The Rugby Vault

A rugby union website that manages match and try highlights.

### `python manage.py runserver`

Runs the Django backend server in the development mode.<br />
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view it in the browser.

## REST Framework

### `GET /highlights/`

Obtain recent matches a tries for the homepage.

**URL parameters: league_name, league_try_name**

### `GET /player/`

Obtain information about a player.

**URL parameters: id, order, parameters(teams, years, leagues), pagenumber**

### `GET /team/`

Obtain information about a team.

**URL parameters: id, order, parameters(teams, years, leagues), pagenumber**

### `GET /matchhistory/`

Obtain the list of games between two teams.

**URL parameters: home team id, away team id**

### `GET /video/`

Get video data for a match or try.

**URL parameters: type, id**

### `POST /rating/`

Submit a rating for a match or try.

**URL parameters: type, googleid, id, rating**

### `GET /search/`

Get search results for a query.

**URL parameters: query**

### `GET /tryprocessing/`

Obtain the most recent match that has not been sliced into tries.

**URL parameters: id**

### `POST /addtry/`

Submit new tries after processing.

**URL parameters: tries, match id**

### `POST /report/`

Tags try or match in database as having an error.

**URL parameters: id, type**

### `GET /matches/`

Get all matches.

**URL parameters: order, parameters(teams, years, leagues), pagenumber**

### `GET /tries/`

Get all tries.

**URL parameters: order, parameters(teams, years, leagues), pagenumber**




## Periodic Scripts

### `python scraper_v2.py`


Scrapes BBC rugby fixtures list for recently completed games and adds matches to the database.


### `python youtube_links.py`

Searches YouTube for match highlights and assigns the video links to the corresponding matches in the database.

