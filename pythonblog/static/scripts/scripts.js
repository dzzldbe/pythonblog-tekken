function fill_field(smth){document.getElementById('form_1').value += smth}
function clear_field(smth){document.getElementById('form_1').value = smth}
const button = document.querySelector('.left-key');

function left_key_click(event) {
if (event.key === 'ArrowLeft') {
   button.click();
}
}
document.addEventListener('keyup', left_key_click);


const button1 = document.querySelector('.right-key');
function right_key_click(event) {
   if (event.key === 'ArrowRight') {
      button1.click();
   }
}
document.addEventListener('keyup', right_key_click);

const list_pass=[]

function send_list() {
   input1=document.getElementById('generated_list');
   input1.value=list_pass
   console.log(input1.value)
}

function delete_last() {
   const target_div=document.getElementById('preview_container')
   const last_img= target_div.querySelector('img:last-child')
   last_img.remove();
   list_pass.pop()
}
function delete_all() {
   const target_div=document.getElementById('preview_container')
   target_div.replaceChildren();
   list_pass.length=0
}
function set_char(moves) {
   const target_div=document.getElementById("char_buttons");
   
   const move_list= moves.split(',')
   move_list.forEach(element => {
      const button=document.createElement('button');
      button.className="btn btn-tekken btn-text"
      button.textContent=element.trim();
      const elm="/static/assets/" + element.trim() + ".png"     
      button.setAttribute('onclick',`add_image("${elm}")`);
      button.setAttribute("height","55")
      button.setAttribute("width","55")
      target_div.appendChild(button)
      console.log(element.trim())
   });
   // console.log(Object.prototype.toString.call(move_list) )
}
   function add_image(path){
// let generated_list=[]
   const preview_container=document.getElementById('preview_container');
   const img=document.createElement('img');
   img.src=path;
   img.width=40;
   img.height=40;
   preview_container.appendChild(img);
// generated_list.push(path)
// input1=document.getElementById('generated_list');
   list_pass.push(path)
// console.log(list_pass)
// input1.value+=path+ "$$$"
}
function handleClick(move) {
   alert(`clik: ${move}`);
}