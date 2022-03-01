//sidebar toggle

let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".menu-toggle");
console.log(sidebarBtn);
sidebarBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("close");
});




