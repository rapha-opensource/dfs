# API Changes
I made very limited changes to the api as defined [here](https://app.swaggerhub.com/apis/aweiker/ToDo/1.0.0#/todo/addTask).

## GET /lists
I removed the nested 'tasks' field, as any incremental change to a list or a task would invalidate the entire returned value.
Generally speaking I prefer flatter resources, as opposed to deeply nested data, as it makes virtually everything easier
for the backend: smaller queries, faster serialization, less cache invalidation, etc.
That being said, ultimately, this could be a point a discussion around what the client expects.

## POST /list/{id}/tasks
Specs say input object takes an 'id', but that should be set by the server, not the client.
Specs don't specify the response body, so I chose to return the JSON-serialized newly created task.
