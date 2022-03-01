//sidebar toggle
var toggle = false;

let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".menu-toggle");

sidebarBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("expand");

  if (toggle === true) {
    document.getElementById('img-toggle').src  = './images/bar.svg';
  } else {
    document.getElementById('img-toggle').src = './images/times.svg';
  }
  toggle = !toggle; 
});

//close sidebar when click outside 
// window.onclick = function(event) {
//   if (!event.target.matches('.menu-toggle') && !event.target.matches('#img-toggle') && !event.target.matches('.nav-item')) {
//       if (sidebar.classList.contains('expand')) {
//         sidebar.classList.remove('expand');
//       }
//   }
// }

//menu toggle

let iconLink=document.querySelectorAll(".icon-link");

iconLink.forEach(item=>item.onclick=()=>{
   item.nextElementSibling.classList.toggle('active');
   item.classList.toggle('active');
     
    item.lastElementChild.classList.toggle('rotate');
   
})



