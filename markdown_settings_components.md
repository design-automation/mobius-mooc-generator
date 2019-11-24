
# Settings for Components

Below is a list of the settings that can be specified for each type of component.

## Common Settings For Components

For components, the heading above the settings must starts with `# COMPONENT`.

The settings differ for each componet. However, there are certain common settings. 

One important setting is called `type`, which defines the type of component being defined.

Possible values of 'type' are as follows:
- `type="text"`
- `type="video"`
- `type="problem-submit"`
- `type="problem-checkboxes"`
- `type="problem-choice"` (not supported at this time)
- `type="problem-dropdown"` (not supported at this time)
- `type="problem-numerical"` (not supported at this time)
- `type="problem-text"` (not supported at this time)

At the moment, for problems, only 'problem-submit' and 'problem-checkboxes' are implemented.
- problem-submit: A problem where the learner needs to submit a file that will be uploade to the edx server and graded with an external grader. 
- problem-checkboxes: A problem where the learner needs to answer a checkboxes question (with multiple right answers).  Feedback

Other common setting for all components  are as follows:

_Required_
- `display_name="unit name"`

Optional
- `visible_to_staff_only+"true"`
- `start="2019-08-18T10:00:00+00:00"`

The `display_name` is not displayed to the user in the edx interface.

## Text

Additional text settings are as follows:

NIL

## Video

Additional video settings are as follows:

_Required_  (either one of the two)
- `youtube_id_1_0="3_yD_cEKoCk"`
- `video="my_video.mp4"`

Optional
- `download_video="false"`
- ... and many more

## Problem - Checkboxes

Additional checkboxes  problem settings are as follows:

Optional
- `max_attempts: "2"`
- `weight: "1.0"`
- `showanswer: "finished"`
- `group_access: "{}"`
- `rerandomize: "always"` or `"never"` or ...
- `attempts_before_showanswer_button: "1"`

## Problem - Submit

Additional submit problem settings are as follows:

_Required_
- `answer="answer_model.mob"` (not shown to the learner)

Optional
- `example="example_model.mob"` (shown to the learner)
- `max_attempts="2"` 
- `weight="1.0"`
- `showanswer="finished"`
