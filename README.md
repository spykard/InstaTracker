# InstaTracker

A social engineering Instagram bot for (not so) malicious means.

[TODO] Download and Fork https://github.com/arc298/instagram-scraper. It outputs story locations to a .JSON, based on a list of Instagram users.

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
