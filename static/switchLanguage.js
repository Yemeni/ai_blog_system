function switchLanguage(newLang) {
    let currentUrl = window.location.pathname;
    let urlParts = currentUrl.split("/").filter(part => part);
    let currentLang = urlParts[0];

    // ✅ Ensure `knownLanguages` exists and is valid
    if (typeof knownLanguages === "undefined" || !Array.isArray(knownLanguages)) {
        console.error("Error: knownLanguages is not defined correctly.");
        return;
    }

    // ✅ Fix issue where an incorrect URL like /fr/vi appears
    if (knownLanguages.includes(currentLang)) {
        urlParts[0] = newLang;
    } else {
        urlParts = [newLang, ...urlParts.slice(1)];  // Prevent incorrect duplicate languages
    }

    window.location.pathname = "/" + urlParts.join("/");
}
