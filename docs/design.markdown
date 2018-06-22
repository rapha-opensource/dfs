## Design Notes
* meant to be run inside a container (Docker) for production, or directly on the developer's machine for development.
* should be fronted by NginX+WSGI (gUnicorn) or similar for protection and scaling, if this were to be shipped.
* alt: work from raw socket to show off some ninja sk33llz, we don't need no framework!
* use async framework for scalability
* no string localization

# Implementation alternatives
Stuff I could have done differently or chose not to do in the interest of time.

. use a real SQL db as opposed to SQLite3, which is just easier here for ease of installation and testing.
. do client data validation via lib (e.g. Marshmallow)
. use a library (e.g. 'sqlalchemy') to add ORM layer instead of manual SQL.
 (would be most helpful for type mismatch between Python and SQL)

