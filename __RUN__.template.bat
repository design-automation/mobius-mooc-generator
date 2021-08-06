REM Script to execute Edx Generator

set mob_uploader_script="C:/xxx/mob_uploader.py"
set edx_generator_script="C:/xxx/edx_generator.py"
set input="C:/yyy/mooc1-procedural-modelling-v3"
set output="C:/zzz/proc"

python %mob_uploader_script% %input%
python %edx_generator_script% %input% %output%


