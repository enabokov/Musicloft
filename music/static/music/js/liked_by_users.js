$(function(){
  function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
  }

  $('.like').on('click', function(){
    var band_name = $(this).parent().parent()
      .prev().children('a').attr('title');
    $.ajax({
              type: 'POST',
              url: 'addliked/',
              data: {
                  'band_id': $(this).attr('data-value'),
                  'csrfmiddlewaretoken': getCookie('csrftoken')
              },
              success: function () {
                alert('You have liked ' + band_name +
                  '!\nThis will be used for your next recommendations')
              }
    });
  });

  $('.dislike').on('click', function(){
    var band_name = $(this).parent().parent()
      .prev().children('a').attr('title');
    $.ajax({
              type: 'POST',
              url: 'adddisliked/',
              data: {
                  'band_id': $(this).attr('data-value'),
                  'csrfmiddlewaretoken': getCookie('csrftoken')
              },
              success: function () {
                alert('Oh, you have disliked ' + band_name +
                  '!\nThis will be used for your next recommendations');
              }
    })
  })
});