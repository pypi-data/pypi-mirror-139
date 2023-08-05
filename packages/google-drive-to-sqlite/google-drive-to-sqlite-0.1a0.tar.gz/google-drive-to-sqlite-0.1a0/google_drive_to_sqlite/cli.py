from os import access
import click
import httpx
import itertools
import json
import sqlite_utils
import textwrap
import urllib.parse
from .utils import files_in_folder_recursive, paginate_files

# https://github.com/simonw/google-drive-to-sqlite/issues/2
GOOGLE_CLIENT_ID = (
    "148933860554-98i3hter1bsn24sa6fcq1tcrhcrujrnl.apps.googleusercontent.com"
)
# It's OK to publish this secret in application source code
GOOGLE_CLIENT_SECRET = "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"
DEFAULT_SCOPE = "https://www.googleapis.com/auth/drive.readonly"


def start_auth_url(google_client_id, scope):
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(
        {
            "access_type": "offline",
            "client_id": google_client_id,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "response_type": "code",
            "scope": scope,
        }
    )


DEFAULT_FIELDS = [
    "kind",
    "id",
    "name",
    "mimeType",
    "starred",
    "trashed",
    "explicitlyTrashed",
    "parents",
    "spaces",
    "version",
    "webViewLink",
    "iconLink",
    "hasThumbnail",
    "thumbnailVersion",
    "thumbnailLink",
    "viewedByMe",
    "createdTime",
    "modifiedTime",
    "modifiedByMe",
    "owners",
    "lastModifyingUser",
    "shared",
    "ownedByMe",
    "viewersCanCopyContent",
    "copyRequiresWriterPermission",
    "writersCanShare",
    "folderColorRgb",
    "quotaBytesUsed",
    "isAppAuthorized",
    "linkShareMetadata",
]


@click.group()
@click.version_option()
def cli():
    "Create a SQLite database of metadata from a Google Drive folder"


@cli.command()
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default="auth.json",
    help="Path to save token, defaults to auth.json",
)
@click.option("--google-client-id", help="Custom Google client ID")
@click.option("--google-client-secret", help="Custom Google client secret")
@click.option("--scope", help="Custom token scope")
def auth(auth, google_client_id, google_client_secret, scope):
    "Authenticate user and save credentials"
    if google_client_id is None:
        google_client_id = GOOGLE_CLIENT_ID
    if google_client_secret is None:
        google_client_secret = GOOGLE_CLIENT_SECRET
    if scope is None:
        scope = DEFAULT_SCOPE
    click.echo("Visit the following URL to authenticate with Google Drive")
    click.echo("")
    click.echo(start_auth_url(google_client_id, scope))
    click.echo("")
    click.echo("Then return here and paste in the resulting code:")
    copied_code = click.prompt("Paste code here", hide_input=True)
    response = httpx.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data={
            "code": copied_code,
            "client_id": google_client_id,
            "client_secret": google_client_secret,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "grant_type": "authorization_code",
        },
    )
    tokens = response.json()
    if "error" in tokens:
        message = "{error}: {error_description}".format(**tokens)
        raise click.ClickException(message)
    if "refresh_token" not in tokens:
        raise click.ClickException("No refresh_token in response")
    # Read existing file and add refresh_token to it
    try:
        auth_data = json.load(open(auth))
    except (ValueError, FileNotFoundError):
        auth_data = {}
    info = {"refresh_token": tokens["refresh_token"]}
    if google_client_id != GOOGLE_CLIENT_ID:
        info["google_client_id"] = google_client_id
    if google_client_secret != GOOGLE_CLIENT_SECRET:
        info["google_client_secret"] = google_client_secret
    if scope != DEFAULT_SCOPE:
        info["scope"] = scope
    auth_data["google-drive-to-sqlite"] = info
    open(auth, "w").write(json.dumps(auth_data, indent=4))


