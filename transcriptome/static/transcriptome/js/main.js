function toggleAll(toggle_id, id) {
    box = document.getElementById(toggle_id);

    if (box.checked == true) {
        var setting = true;
    } else {
        var setting = false;
    }

    var cur_id = id + '0';

    var count = 1;
    while(box = document.getElementById(cur_id)) {
        box.checked = setting;
        cur_id = id + count;
        count++;
    }
}
