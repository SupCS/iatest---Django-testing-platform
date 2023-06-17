const menu = document.querySelector(".menu")
const btn = document.querySelector(".show-menu")
const lstcour = document.querySelector(".list-corses")
btn.addEventListener("click", ()=>{
    if (menu.classList.contains("hidden")){
        menu.classList.add("animate__fadeInDown")
        menu.classList.remove("animate__fadeOutUp")
        menu.classList.remove("hidden")
    }
    else{
        menu.classList.add("animate__fadeOutUp")
        menu.classList.remove("animate__fadeInDown")
        setTimeout( ()=>{
            menu.classList.add("hidden")    
        }, 600)
    }
        
})