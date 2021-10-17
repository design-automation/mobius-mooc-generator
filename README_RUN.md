# Running the Möbius MOOC Generator

Important note:

**WARNING: any existing contents in the output folder (i.e. in this case `./out/MOOC1`) will be deleted.**

**WARNING: When you upload the .tar.gz file to Edx, any existing course contents in edx will be deleted.**

Make sure to save backups!

## Dependencies

This Python3 script requires three python modules. These can be installed with `pip` as follows:

* `pip install markdown`
* `pip install lxml`
* `pip install boto3`

Markdown is processes using the python markdown module.
- https://python-markdown.github.io

The following extensions are used:
- https://python-markdown.github.io/extensions/extra/
  - https://python-markdown.github.io/extensions/fenced_code_blocks/
  - https://python-markdown.github.io/extensions/tables/

extensions = ['extra', 'sane_lists']

## Set AWS Credentials for S3 Upload

The `.mob` files need to be uploaded to an S3 bucket. In order for this to work, you need to specify some settings.
* The settings for the s3 bucket are specified in the `__SETTINGS__.py` file in the MOOC root input folder.
* The auth settings for accessing your AWS account are specified in the file `__AWS__.py`, in the `aws_cred` folder.

For the auth settings, got to the folder `aws_cred`, and you will find a file called `__AWS__.template.py`. Rename this file to `__AWS__.py` and add your ID and secret key. 

## Execution

There are two Python scripts:
* `edx_generator.py`: Generates all the MOOC files, including the `.tar.gz` file that can be uploaded to directly to Edx.
* `mob_uploader.py`: Uploads `.mob` files to your AWS s3 bucket.

Execute the generator:
```
python ./edx_generator.py "C:/xxxx/mooc1-procedural-modelling" "C:/Data/xxxx/mooc1"
```

Execute the uploader:
```
python ./mob_uploader.py "C:/xxxx/mooc1-procedural-modelling"
```

The `__SETTINGS__.py` file in the MOOC root input folder specifies a set of global settings that you can set for your context. 

**WARNING: any existing contents in the output folder (i.e. in this case `./out/MOOC1`) will be deleted.**

## Upload the .tar.gz File

After running the edx generator (assuming no errors), a `tar.gz` file will be generated. This file can be uploaded to your MOOC.

**WARNING: When you upload the .tar.gz file to Edx, any existing course contents in edx will be deleted.**
