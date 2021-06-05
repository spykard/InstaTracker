# InstaTracker

A social engineering Instagram bot for (not so) malicious means.

## Running the Tool

1. Install the required Python packages/dependencies.
2. Set the appropriate configuration parameters, by creating `/tracking/ActivePosts.txt` that includes a list of the posts to track, using the following format:

``` bash
https://www.instagram.com/p/CPoWUvmn7Eo/
...
```

3. Also set the appropriate Instagram account login information in the file `/config/config.ini`, using the following format:

``` ini
[Settings]
username = xxx
password = xxx
...
```

4. Make sure that a `source.csv` file exists in `/data`, following the format described in a following [Chapter](#Input/Output-Format).

5. Run the Python script:

``` bash
python mainPosts.py
```

## Input/Output CSV Format

| instagram_url | instagram_id | instagram_name | is_public | done_posts | high_priority | has_story_available | score | notes |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| https://www.instagram.com/bmw/ | ... | ... | | | | | | |

## Troubleshooting - Error 429: Too Many Requests

In case of [Error 429](https://instaloader.github.io/troubleshooting.html#too-many-requests), where too many requests have been sent to the server and the tool gets automatically redirected to Log In, perform the following actions: Either re-run the `export_firefox_session.py` to get a fresh session and/or try a different Instagram Account.

## Incorporate Instagram Scraper for Automatic Analysis

After we acquire the output data, we perform manual analysis. If automatic analysis of Instagram Stories is needed, [InstagramScraper](https://github.com/arc298/instagram-scraper) could be used, featuring location detection for stories. It has the ability to output story locations to a .json file, based on a list of Instagram users. Some examples:

``` bash
instagram-scraper user_xxx -u username -p password -t story --filter-location 109790383963906 --include-location --location
instagram-scraper --tag athens -u username -p password -t story --include-location --filter-location 109790383963906
instagram-scraper trolololer86 -u username -p password -t story --filter-location 14294616 --include-location --location
```
