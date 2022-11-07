import re
import unicodedata
import os
filepath = os.path.abspath(os.curdir)

# Pass Snipd Mass Export Filename
# i.e "snipd_export_2022-11-07_13-40.md"
snipd_file_name = 'snipd_export_2022-11-07_13-40.md'

# Read all podcast snips to text
with open(snipd_file_name, encoding="utf8") as f:
    file_text = f.read()

# Split snipd global text file into indivial podcast text list.
podcasts_text_list = re.split('(?<!#)#(?!#|\w)', file_text)


def slugify(value, allow_unicode=False):
    """
    - Function for converting podcast titles to savable filenames
    - Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '-', value)
    return value


def podcast_details(podcast_text):
    """
    Podcast Processing Function
    """
    pod_dict = {}
    pod_dict['podcast_title'] = re.findall('Episode\s*title\s*::\s*\[\[(.*?)\]\]', podcast_text)[0]
    pod_dict['filename'] = slugify(pod_dict['podcast_title'])
    pod_dict['podcast_show'] = re.findall('Show\s*::\s*\[\[(.*?)\]\]', podcast_text)[0]
    pod_dict['podcast_note'] = '#' + podcast_text
    return pod_dict


# Process Podcasts
podcast_dict_list = []
for podcast_text in podcasts_text_list[1:]:
    podcast_dict = podcast_details(podcast_text)
    podcast_dict_list.append(podcast_dict)

# Save Podcasts
for podcast_dict in podcast_dict_list:
    file_name = podcast_dict['podcast_title']
    with open(f'{filepath}\\podcast_notes\\{podcast_dict["filename"]}.md', "w", encoding="utf8") as md_file:
        md_file.write(podcast_dict['podcast_note'])
