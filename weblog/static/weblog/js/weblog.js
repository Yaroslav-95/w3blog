function toggleNode(caller){
    state = caller.getAttribute('node-state');
    target = document.getElementById(caller.getAttribute('node-target'));
    if(state=='closed'){
        caller.innerHTML =  '—';
        caller.setAttribute('node-state', 'open');
    }
    else{
        caller.innerHTML =  '+';
        caller.setAttribute('node-state', 'closed');
    }
    target.classList.toggle('show');
}

function loadBlogPosts(url, page = 2){
    var req = new XMLHttpRequest();
    function insert(){
        if (this.status == 200 && this.readyState == 4){
            var blog_content = document.querySelector(".blog-content");
            try{
                var nxtpage_button = document.querySelector(".nxtpage-button");
                nxtpage_button.insertAdjacentHTML("beforebegin", this.responseText);
            }
            catch(er){
                console.log("error "+er);
                blog_content.insertAdjacentHTML("beforeend", this.responseText);
            }
            console.log(this.responseText);
        }
    }
    req.addEventListener("readystatechange", insert);
    req.open("GET", url, true);
    req.send();
}
