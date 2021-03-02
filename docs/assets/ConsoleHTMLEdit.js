
function load_html() {
    let iframe_source = document.getElementById("brython_html_area")

    iframe_source.src = location.href + "/support.html"

    let iframe_doc = iframe_source.contentDocument || iframe_source.contentWindow.document
    let text_area = iframe_doc.getElementById("text_area_wrapper")

    text_area.style = iframe_source.style
}

load_html()
