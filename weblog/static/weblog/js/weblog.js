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

function floatSidebar(){
    if (screen.width > 760){
        var sidebar = document.querySelector(".weblog-sidebar.floating-sidebar");
        var sidebar_filler = document.querySelector(".sidebar-filler");
        var blog_content = document.querySelector(".blog-content");
        var offset = document.querySelector("nav").offsetHeight +
            document.querySelector(".breadcrumb").offsetHeight;
        if((document.body.scrollTop > offset || document.documentElement.scrollTop > offset)){
            sidebar.classList.add("float");
            sidebar_filler.classList.remove("hidden");
            sidebar.style.left = blog_content.offsetLeft + blog_content.offsetWidth + "px";
        }
        else{
            sidebar.classList.remove("float");
            sidebar_filler.classList.add("hidden");
        }
    }
}

function loadBlogPosts(url, page = 2, isinfinite = false){
    var req = new XMLHttpRequest();
    function insert(response, isinfinite){
        if (response.status == 200 && response.readyState == 4){
            var loader_container = document.querySelector(".loader-container");
            if (!isinfinite){
                var nxtpage_container = document.querySelector(".nxtpage-container");
                nxtpage_container.insertAdjacentHTML("beforebegin", response.responseText);
                nxtpage_container.classList.remove("hidden");
            }
            else{
                loader_container.insertAdjacentHTML("beforebegin", response.responseText);
            }
            loader_container.classList.add("hidden");
        }
    }
    if(!isinfinite)
        document.querySelector(".nxtpage-container").classList.add("hidden");
    document.querySelector(".loader-container").classList.remove("hidden");
    req.addEventListener("readystatechange", function(){insert(this, isinfinite)});
    req.open("GET", url, true);
    req.send();
}
