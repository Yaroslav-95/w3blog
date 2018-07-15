function toggleNode(caller){
    state = $(caller).attr('node-state');
    target = $(caller).attr('node-target');
    if(state=='closed'){
        $(caller).html('—');
        $(caller).attr('node-state', 'open');
    }
    else{
        $(caller).html('+');
        $(caller).attr('node-state', 'closed');
    }
    $('#'+target).toggle();
}
