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

CODE_INLINE_CSS = ';'.join([
    #'font-family:Terminus,Consolas,Courier,Terminal,monospace'
    'font-size: 14px',
    'font-weight: 600',
    'font-family:monospace',
    'margin: 0 2px',
    'padding: 0px 5px',
    'border: 1px solid #eaeaea',
    'background-color: #f9f9f9'
    ])

CODE_BOX_CSS = ';'.join([
    'display: block',
    'clear: both',
    'margin-bottom: 10px',
    'border: 1px solid #000000',
    'border-radius: 0px',
    'padding: 10px',
    'width: 600px',
    'background-color: #fafafa'
    ])

CODE_LINE_CSS = ';'.join([
    'font-size: 14px',
    'font-weight: 600',
    'font-family:monospace',
    'margin: 2px',
    'padding: 5px',
    'border-left: 1px solid #999999',
    'border-bottom: 1px solid #999999',
    'border-top: 0px',
    'border-right: 0px',
    'border-radius: 0px'
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
    'border-width:4px',
    'border-color:#065683'
    ])


#--------------------------------------------------------------------------------------------------
