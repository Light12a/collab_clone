let dropdownbtn = document.querySelectorAll('.dropdown-btn');

dropdownbtn.forEach(item =>item.onclick = ()=> {
    //close all sub menu
    dropdownbtn.forEach((i)=>{
        if(i != item){
            i.classList.remove('active');
            i.nextElementSibling.classList.remove('active');
            i.lastElementChild.classList.remove('rotate');
        }
    });
    //active this submenu
    item.classList.toggle('active');
    item.nextElementSibling.classList.toggle('active');
    item.lastElementChild.classList.toggle('rotate');
    
})