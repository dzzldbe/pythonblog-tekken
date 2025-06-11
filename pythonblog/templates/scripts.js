


function add_image(path){
     // let generated_list=[]
     const preview_container=document.getElementById('preview_container');
     const img=document.createElement('img');
     img.src=path;
     img.width=40;
     img.height=40;
     preview_container.appendChild(img);
     // generated_list.push(path)
     input1=document.getElementById('generated_list');
     input1.value+=path+ "$$$"
}



document.getElementById('btn-tekken').onclick = add_image("") 
{

}
// onclick="add_image('{{ url_for("static", filename="assets/next.png")}}')"

<div class="col ">
     <a class="btn btn-tekken right-key" 
               data-bs-toggle="tooltip" 
               data-bs-title="You can use Arrow Right Key" 
               onclick="add_image('{{ url_for("static", filename="assets/next.png")}}')">
          <img src="{{ url_for('static', filename='assets/next.png')}}" alt="" height="50" width="50">
     </a>
</div>