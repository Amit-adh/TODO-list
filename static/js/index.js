document.addEventListener("DOMContentLoaded", function(){
    const btn = document.getElementById("add-task");
    btn.addEventListener("mousedown", add)
})

function add(){
    const text_box = document.getElementById("task-text").value;
    const priority = document.getElementById("priority").value;

    if(text_box === "") return;
    
    const ul = document.getElementById(priority);

    const new_li = document.createElement("li");
    new_li.innerHTML = text_box + " " + 
        "<button class='modify-btn'>Modify</button>" + " " +
        "<button class='delete-btn'>Delete</button>";

    const mod_btn = new_li.querySelector(".modify-btn");
    const del_btn = new_li.querySelector(".delete-btn");

    mod_btn.addEventListener("mousedown", modify);
    del_btn.addEventListener("mousedown", remove);
    
    ul.appendChild(new_li);
}

function modify(event){
    button = event.target;
    const li_item = button.parentElement;
    const text = document.getElementById("task-text").value;
    li_item.innerHTML = "<input type='text' class='modify-txt'> <button id = 'submit-btn'>Submit</button>";

    document.querySelector(".modify-txt").value = text;

    const btn = document.getElementById("submit-btn");
    btn.addEventListener("mousedown", submit);
}

function submit(event){
    button = event.target;
    const new_li = button.parentElement;
    text = document.querySelector(".modify-txt").value;
    new_li.innerHTML = text + " " + 
        "<button class='modify-btn'>Modify</button>" + " " +
        "<button class='delete-btn'>Delete</button>";

        const mod_btn = new_li.querySelector(".modify-btn");
        const del_btn = new_li.querySelector(".delete-btn");
    
        mod_btn.addEventListener("mousedown", modify);
        del_btn.addEventListener("mousedown", remove);
}

function remove(event){
    button = event.target;
    const li_item = button.parentElement;
    li_item.remove(button);
}