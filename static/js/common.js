function confirmDelete(id, url, csrftoken) {
    if (confirm("确定要删除吗？")) {
        fetch("/" + url + "/" + id + "/delete/", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.state) {
                    alert("删除成功!");
                    window.location.reload()
                } else {
                    alert("删除失败!")
                }
            })
    }
}

function Add(url, csrftoken) {
    clearSpanContent()
    const form = document.getElementById("form");
    const data = new FormData(form);
    fetch('/' + url + '/add/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,  // 在请求头中添加 CSRF 令牌
        },
        body: data
    })
        .then(response => response.json())
        .then(data => {
                if (data.state) {
                    alert("添加成功!");
                    window.location.reload();
                } else {
                    for (const [field, messages] of Object.entries(data.error)) {

                        const fieldElement = document.getElementById(`id_${field}`);
                        const errorSpan = fieldElement.nextElementSibling;
                        errorSpan.innerHTML = '';
                        errorSpan.innerHTML = messages;
                    }
                }
            }
        )
}

function clearSpanContent() {
    const spans = document.querySelectorAll('#edit_input span');
    const spans_1 = document.querySelectorAll('#form span');
    spans.forEach(span => {
        span.textContent = '';
    });
    spans_1.forEach(spans_1 => {
        spans_1.textContent = "";
    })
}

{

    function edit_data(id, url, csrftoken) {
        localStorage.setItem("editID", id);
        fetch("/" + url + "/" + id + "/edit/", {
            method: "GET",
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
            .then(response => response.json())
            .then(data => {
                for (const name in data) {
                    const tag = `id_${name}`;
                    const elements = document.querySelectorAll(`#${tag}`);
                    const secondElement = elements[1];
                    secondElement.placeholder = data[name];
                    secondElement.value = data[name];
                }
            })
    }

    function update(url, csrftoken) {
        id = localStorage.getItem("editID");
        const tar = document.getElementById("edit_input");
        const data = new FormData(tar);
        fetch("/" + url + "/" + id + "/edit/", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken,  // 在请求头中添加 CSRF 令牌
            },
            body: data
        })
            .then(response => response.json())
            .then(data => {
                if (data.state) {
                    alert("修改成功!");
                    localStorage.removeItem("editID");
                    window.location.reload();
                } else {
                    for (const [field, messages] of Object.entries(data.error)) {
                        const tag = `id_${field}`;
                        const elements = document.querySelectorAll(`#${tag}`);
                        const secondElement = elements[1];
                        const errorSpan = secondElement.nextElementSibling;
                        errorSpan.innerHTML = '';
                        errorSpan.innerHTML = messages;
                    }
                }
            })
    }
}
