// https://stackoverflow.com/questions/7373081


function load_html() {
    let iframe_source = document.getElementById("brython_html_area")

    iframe_source.src = location.href + "/support.html"

    let iframe_doc = iframe_source.contentDocument || iframe_source.contentWindow.document
    let text_area_div = iframe_doc.getElementById("text_area_wrapper")
    let text_area = iframe_doc.getElementsByClassName("interactive_brython")

    // text_area_div.style = iframe_source.style
    text_area.scrollTop = text_area.scrollHeight

}

load_html()
