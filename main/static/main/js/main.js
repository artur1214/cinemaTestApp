
function getValue(id) {
    return document.getElementById('id_' + id).value;
}
function setValue(id, val) {
    document.getElementById('id_' + id).value = val;
}

function getCookie(name) {  //куки
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


async function onCinemaAdd(el) {
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    el.disabled = true

    let promise = await fetch('/api/cinema/add/', {
        method: 'POST',
        headers:{
            "X-CSRFToken": csrftoken
        },
        body: new FormData(add_form)
    })
    promise.json().then(result=> {
        $('#error-place').html('')
        if(result['ok'] == true){
            M.toast({html: 'Успешно добавлено'})
            setValue('title', '')
            setValue('adress', '')
        }
        else{
            //console.log(result['error']['title'][0]);
            if(result['error']['title']){
                $('#error-place').html(result['error']['title']);
            }
            else if(result['error']['adress']){
                $('#error-place').html(result['error']['adress']);
            }
            else if(result['error']){
                $('#error-place').html(result['error']);
            }

        }
        el.disabled = false;

    });

}

async function onScheduleAdd() {
    this.disabled = true;
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let promise = await fetch('/api/schedule/add/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: new FormData(add_form)
    })
    promise.json().then(result => {
        $('#error-place').html('')
        if (result['ok'] == true) {
            M.toast({html: 'Успешно добавлено'})
            setValue('title', '')
            setValue('date_time', null)
            //setValue('cinema_pick', 0)
        } else {
            //console.log(result['error']['title'][0]);
            if (result['error']['title']) {
                $('#error-place').html(result['error']['title']);
            }
            else if (result['error']['date_time']) {
                $('#error-place').html(result['error']['date_time']);
            }
            else if(result['error']['cinema']){
                $('#error-place').html(result['error']['cinema']);
            }
            else if (result['error']) {
                $('#error-place').html(result['error']);
            }
            this.disabled = false
        }
    });

}

async function deleteFilm(el) {
    let id = el.value
    let promise = await fetch('/api/remove/', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({id: id})
    })
    promise.json().then(result => {
        $('#error-place').html('')
        if (result['ok'] === true) {
            $(`#row_id_${id}`).remove()
        }
    })
}

//materialize инициализация
    $(document).ready(function () {
        $('select').formSelect();
    });

function scheduleFilter(){
    let date = $('#curDatePicker').val()
    let cinema = $('#cinema-pick').val()
    if(cinema){
        window.location.href = `?date=${date}&cinema=${cinema}`;
    }
    else{
        window.location.href = `?date=${date}`;
    }
    //window.location.href = `?date=${date}`;
}

function openEditWindow(el){
    let id = el.value;
    let modal = $('#edit_modal');
    //console.log($(`#row_id_${id}`).find('td'))
    let row = $(`#row_id_${id}`).find('td')
    $('#modal_update').val(id);
    $('#modal_delete').val(id);
    $('#title_edit').val(row[1].textContent)
    $('#adress_edit').val(row[2].textContent)
    modal.css('display', 'block');

}

async function deleteCinema(el) {
    let promise = await fetch('/api/cinema/update/', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({id: el.value, del: true})
    })
    promise.json().then(result => {
        if (result['ok'] == true) {
            $(`#row_id_${el.value}`).remove()
            $('#edit_modal').css('display', 'none')
        }
    })

}

async function updateCinema(el){
    let promise = await fetch('/api/cinema/update/', {

        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({id: el.value, del: false, title: $('#title_edit').val(), adress: $('#adress_edit').val()})
    })
    promise.json().then(result => {
        if (result['ok'] == true) {
            let cols = $(`#row_id_${el.value}`).find('td')
            cols[1].textContent = $('#title_edit').val()
            cols[2].textContent = $('#adress_edit').val()
            $('#edit_modal').css('display', 'none')
        }
        else{
            if(result['error']['title']){
                $('#error-place').html(result['error']['title']);
            }
            else if(result['error']['adress']){
                $('#error-place').html(result['error']['adress']);
            }
            else if(result['error']){
                $('#error-place').html(result['error']);
            }
        }
    })

}