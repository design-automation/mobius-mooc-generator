import os
## Course Relative Path
COURSE_PATH = "test\\input"
OUTPUT_PATH = "test\\output"

# SETTINGS FOR EDX
SETTINGS_FILENAME = "_settings" # settings files should end with this
LANGUAGES = ['en', 'zh', 'pt', 'fr'] # available languages: ["us", "uk", "pt", "es", "zh", "fr", "de", "nl"]
ASSET_FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'srt'] # these files will be included in the zip for edx upload

## SETTINGS FOR AMAZON
S3_FILE_EXTENSIONS = ["mob"] # these files will be uploaded to amazon
S3_ANSWER_FILENAME = "_ans" # files that are answers should end with this
S3_ANSWERS_BUCKET = "sct-mooc-answers" # the s3 bucket where answers will be uploaded (private)
S3_EXAMPLES_BUCKET = "sct-mooc-examples" # the s3 bucket where examples will be uploaded (public)

