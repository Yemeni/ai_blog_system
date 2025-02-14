function switchLanguage(newLang) {
    let currentUrl = window.location.pathname;
    let urlParts = currentUrl.split("/").filter(part => part);
    let currentLang = urlParts[0];

    let knownLanguages = ["en", "ar", "de", "fr"];

    if (knownLanguages.includes(currentLang)) {
        urlParts[0] = newLang;
    } else {
        urlParts.unshift(newLang);
    }

    window.location.pathname = "/" + urlParts.join("/");
}
