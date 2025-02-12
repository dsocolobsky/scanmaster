function doPing(ip) {
    $('#loading').show();
    $.post("/ping/" + ip, function (data) {
        console.log(data);
        $('#loading').hide();
        location.reload();
    });
}

function doNmap(ip) {
    $('#loading').show();
    $.post("/nmap/" + ip, function (data) {
        console.log(data);
        $('#loading').hide();
        location.reload();
    });
}

function doScreenshot(ip) {
    $('#loading').show();
    $.post("/screenshot/" + ip, function (data) {
        console.log(data);
        $('#loading').hide();
        location.reload();
    });
}

function changeName(ip, newname) {
    $('#loading').show();
    $.post("/host/" + ip + "/change/name", {name: newname}, function (data) {
        console.log(data);
        $('#loading').hide();
        location.reload();
    })
}

function makeNameEditable(ip) {
    console.log("reached " + ip);
    var elem = document.getElementById(ip + '::name');
    var isEditable = elem.contentEditable === 'true';

    if (!isEditable) {
        elem.parentElement.removeAttribute('href');
        elem.contentEditable = 'true';
        document.getElementById(ip + '::name').focus();
    } else {
        elem.contentEditable = 'false';
        var newname = elem.textContent;
        changeName(ip, newname);
    }
}