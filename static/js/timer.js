var url_ = $("input[name=url]").val();
const minutes = document.querySelector(".minutes")
const sec = document.querySelector(".sec")
let time = Number(sec.innerHTML) + Number(minutes.innerHTML) * 60
let zminna = setInterval(()=>{
        console.log("time = "+ time)
        if (time == 0) {
            window.location.replace(url_);
        }
        // if (time == 1){
        //     clearInterval(zminna);
        // }
        if (sec.innerHTML == "0" || sec.innerHTML == "00"){
            minutes.innerHTML = minutes.innerHTML - 1
            sec.innerHTML = 60
        }
        sec.innerHTML = sec.innerHTML - 1
        if (sec.innerHTML < 10){
            sec.innerHTML = "0" + sec.innerHTML
        }
        time = time - 1     
    }, 1000 )