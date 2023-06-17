const btn = document.querySelector(".delete-course")
const submition = document.querySelector(".submission-deleting")
const no = document.querySelector(".NO")
btn.addEventListener("click", ()=>{
    submition.classList.remove("hidden")
    no.addEventListener("click", ()=>{
        submition.classList.add("hidden")
    })
}) 