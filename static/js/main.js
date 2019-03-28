const themeItemHeaders = document.querySelectorAll('.theme-item__header')

themeItemHeaders.forEach((item) => {
    item.addEventListener('click' , (evt) => {
        evt.currentTarget.parentNode.classList.toggle('theme-item--opened')
    })
})
