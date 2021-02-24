const sideBarItems = document.querySelectorAll(".side-bar-item")
const navBarItems = document.querySelectorAll(".nav-item")
sideBarItems.forEach(item => {
    item.addEventListener("click", (e) => {
        item.classList.toggle("active")
    })
})

navBarItems.forEach(item => {
    item.addEventListener("click", (e) => {
        navBarItems.forEach(e => {
            if (e !== item)
                e?.classList.remove("active")
        })

        item.classList.toggle("active")
    })
})

// Mobile sidebar toggler
const toggler = document.querySelector("#toggler")
const sidebar = document.querySelector("#sidebar")
toggler.addEventListener("click", (e) => {
    sidebar.classList.toggle("fold")
    toggler.classList.toggle("open")
    $("html, body").animate({ scrollTop: 0 }, "slow");
})

// Activate current sidebar element
const activeId = sidebar.dataset.active
document.getElementById(activeId).classList.add("active")
