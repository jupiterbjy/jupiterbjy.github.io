
function load() {
    // Setup for pio and various styles.

    pio_reference = new Paul_Pio(
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

    let pio_container = document.getElementsByClassName("pio-container").item(0)
    let pio_canvas = document.getElementById("pio")

    // Edit styles here
    pio_container.style.bottom = "-2rem"
    pio_container.style.zIndex = "1"
    pio_canvas.style.height = "20rem"
    pio_alignment = "left"

    // Then apply style
    pio_refresh_style()
}


function model_list_url(){
    // Just a convenience function for ease of add/remove models.

    const cdn_host = "https://cdn.jsdelivr.net/gh/"

    const src_cdn = [
        "guansss/pixi-live2d-display/test/assets/shizuku/shizuku.model.json",
        "guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json",
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
    return Array.from(src_cdn, (s, _) => cdn_host + s)
}


function switch_left_right(){
    // This is not needed at all, just to demonstrate switching left-right on the fly.

    if (pio_alignment === "left"){
        pio_alignment = "right"
    }
    else {
        pio_alignment = "left"
    }

    pio_refresh_style()
}

let pio_reference
window.onload = load