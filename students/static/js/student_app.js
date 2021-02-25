const electiveContainer = document.querySelector("#elective_container");
const selector = electiveContainer?.querySelector("select")

const getSubjectsForClass = (element) => {
    const classId = element.value;
    if (classId === "" || classId === null) return

    selector.setAttribute("disabled", true)

    url = "/ajax/subjects"
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