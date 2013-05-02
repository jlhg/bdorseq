function toggle(form_name) {
    checkboxes = document.getElementsByName(form_name.name);

    for (var i = 0, n = checkboxes.elements.length; i < n; i++) {
        checkboxes.elements[i].checked = form_name.elements[i].checked;
    }

}
