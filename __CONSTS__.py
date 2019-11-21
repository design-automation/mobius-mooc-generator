import os

## Course Relative Path
COURSE_PATH = "test\\input"
OUTPUT_PATH = "test\\output"

# ASSETS
# these files will be included in the zip for edx upload
ASSET_FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'srt'] 

# FILENAMES
SETTINGS_FILENAME = "_settings" # settings files should end with this
MOB_ANSWER_FILENAME = "_ans.mob" # files that are answers should end with this
MOB_EXAMPLE_FILENAME = "_exp.mob" # files that are examples should end with this

# SETTINGS FOR AMAZON BUCKET FOR ANSWERS
MOB_S3_ANSWERS_BUCKET = "sct-mooc-answers" # the s3 bucket where answers will be uploaded (private)
MOB_S3_EXAMPLES_BUCKET = "sct-mooc-examples" # the s3 bucket where examples will be uploaded (public)

# MOBIUS URL
#MOB_URL = 'https://mobius.design-automation.net/' # the stable version
MOB_URL = 'https://design-automation.github.io/mobius-parametric-modeller-dev' # the dev version

# LANGUAGES
# available languages: ["us", "uk", "pt", "es", "zh", "fr", "de", "nl"]
LANGUAGES = ['en', 'zh', 'pt', 'fr']
ALL_LANGUAGES = {
    'en': 'English',
    'zh': 'Mandarin',
    'pt': 'Portuguese',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'nl': 'Dutch'
} 
