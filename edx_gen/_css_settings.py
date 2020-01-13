#--------------------------------------------------------------------------------------------------
# Settings for headings
H3_CSS = ';'.join([
    'font-size: 22px',
    'font-weight: 400',
    'font-style: normal',
    'color: #474747'
    ])

H4_CSS = ';'.join([
    'font-size: 20px',
    'font-weight: 400',
    'font-style: italic',
    'color: #474747'
    ])

H5_CSS = ';'.join([
    'font-size: 18px',
    'font-weight: 400',
    'text-decoration: underline',
    'color: #474747'
    ])

#--------------------------------------------------------------------------------------------------
# Settings for figures

FIGURE_CSS = ';'.join([
    'margin-top:20px',
    'margin-bottom:20px'
    ])

FIGCAPTION_CSS = ';'.join([
    'width:400px',
    # 'display:block',
    # 'margin-left:auto',
    # 'margin-right:auto',
    'margin-top:8px',
    'text-align:left',
    'font-style:italic'
    ])

IMAGE_MODAL_CSS = ';'.join([
    'width:400px',
    # 'display:block',
    # 'margin-left:auto',
    # 'margin-right:auto',
    'border-style:solid',
    'border-width:1px'
    ])

IMAGE_CSS = ';'.join([
    # 'display:block',
    # 'margin-left:auto',
    # 'margin-right:auto',
    'border-style:solid',
    'border-width:1px'
    ])

PRE_CSS = ';'.join([
    'white-space: pre-line',
    'background:#F8F8F8',
    'border-style:solid',
    'border-width:1px',
    'padding:10px;'
    ])

CODE_CSS = ';'.join([
    'font-weight: 600',
    'font-family:monospace'
    #'font-family:Terminus,Consolas,Courier,Terminal,monospace'
    ])
#--------------------------------------------------------------------------------------------------
# Settings for the language buttons
# These are the buttons that appear under each video

LANG_BUTTON_CSS = ';'.join([
    'padding:2px',
    'margin:1px',
    'border-style:solid',
    'border-width:1px',
    'display:inline',
    'cursor:pointer'
    ])

SELECT_LANG_SCRIPT = '''
function myFunction(lang) {
  document.getElementById('chinese').style="display:none";
  document.getElementById('french').style="display:none";
  if (lang !== 'none') {
    document.getElementById(lang).style="display:block";
  }
}
'''
#--------------------------------------------------------------------------------------------------
# Settings for Mobius Iframes
# These are the embedded Mobius models

MOB_IFRAME_WIDTH = '100%'
MOB_IFRAME_HEIGHT ='600px'

MOB_MINI_IFRAME_WIDTH = '80%'
MOB_MINI_IFRAME_HEIGHT ='400px'

MOB_IFRAME_STYLE = ';'.join([
    # 'display:block',
    # 'margin-left:auto',
    # 'margin-right:auto',
    'border-style:solid',
    'border-width:5px',
    'border-color:grey'
    ])


#--------------------------------------------------------------------------------------------------
