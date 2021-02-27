
function main_script() {
    let pio = load()
}

function load() {
    return new Paul_Pio(
        {
            "mode": "fixed",
            "hidden": true,
            "content": {
                "welcome": ["Hi!"],
                "custom": [
                    {"selector": ".comment-form", "text": "欢迎参与本文评论，别发小广告噢~"},
                    {"selector": ".home-social a:last-child", "text": "在这里可以了解博主的日常噢~"},
                    {"selector": ".post-item a", "type": "read"},
                    {"selector": ".post-content a, .page-content a", "type": "link"}
                ]
            },
            "night": "single.night()",
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


window.onload = main_script
