var _IS_WAIT=false;

function popup_show(s) {
    alert(s);
}

function sw_post(post_data) {
    if (post_data.field&&Array.isArray(post_data.field)) {
        for (var i=0;i<post_data.field.length;i++) {
            post_data.data[post_data.field[i]]=$('#'+post_data.field[i]).val();
        }
    }

    if (post_data.is_wait !== false) {
        if(_IS_WAIT === true) {
            popup_show("요청 진행중인 작업이 있습니다. 잠시만 기다려주세요.");
        }
    }
    _IS_WAIT=true;

    var request = $.ajax({
        type: "POST",
        url: post_data.request_url,
        data: JSON.stringify(post_data.data),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8'}
    );

    request.done(function(result) {
        _IS_WAIT=false;
        if(result.error_code === 0) {
            if (typeof(post_data.next_url) === 'string') {
                location.href = post_data.next_url;
            } else if (typeof(post_data.next_url) === 'function') {
                post_data.next_url(result);
            }
        }
        else {
            if (result.error_code === 99999) {
                if (post_data.init_url) {
                    location.href = post_data.init_url;
                }
            }
            if (post_data.error && typeof(post_data.error) === 'function') {
                post_data.error(result.error_code, result.error_message);
            } else {
                alert(result.error_message);
            }
        }
    }).fail(function(err) {
        _IS_WAIT=false;
        console.error('ERROR :' + err.statusText);
        alert('ERROR :' + err.statusText);
    });
}
