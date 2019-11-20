import os
## ImageMagick Binary location
IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'C:\\Program Files\\ImageMagick-7.0.8-Q16\\magick.exe')

## LibreOffice program file location
PATH_TO_LIBRE_OFFICE_PROGRAM = "D:\\mscInstallations\\LibreOffice\\program\\"

## Course Relative Path
COURSE_PATH = "input\\Course\\"

## Video settings
VIDEO_RES = (1080,720)
TITLE_PERIOD = 3 #seconds

## Audio settings
LANGUAGES = ["uk", "zh"] # available: refer to keys of VOICES below
VOICES = dict(
    us = dict(
            lang_code = "en-US", # usable for translate api
            neural = True,
            ids = ["Joanna", "Kendra", "Kimberly", "Salli", "Joey", "Matthew"]
        ),
    uk = dict(
            lang_code = "en-GB",
            neural = True,
            ids = ["Amy", "Emma", "Brian"]
        ),
    pt = dict(
            lang_code = "pt-BR",
            neural = True,
            ids = ["Camila"]
        ),
    es = dict(
            lang_code = "es-US",
            neural = True,
            ids = ["Lupe"]
        ),
    zh = dict(
            lang_code = "cmn-CN",
            neural = False,
            ids = ["Zhiyu"]
        ),
    fr = dict(
            lang_code = "fr-FR",
            neural = False,
            ids = ["Celine", "Léa", "Mathieu"]
        ),
    de = dict(
            lang_code = "de-DE",
            neural = False,
            ids = ["Marlene", "Vicki", "Hans"]
        ),
    nl = dict(
            lang_code = "nl-NL",
            neural = False,
            ids = ["Lotte", "Ruben"]
        )
)