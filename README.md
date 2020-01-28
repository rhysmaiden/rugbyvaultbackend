
## The Rugby Vault

A rugby union website that manages match and try highlights.

### `python manage.py runserver`

Runs the Django backend server in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

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



### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `yarn build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify
# rugbyvaultfrontend
