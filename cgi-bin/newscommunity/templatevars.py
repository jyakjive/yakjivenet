
DIV_COMMENTS = '''
<SCRIPT TYPE="text/javascript">
function submitCommentForm(cform){

    var frm = document.getElementById
        ? document.getElementById(cform)
        : document.forms[cform];

    if (!frm){
        for (i = 0; i < document.forms.length; i++){
            if (document.forms[i].name == cform){
                frm = document.forms[i];
                break;
            }
        }
    }

    var check = true;
    var curloc = null;
    if (frm.elements) {
        curloc = frm.elements['curlocation'];
        curloc.value = document.location;
        check = (frm.elements['tname'].value != '');
        check = (check && (frm.elements['comment'].value != ''));
        check = (check && (frm.elements['email'].value != '') && (frm.elements['email'].value.indexOf('.') > 0));
    } else {
        curloc = frm.curlocation;
        curloc.value = document.location;
        check = (frm.name.value != '');
        check = (check && (frm.comment.value != ''));
        check = (check && (frm.email.value != '') && (frm.email.value.indexOf('.') > 0));
    }
    if (check){
        frm.submit();
    } else {
        alert('You must complete all information\\nto submit a comment, including\\na valid email address or website.');
    }
}
</SCRIPT>
'''

DIV_GUESTBOOK = '''
<SCRIPT TYPE="text/javascript">
function submitGuestbookForm(gform){

    var frm = document.getElementById
        ? document.getElementById(gform)
        : document.forms[gform];

    if (!frm){
        for (i = 0; i < document.forms.length; i++){
            if (document.forms[i].name == gform){
                frm = document.forms[i];
                break;
            }
        }
    }

    var check = true;
    var curloc = null;
    if (frm.elements) {
        curloc = frm.elements['curlocation'];
        curloc.value = document.location;
        check = (frm.elements['tname'].value != '');
        check = (check && (frm.elements['title'].value != ''));
        check = (check && (frm.elements['comment'].value != ''));
        check = (check && (frm.elements['email'].value != '') && (frm.elements['email'].value.indexOf('.') > 0));
    } else {
        curloc = frm.curlocation;
        curloc.value = document.location;
        check = (frm.name.value != '');
        check = (check && (frm.title.value != ''));
        check = (check && (frm.comment.value != ''));
        check = (check && (frm.email.value != '') && (frm.email.value.indexOf('.') > 0));
    }
    if (check){
        frm.submit();
    } else {
        alert('You must complete all information\\nto submit a comment, including\\na valid email address or website.');
    }
}
</SCRIPT>
'''
