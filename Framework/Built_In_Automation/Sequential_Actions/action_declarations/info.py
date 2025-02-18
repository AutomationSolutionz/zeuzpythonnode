import regex as re
from . import (
    appium,
    common,
    desktop,
    rest,
    selenium,
    utility,
    windows,
    xml,
    database,
    performance,
    security,
)

modules = (
    appium,
    common,
    desktop,
    rest,
    selenium,
    utility,
    windows,
    xml,
    database,
    performance,
    security,
)

# This will be exported and contains all the actions.
actions = {}

action_id = 1
for mod in modules:
    for dec in mod.declarations:
        actions[action_id] = dec
        action_id += 1

# List of Sub-Field keywords, must be all lowercase, and using single spaces - no underscores
action_support = (
    "action",
    "optional action",
    "loop action",
    "element parameter",
    "child parameter",
    "sibling parameter",
    "parent parameter",
    "following parameter",
    "next parameter",
    "preceding parameter",
    "previous parameter",
    "search element parameter",
    "target parameter",
    "desired element parameter", "desired parent parameter", "desired sibling parameter", "desired child parameter",
    "src element parameter", "src parent parameter", "src sibling parameter", "src child parameter",
    "source element parameter", "source parent parameter", "source sibling parameter", "source child parameter",
    "dst element parameter", "dst parent parameter", "dst sibling parameter", "dst child parameter",
    "destination element parameter", "destination parent parameter", "destination sibling parameter", "destination child parameter",
    "optional parameter",
    "optional label",
    "iframe parameter",
    "frame parameter",
    "method",
    "url",
    "body",
    "header",
    "headers",
    "compare",
    "path",
    "value",
    "result",
    "scroll parameter",
    "table parameter",
    "source parameter",
    "input parameter", "parameter",
    "output parameter",
    "custom action",
    "unique parameter",
    "save parameter",
    "get parameter",
    "loop settings",
    "optional loop settings",
    "optional loop condition",
    "optional loop control",
    "attribute constrain",
    "optional option",
    "graphql",
    "shared capability", "chrome option", "edge option", "chromium option", "firefox option", "safari option",
    "pre sleep", "post sleep", "pre post sleep", "post pre sleep",
    "zoom parameter", "optional zoom parameter", "pan parameter", "optional pan parameter",
    "profile option", "profile options",
    "text classifier offset"
    "fail message",
)

#Old one
# patterns = [
#     r'^sr *(src |source |dst |destination |desired )?(parent|sibling|child|next|following|previous|preceding) (\d+ )*parameter$',
#     r'^sr *(src |source |dst |destination |desired )?element parameter$',
# ]


#New one 
patterns = [
    r'^(sr\s+)?'  # Optional 'sr' prefix followed by one or more spaces
    r'(src |source |dst |destination |desired )?'
    r'(parent|sibling|child|next|following|previous|preceding)'
    r'( \d+)? parameter$',  # Optional numeric index and ends with 'parameter'

    r'^(sr\s+)?'  # Optional 'sr' prefix
    r'(src |source |dst |destination |desired )?'
    r'element parameter$',
]

# List of supported mobile platforms - must be lower case
supported_platforms = ("android", "ios")

def sub_field_match(text:str)->bool:
    if text in action_support:
        return True
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False
'''
parent 1 parameter
'''