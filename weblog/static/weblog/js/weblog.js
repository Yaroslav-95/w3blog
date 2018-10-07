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

function loadBlogPosts(page = 2, category = null){
}
