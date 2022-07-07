// Activate datatable
document.querySelectorAll(".data-table")?.forEach(table => {
    try {
        $(table).DataTable({
            "dom": '<"wrapper"ftipl>', // Reference: https://datatables.net/reference/option/dom
        })
    } catch (error) {
        console.log(error)
    }
})
