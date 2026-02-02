// https://stackoverflow.com/questions/7373081

// Why this existed? I don't remember

function load_html() {
    let iframe_source = document.getElementById("brython_html_area")

    iframe_source.src = location.href + "/support.html"

    let iframe_doc = iframe_source.contentDocument || iframe_source.contentWindow.document
    // let main_page = iframe_doc.getElementsByClassName("page-content")
    let text_area = iframe_doc.getElementsByClassName("interactive_brython")

    text_area.scrollTop = text_area.scrollHeight

}

load_html()
