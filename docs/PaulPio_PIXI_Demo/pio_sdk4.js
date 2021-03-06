/* ----

# Pio Plugin
# By: Dreamer-Paul
# Last Update: 2021.3.6

一个支持更换 Live2D 模型的 Typecho 插件。

本代码为奇趣保罗原创，并遵守 GPL 2.0 开源协议。欢迎访问我的博客：https://paugram.com

jupiterbjy: I couldn't fetch pio frm cdn.jsdelivr.net as it was serving way old version of this.
jupiterbjy: code itself is not modified and all right reserved to original author

---- */


function loadlive2d(canvas, json_object_or_url) {
    // Replaces original l2d method 'loadlive2d' for Pio.

    console.log("[Pio] Loading new model!")

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

        model.scale.set(Math.min(scaleX, scaleY));

        // check alignment, and align model to corner
        if (document.getElementsByClassName("pio-container").item(0).className.includes("left")){
            model.x = 0
        } else {
            model.x = canvas_.width - model.width
        }
        model.y = (canvas_.height - model.height) / 2


        // Hit callback definition
        model.on('hit', hitAreas => {
            if (hitAreas.includes('body')) {
                console.log(`[Pio] Touch on body (SDK2)`)
                model.motion('tap_body')

            } else if (hitAreas.includes("Body")) {
                console.log(`[Pio] Touch on body (SDK3/4)`)
                model.motion('Tap')

            } else if (hitAreas.includes("head") || hitAreas.includes("Head")){
                console.log(`[Pio] Touch on head`)
                model.expression()
            }
        })
        console.log(`[Pio] New model h/w dimension: ${model.height} ${model.width}`)
        console.log(`[Pio] New model x/y offset: ${model.x} ${model.y}`)
    })
}


function pio_initialize_container(){
    // referencing github.com/wu-kan/wu-kan.github.io/

    // Generating container
    let pio_container = document.createElement("div")
    pio_container.classList.add("pio-container")

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

    // default parameter
    // Pio will be placed at left side while menus are right side without explicit "right" or "left".
    pio_container.classList.add("right")
}


function pio_refresh_style(){
    // Had to separate this from PIXI initialization
    // or first loaded Live2D's size will break on resizing.
    // Always make sure to call this after canvas style changes!

    app.resizeTo = document.getElementById("pio")
}


function _pio_initialize_pixi_app() {

    app = new PIXI.Application({
        view: document.getElementById("pio"),
        transparent: true,
        autoStart: true,
    })
}


function _pio_initialize() {
    pio_initialize_container()
    _pio_initialize_pixi_app()

    pio_refresh_style()
}

let app
_pio_initialize()