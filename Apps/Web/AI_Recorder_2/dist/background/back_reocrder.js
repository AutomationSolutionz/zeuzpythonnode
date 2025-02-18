var metaData = {};

fetch("./data.json")
    .then(Response => Response.json())
    .then(data => {
        metaData = data;
        console.log('metaData', metaData)
    });

const browserAppData = chrome || browser;

function generateId({stack, command, url, xpath}){
    if (stack){
        for (const item of Object.keys(Stack)) {
            if(Stack[item] && Stack[item][0].command === command && Stack[item][0].url === url && Stack[item][0].xpath === xpath)
                return item
        }
    }
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let id = '';
    for (let i = 0; i < 8; i++) {
      id += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return id;
}

var notificationCount = 0;
function notification(command) {
    let tempCount = String(notificationCount);
    notificationCount++;

    browserAppData.notifications.create(tempCount, {
        "type": "basic",
        "iconUrl": "../small_logo.png",
        "title": "Action Recorded",
        "message": String(command)
    });

    setTimeout(function() {
        browserAppData.notifications.clear(tempCount);
    }, 15000);
}

var action_name_convert = {
    select: "click",
    type: "text",
    open: "go to link",
    Go_to_link: "go to link",
    doubleClick: "double click",
    Validate_Text: "validate full text",
    Validate_Text_By_AI: "validate full text by ai",
    Save_Text: "save attribute",
    Wait_For_Element_To_Appear: "wait",
    Wait_For_Element_To_Disappear: "wait disable",
}

async function fetchAIData(id, command, value, url, document){
    if (command === 'keystroke keys'){
        let keystroke = {
            id: id,
            action: 'keystroke keys',
            element: "",
            is_disable: false,
            name: `keystroke: ${value}`,
            value: url,
            main: [['keystroke keys', 'selenium action', value]],
            xpath: "",
        };
        browserAppData.runtime.sendMessage({
            action: 'record-finish',
            data: keystroke,
        })
        return;
    }
    if (command === 'go to link'){
        let go_to_link = {
            id: id,
            action: 'go to link',
            element: "",
            is_disable: false,
            name: `Open ${(url.length>25) ? url.slice(0,20) + '...' : url}`,
            value: url,
            main: [['go to link', 'selenium action', url]],
            xpath: "",
        };
        browserAppData.runtime.sendMessage({
            action: 'record-finish',
            data: go_to_link,
        })
        return;
    }
    if (['select', 'click'].includes(command)) value = ""
    let validate_full_text_by_ai = false
    if (command === 'validate full text by ai'){
        command = 'validate full text';
        validate_full_text_by_ai = true;
    }

    //The following code removes non-unicode characters (except \x09 and \x0A that are \t and \n), that causes issue in lxml tree
    // Optionally remove control characters (0-31 and 127 in ASCII) except 9,10 \t and \n
    document = document.replace(/[\x00-\x08\x0B-\x1F\x7F]/g, ''); 
    // console.log('document', document)

    var dataj = {
        "page_src": document,
        "action_name": command,
        "action_type": "selenium",
        "action_value": value,
        "source": "web",
    };
    var data = JSON.stringify(dataj);

    const url_ = `${metaData.url}/ai_record_single_action/`
    const input = {
        method: "POST",
        headers: {
            // "Content-Type": "application/json",
            "X-Api-Key": metaData.apiKey,
        },
        body: data,
    }
    var r = await fetch(url_, input)
    var resp = await r.json();
    if (resp.info !== 'success'){
        console.error('resp', resp.info)
        return
    }
    let response = resp.ai_choices;

    if (validate_full_text_by_ai){
        let text_classifier = await browserAppData.runtime.sendMessage({
            action: 'content_classify',
            text: value,
        });

        console.log("text_classifier", text_classifier);
        let label = text_classifier[0].label;
        label = label.charAt(0).toUpperCase() + label.slice(1).toLowerCase();
        let offset = Number((text_classifier[0].score * 0.9).toFixed(2));
        // offset = Math.max(0.8, offset);
        response[0].data_set = response[0].data_set.slice(0,-1)
        .concat([[label, "text classifier offset", offset]])
        .concat(response[0].data_set.slice(-1))
        value = '';
    }
    else if (command === 'save attribute'){
        response[0].data_set = response[0].data_set.slice(0,-1)
        .concat([
            ["text", "save parameter", "var_name"],
            ["save attribute", "selenium action", "save attribute"],
        ])
        value = '';
    }
    else if (['wait', 'wait disable'].includes(command)){
        value = 10;
    }
    response[0].short.value = value;
    if (command === 'text') response[0].data_set[response[0].data_set.length-1][response[0].data_set[0].length-1] = value;
    else if (value) response[0].data_set[response[0].data_set.length-1][response[0].data_set[0].length-1] = value;
    let single_action = {
        id: id,
        action: response[0].short.action,
        element: response[0].short.element,
        is_disable: false,
        name: response[0].name,
        value: response[0].short.value,
        main: response[0].data_set,
        xpath: response[0].xpath,
    }
    browserAppData.runtime.sendMessage({
        action: 'record-finish',
        data: single_action,
    })
}

var Stack = {}
async function record_action(id, command, xpath, value, url, tagName, document, stack){
    let stacked_id = ''
    if (stack){
        if (!(id in Stack)){
            Stack[id] = [{
                id: id,
                command: command,
                xpath: xpath,
                value: value,
                url: url,
                tagName: tagName,
                document: document
            }]
            browserAppData.runtime.sendMessage({
                action: 'record-start',
                data: {
                    id:id
                },
            })
        }
        else if(
            Stack[id][0].command == command &&
            Stack[id][0].xpath == xpath &&
            Stack[id][0].url == url
        ){
            Stack[id].push({
                id: id,
                command: command,
                xpath: xpath,
                value: value,
                url: url,
                tagName: tagName,
                document: document
            })
        }
        stacked_id = id
    }
    for (const item of Object.keys(Stack)) {
        if (item === stacked_id) 
            continue
        let _id = Stack[item][Stack[item].length-1].id
        let _command = Stack[item][Stack[item].length-1].command
        let _value = Stack[item][Stack[item].length-1].value
        let _url = Stack[item][Stack[item].length-1].url
        let _document = Stack[item][Stack[item].length-1].document
        if (Object.keys(action_name_convert).includes(_command)) 
            _command = action_name_convert[_command];
        notification(_command);
        fetchAIData(_id, _command, _value, _url, _document);
        delete Stack[item]        
    }

    if(!stack){
        browserAppData.runtime.sendMessage({
            action: 'record-start',
            data: {
                id: id,
                action: action_name_convert[command]
            },
        })
        if (Object.keys(action_name_convert).includes(command)) command = action_name_convert[command];
        notification(command);
        fetchAIData(id, command, value, url, document); 
    } 
}

browserAppData.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.action == 'start_recording') {
            Stack = {}
            notificationCount = 0;
        }
        else if (request.action == 'record_action') {
            let id = generateId({
                stack: request.stack,
                command: request.command,
                url: request.url,
                xpath: request.xpath,
            })
            console.log('action_name =',request.command)
            record_action(
                id,
                request.command,
                request.xpath,
                request.value,
                request.url,
                request.tagName,
                request.document,
                request.stack,
            );
        }
    }
);
