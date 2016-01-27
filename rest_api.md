# REST API Overview

To view a listing of the available API options navigate to: 
[https://td.unfoldingword.org/api/](https://td.unfoldingword.org/api/) or
[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) if running locally.


By default, navigating to an API URL will display a summary and any data in HTML format.  To retrieve the data in a 
JSON format, put `?format=json` on the end of the URL.  Example:
[https://td.unfoldingword.org/api/](https://td.unfoldingword.org/api/) displays a summary, and
[https://td.unfoldingword.org/api/?format=json](https://td.unfoldingword.org/api/?format=json) returns JSON.


For some of the functions, you can also receive JSON by placing `.json` on the end of the URL.  So
[https://td.unfoldingword.org/api/publish-requests/?format=json](https://td.unfoldingword.org/api/publish-requests/?format=json) and
[https://td.unfoldingword.org/api/publish-requests.json](https://td.unfoldingword.org/api/publish-requests.json)
both return the same list.


### Creating a new Publish Request

You can create a new Publish Request by sending a POST request to 
[https://td.unfoldingword.org/api/publish-requests/?format=json](https://td.unfoldingword.org/api/publish-requests/?format=json).

This is the form I used during development. The `resource_type`, `language` and `source_text` fields are validated 
against the tD database, and you will receive an error if the values submitted are not valid.  Also, `requestor_email`
must be a valid e-mail address.

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test</title>
    </head>
    <body>
    <form action="http://127.0.0.1:8000/api/publish-requests/?format=json" method="post">
        <input type="text" name="requestor" value="Phil Hopper" /><br>
        <input type="text" name="resource_type" value="1" /><br>
        <input type="text" name="language" value="1868" /><br>
        <input type="text" name="checking_level" value="1" /><br>
        <input type="text" name="source_text" value="1747" /><br>
        <input type="text" name="source_version" value="3.2" /><br>
        <input type="text" name="contributors" value="contributors" /><br>
        <input type="text" name="requestor_email" value="philhopper@email.com" /><br>
        <input type="text" name="license_title" value="CC BY-SA 4.0" /><br>
        <input type="submit" value="Submit" />
    </form>
    </body>
    </html>
    