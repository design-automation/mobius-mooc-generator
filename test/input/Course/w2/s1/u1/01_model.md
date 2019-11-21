type: html
display_name: A Mobius Model

# A mobius Model

You can insert a mobius iframe by inserting a link that looks something like this:

```
[mobius=publish, defaultViewer=0, showViewer=1, node=2](my_model_exp.mob)
```

Mobius can run in different modes. The `publish` mode is a special type of mode as it hides the usual interafces for editing the model. In this mode, the only thing you can do is change the parameters and click play. Instead of the usual dashboard, you get a little tab on the left side of the viewer, which slides open the dashbaord settings. 

`mobius` selects the modes.
Values can be as folows: 

* `mobius = gallery` - normal mode, with the gallery tab active
* `mobius = dashboard` - normal mode, with the dashboard tab active
* `mobius = flowchart` - normal mode, with the flowchart tab active
* `mobius = editor` - normal mode, with the editor tab active
* `mobius = publish` - special mode, all other tabs are hidden

`defaultViewer` selects the viewer that will be open by default.
Values can be as folows: 

* `defaultViewer = 0` for console viewer
* `defaultViewer = 1` for CAD viewer
* `defaultViewer = 2` for geospatial viewer

`showViewer` only has an impact when `mobius=publish`. It selects which viewers are shown and which are hidden when mobius is in the bublish mode. 
Values can be as follows: 

* `showViewer = 0` for only the console viewer
* `showViewer = 1` for the console and the CAD viewer
* `showViewer = 2` for the console and the geospatial viewer
* `showViewer = 3` for all viewers

The node indicates the node in your mobius model. 

## Examples

Here is a mobius model embedded as `[mobius=publish, defaultViewer=0]`

[mobius = publish, defaultViewer = 0](model_exp.mob)


Here is a mobius model embedded as `[mobius=publish, showViewer=1]`

[mobius = publish, showViewer = 1](model_exp.mob)


Here is a mobius model embedded as `[mobius=publish, showViewer=2]`

[mobius=publish, showViewer = 2](model_exp.mob)


Here is a mobius model embedded as `[mobius=dashboard, defaultViewer=1]`

[mobius = dashboard, defaultViewer = 1](model_exp.mob)


Here is a mobius model embedded as `[mobius=editor, defaultViewer=2]`

[mobius = editor, defaultViewer = 2](model_exp.mob)
