function change_title(){
    let obj = document.getElementById("title")
    let title = (obj.value !== "") ? obj.value : "看音写词"
    document.getElementsByTagName('title')[0].innerText = title
    document.getElementsByTagName("h1")[0].innerText = title
}

function request() {
    let title = document.getElementById('title').value
    $.ajax({
        url: "./pinyin",
        type: "post",
        data: {"content": document.getElementById("words").value},
        async: false,
        success: function (result) {
            document.getElementById("text").innerHTML = result
        }
    })
    print()
}
