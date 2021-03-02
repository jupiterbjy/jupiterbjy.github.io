
function mainScript() {
    pio_preconfigure()
    let pio = load()
}

function load() {
    return new Paul_Pio(
        {
            "mode": "fixed",
            "hidden": false,
            "content": {
                "welcome": ["Hi!"],
                "custom": [
                    {"selector": ".comment-form", "text": "Content Tooltip"},
                    {"selector": ".home-social a:last-child", "text": "Blog Tooltip"},
                    {"selector": ".post-item a", "type": "read"},
                    {"selector": ".post-content a, .page-content a", "type": "link"}
                ]
            },
            "model": model_list_url(),
            "tips": true
        }
    )
}

function model_list_url(){
    let proxy_host = "https://cdn.jsdelivr.net/gh/imuncle/live2d/model/"
    let source_ = [
        "22/model.default.json",
        "22/model.2016.xmas.1.json",
        "22/model.2016.xmas.2.json",
        "22/model.2017.school.json",
        "22/model.2017.summer.normal.1.json",
        "22/model.2017.summer.normal.2.json",
        "22/model.2017.summer.super.1.json",
        "22/model.2017.summer.super.2.json",
        "22/model.2017.valley.json",
        "22/model.2018.lover.json"
    ]

    return Array.from(source_, (s, k) => proxy_host + s)
}

function pio_preconfigure(){
    // referencing https://github.com/wu-kan/wu-kan.github.io/
    // Originally was following pio document and had it in HTML, but this looks cleaner

    // Generating container
    let pio_container = document.createElement("div")
    pio_container.classList.add("pio-container")
    pio_container.classList.add("left")
    pio_container.style.bottom = "-2rem"
    pio_container.style.zIndex = "1"

    // Generate action
    let pio_action = document.createElement("div")
    pio_action.classList.add("pio-action")

    // Generate canvas
    let pio_canvas = document.createElement("canvas")
    pio_canvas.id = "pio"
    pio_canvas.style.width = "14rem"
    pio_canvas.width = "640"
    pio_canvas.height = "800"

    // insert elements
    document.body.insertAdjacentElement("beforeend", pio_container)
    pio_container.insertAdjacentElement("beforeend", pio_action)
    pio_container.insertAdjacentElement("beforeend", pio_canvas)

}


window.onload = mainScript
