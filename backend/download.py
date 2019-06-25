import typing
import uuid

# request don't work in docker for this website https://github.com/kennethreitz/requests/issues/3948
# import urllib3
import urllib.request
import backend


def download_url(
    url: str, save_directory: str, error_directory: str
) -> typing.Tuple[bool, str]:
    url_uuid = uuid.uuid1()
    download_success = False
    try:
        r = urllib.request.urlopen(url)
        if r.getcode() == 200:
            download_success = True
    except Exception as e:
        print(e)
    if download_success:
        filepath = f"{save_directory}/{url_uuid}"
        open(filepath, "wb").write(r.read())
    else:
        filepath = f"{error_directory}/{url_uuid}"
        open(filepath, "w").write("")
    return download_success, filepath


def parse_url_file(url_filepath: str, limit: int = 20):
    count = 0
    downloaded_files = []
    with open(url_filepath, "r+") as url_file:
        for url in url_file:
            success, result_filepath = download_url(
                url=url,
                save_directory=backend.BACKEND_DOWNLOAD_DIRECTORY,
                error_directory=backend.BACKEND_ERROR_DIRECTORY,
            )
            downloaded_files.append(
                {"success": success, "url": url, "filepath": result_filepath}
            )
            count += 1
            if count == limit:
                break
    return downloaded_files


if __name__ == "__main__":
    parse_url_file(url_filepath="urls.txt")
