# API Changes
I made very limited changes to the api as defined [here](https://app.swaggerhub.com/apis/aweiker/ToDo/1.0.0#/todo/addTask).

## POST /list/{id}/tasks
Specs say input object takes an 'id', but that should be set by the server, not the client.
Specs don't specify the response body, so I chose to return the JSON-serialized newly created task.


# Implementation alternatives
Stuff I could have done differently or chose not to do in the interest of time.

. do client data validation via lib (e.g. Marshmallow)
. use a library (e.g. 'sqlalchemy') to add ORM layer instead of manual SQL.
 (would be most helpful for type mismatch between Python and SQL)

