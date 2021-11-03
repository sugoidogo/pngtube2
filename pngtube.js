async function getDevices() {
    return JSON.parse(await (await fetch(document.URL + 'audio/')).text())
}

async function setAudioListener(listener, device = null) {
    url = document.URL + 'audio'
    if (device) {
        url += '/' + encodeURIComponent(device)
    }
    eventsource = new EventSource(url);
    eventsource.onMessage = function (event) {
        listener(event.data)
    }
    eventsource.onError = function () {
        eventsource.close()
    }
    return eventsource
}