@cli.command()
@click.argument("url")
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option("--paginate", help="Paginate through all results in this key")
@click.option(
    "--nl", is_flag=True, help="Output paginated data as newline-delimited JSON"
)
@click.option("--stop-after", type=int, help="Stop paginating after X results")
def get(url, auth, paginate, nl, stop_after):
    "Make an authenticated HTTP GET to the specified URL"
    if not url.startswith("https://www.googleapis.com/"):
        if url.startswith("/"):
            url = "https://www.googleapis.com" + url
        else:
            raise click.ClickException(
                "url must start with / or https://www.googleapis.com/"
            )
    access_token = load_token(auth)

    if not paginate:
        response = httpx.get(
            url,
            headers={"Authorization": "Bearer {}".format(access_token)},
            timeout=10.0,
        )
        if response.status_code != 200:
            raise click.ClickException(
                "{}: {}\n\n{}".format(response.url, response.status_code, response.text)
            )
        click.echo(json.dumps(response.json(), indent=4))

    else:

        def paginate_all():
            i = 0
            next_page_token = None
            while True:
                params = {}
                if next_page_token is not None:
                    params["pageToken"] = next_page_token
                response = httpx.get(
                    url,
                    params=params,
                    headers={"Authorization": "Bearer {}".format(access_token)},
                    timeout=10.0,
                )
                data = response.json()
                if response.status_code != 200:
                    raise click.ClickException(json.dumps(data, indent=4))
                # Paginate using the specified key and nextPageToken
                if paginate not in data:
                    raise click.ClickException(
                        "paginate key {} not found in {}".format(
                            repr(paginate), repr(list(data.keys()))
                        )
                    )
                for item in data[paginate]:
                    yield item
                    i += 1
                    if stop_after is not None and i >= stop_after:
                        return

                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break

        if nl:
            for item in paginate_all():
                click.echo(json.dumps(item))
        else:
            for line in stream_indented_json(paginate_all()):
                click.echo(line)


@cli.command()
@click.argument(
    "database",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=False,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
@click.option("--folder", help="Files in this folder ID and its sub-folders")
@click.option("-q", help="Files matching this query")
@click.option("--full-text", help="Search for files with text match")
@click.option(
    "json_", "--json", is_flag=True, help="Output JSON rather than write to DB"
)
@click.option(
    "--nl", is_flag=True, help="Output newline-delimited JSON rather than write to DB"
)
@click.option("--stop-after", type=int, help="Stop paginating after X results")
def files(database, auth, folder, q, full_text, json_, nl, stop_after):
    """
    Retrieve metadata for files in Google Drive, and write to a SQLite database
    or output as JSON.

        google-drive-to-sqlite files files.db

    Use --json to output JSON, --nl for newline-delimited JSON:

        google-drive-to-sqlite files files.db --json

    Use a folder ID to recursively fetch every file in that folder and its
    sub-folders:

        google-drive-to-sqlite files files.db --folder 1E6Zg2X2bjjtPzVfX8YqdXZDCoB3AVA7i
    """
    if not database and not json_ and not nl:
        raise click.ClickException("Must either provide database or use --json or --nl")
    if q and full_text:
        raise click.ClickException("Cannot use -q and --full-text at the same time")
    if full_text:
        q = "fullText contains '{}'".format(full_text.replace("'", ""))
    access_token = load_token(auth)
    if folder:
        all = files_in_folder_recursive(access_token, folder, fields=DEFAULT_FIELDS)
    else:
        all = paginate_files(access_token, q=q, fields=DEFAULT_FIELDS)

    if stop_after:
        prev_all = all

        def new_all():
            i = 0
            for file in prev_all:
                yield file
                i += 1
                if i >= stop_after:
                    break

        all = new_all()

    if nl:
        for file in all:
            click.echo(json.dumps(file))
        return
    if json_:
        for line in stream_indented_json(all):
            click.echo(line)
        return
    db = sqlite_utils.Database(database)
    # Commit every 100 records
    for chunk in chunks(all, 100):
        with db.conn:
            db["files"].insert_all(chunk, pk="id", replace=True)


def load_token(auth):
    try:
        token_info = json.load(open(auth))["google-drive-to-sqlite"]
    except (KeyError, FileNotFoundError):
        raise click.ClickException("Could not find google-drive-to-sqlite in auth.json")
    # Exchange refresh_token for access_token
    data = httpx.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": token_info["refresh_token"],
            "client_id": token_info.get("google_client_id", GOOGLE_CLIENT_ID),
            "client_secret": token_info.get(
                "google_client_secret", GOOGLE_CLIENT_SECRET
            ),
        },
    ).json()
    if "error" in data:
        raise click.ClickException(str(data))
    return data["access_token"]


def stream_indented_json(iterator, indent=2):
    # We have to iterate two-at-a-time so we can know if we
    # should output a trailing comma or if we have reached
    # the last item.
    current_iter, next_iter = itertools.tee(iterator, 2)
    next(next_iter, None)
    first = True
    for item, next_item in itertools.zip_longest(current_iter, next_iter):
        is_last = next_item is None
        data = item
        line = "{first}{serialized}{separator}{last}".format(
            first="[\n" if first else "",
            serialized=textwrap.indent(
                json.dumps(data, indent=indent, default=repr), " " * indent
            ),
            separator="," if not is_last else "",
            last="\n]" if is_last else "",
        )
        yield line
        first = False
    if first:
        # We didn't output anything, so yield the empty list
        yield "[]"


def chunks(sequence, size):
    iterator = iter(sequence)
    for item in iterator:
        yield itertools.chain([item], itertools.islice(iterator, size - 1))
