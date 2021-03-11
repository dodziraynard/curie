const electiveContainer = document.querySelector("#elective_container");
const selector = electiveContainer?.querySelector("select")

const getSubjectsForClass = (element) => {
    const classId = element.value;
    selector.setAttribute("disabled", true)
    if (classId === "" || classId === null) return

    url = "/ajax/class-subjects"
    $.get(url, { class_id: classId }, (data, status) => {
        if (status == "success") {
            selector.innerHTML = ""
            for (subject of data.subjects) {
                const option = document.createElement("option")
                option.setAttribute("value", subject.subject_id)
                option.innerText = subject.name
                selector.append(option)
            }
            selector.removeAttribute("disabled")
        } else {
            alert("Unknown error occured.")
        }
    });
}


document.querySelector("#all_classes")?.addEventListener("change", (e) => {
    if (e.target.checked) {
        $("#promotion-class").slideUp(500, function () {
            $("#promotion-class").slideUp(500);
        });
    } else{
        $("#promotion-class").slideDown(500, function () {
            $("#promotion-class").slideDown(500);
        });
    }
})