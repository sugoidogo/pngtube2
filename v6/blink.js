(function blink(){
    const style=getComputedStyle(document.body)
    const min=+style.getPropertyValue('--blink-min')
    const max=+style.getPropertyValue('--blink-max')
    const time=+style.getPropertyValue('--blink-time')
    console.debug(min,max,time)
    for(const element of document.querySelectorAll('*')){
        element.classList.add('blink')
    }
    setTimeout(()=>{
        for(const element of document.querySelectorAll('*')){
            element.classList.remove('blink')
        }
    },time*1000)
    setTimeout(blink, (Math.random() * (max - min) + min)*1000)
})()