#MOOC_NAME
EDX_COURSE = 'SCT04' 
EDX_EXTERNAL_GRADER_QUEUENAME = 'spatial_computational_thinking'

## Course Relative Path
# COURSE_PATH = 'test\\input'
# OUTPUT_PATH = 'test\\output'

COURSE_PATH = 'C:\\Dropbox\\Files\\Software\\AwsCommitPJ\\spatial-computational-thinking-mooc\\mooc1-procedural-modelling'
OUTPUT_PATH = 'C:\\Data\\edx-generator\\mooc1'

# ASSETS
# these files will be included in the zip for edx upload
ASSET_FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'srt'] 

# SETTINGS FOR MOBIUS FILES
MOB_ANSWER_FILENAME = '_ans.mob' # files that are answers should end with this
MOB_EXAMPLE_FILENAME = '_exp.mob' # files that are examples should end with this
MOB_URL = 'https://design-automation.github.io/mobius-parametric-modeller-dev' # the dev version
#MOB_URL = 'https://mobius.design-automation.net/' # the stable version

# AMAZON S3 SETTINGS
S3_VIDEOS_BUCKET_URL = 'https://mooc-s3cf.s3-ap-southeast-1.amazonaws.com/'
S3_ANSWERS_BUCKET_URL =  'https://sct-mooc-answers.s3.amazonaws.com/'
S3_EXAMPLES_BUCKET_URL =  'https://sct-mooc-examples.s3.amazonaws.com/'
S3_ANSWERS_BUCKET = 'sct-mooc-answers' # the s3 bucket where answers will be uploaded (private)
S3_EXAMPLES_BUCKET = 'sct-mooc-examples' # the s3 bucket where examples will be uploaded (public)

# LANGUAGES
# available languages: ['us', 'uk', 'pt', 'es', 'zh', 'fr', 'de', 'nl']
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

