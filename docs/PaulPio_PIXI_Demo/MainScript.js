
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
    const proxy_host = "https://cdn.jsdelivr.net/gh/"

    const source_0 = [
        "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/shizuku/shizuku.model.json",
        "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json",
    ]

    const source_1 = [
        "imuncle/live2d/live2d_3/model/Azue%20Lane(JP)/xixuegui_4/xixuegui_4.model3.json",
        "imuncle/live2d/model/22/model.default.json",
        "imuncle/live2d/model/22/model.2016.xmas.1.json",
        "imuncle/live2d/model/22/model.2016.xmas.2.json",
        "imuncle/live2d/model/22/model.2017.school.json",
        "imuncle/live2d/model/22/model.2017.summer.normal.1.json",
        "imuncle/live2d/model/22/model.2017.summer.normal.2.json",
        "imuncle/live2d/model/22/model.2017.summer.super.1.json",
        "imuncle/live2d/model/22/model.2017.summer.super.2.json",
        "imuncle/live2d/model/22/model.2017.valley.json",
        "imuncle/live2d/model/22/model.2018.lover.json"

    ]
    const joined = Array.from(source_1, (s, _) => proxy_host + s)

    return source_0.concat(joined)
}


function pio_preconfigure(){
    // referencing https://github.com/wu-kan/wu-kan.github.io/
    // Originally was following pio document and had it in HTML,
    // but using this way for management factors and to handle PIXI resizing elements.

    // Generating container
    let pio_container = document.createElement("div")
    pio_container.classList.add("pio-container")
    pio_container.classList.add("left")
    pio_container.id = "pio-container-id"

    // Generate action
    let pio_action = document.createElement("div")
    pio_action.classList.add("pio-action")

    // Generate canvas
    let pio_canvas = document.createElement("canvas")
    pio_canvas.id = "pio"

    // insert elements
    document.body.insertAdjacentElement("beforeend", pio_container)
    pio_container.insertAdjacentElement("beforeend", pio_action)
    pio_container.insertAdjacentElement("beforeend", pio_canvas)
}


function pio_reconfigure_style(){
    // Since PIXI somehow resizes canvas and I have no control over that,
    // styling should happen afterward.

    let pio_container = document.getElementById("pio-container-id")
    let pio_canvas = document.getElementById("pio")

    pio_container.style.bottom = "-2rem"
    pio_container.style.zIndex = "1"
    pio_canvas.style.width = "14rem"
    pio_canvas.width = 640
    pio_canvas.height = 800
}


function loadlive2d(canvas, json_object_or_url) {
    // Replaces original l2d method 'loadlive2d' for Pio.

    try {
        app.stage.removeChildAt(0)
    } catch (error) {

    }

    let model = PIXI.live2d.Live2DModel.fromSync(json_object_or_url)

    model.once("load", () => {
        app.stage.addChild(model)

        const canvas_ = document.getElementById("pio")

        const scaleX = canvas_.width / model.width;
        const scaleY = canvas_.height / model.height;

        // fit the window
        model.scale.set(Math.min(scaleX, scaleY));

        // align to corner
        model.x = (model.width - canvas_.width) / 2
        model.y = (canvas_.height - model.height) / 2

        console.log(`[LOG] model h/w dimension: ${model.height} ${model.width}`)
        console.log(`[LOG] model x/y location: ${model.x} ${model.y}`)

        model.on('hit', hitAreas => {
            if (hitAreas.includes('body')) {
                console.log(`[LOG] Touch on body (SDK2)`)
                model.motion('tap_body')

            } else if (hitAreas.includes("Body")) {
                console.log(`[LOG] Touch on body (SDK3)`)
                model.motion('Tap')

            } else if (hitAreas.includes("head") || hitAreas.includes("Head")){
                console.log(`[LOG] Touch on head`)
                model.expression()
            }
        })
    })
}


function init_app() {

    app = new PIXI.Application({
        view: document.getElementById("pio"),
        transparent: true,
        autoStart: true,
    })
}

function app_reconfigure_style(){
    // need to separate this from PIXI initialization or first loaded Live2D size breaks on resize.
    app.resizeTo = document.getElementById("pio")
}


function mainScript() {
    pio_preconfigure()
    init_app()

    pio_reconfigure_style()
    app_reconfigure_style()

    let pio = load()
}

let app

window.onload = mainScript