//sidebar toggle

let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".menu-toggle");
console.log(sidebarBtn);
sidebarBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("close");
});

//menu toggle

let iconLink=document.querySelectorAll(".icon-link");

iconLink.forEach(item=>item.onclick=()=>{
   item.nextElementSibling.classList.toggle('active');
   item.classList.toggle('active');
     
   item.lastElementChild.classList.toggle('rotate');
   
})



