$(document).ready(function() {

  var current_fs, next_fs, previous_fs; //fieldsets
  var opacity;
  var current = 1;
  var steps = $("fieldset").length;

  setProgressBar(current);

  $(".next").click(function() {

    current_fs = $(this).parent();
    next_fs = $(this).parent().next();

    //Add Class Active
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    //show the next fieldset
    next_fs.show();
    //hide the current fieldset with style
    current_fs.animate({
      opacity: 0
    }, {
      step: function(now) {
        // for making fielset appear animation
        opacity = 1 - now;

        current_fs.css({
          'display': 'none',
          'position': 'relative'
        });
        next_fs.css({
          'opacity': opacity
        });
      },
      duration: 500
    });
    setProgressBar(++current);
  });

  $(".previous").click(function() {

    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();

    //Remove class active
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    previous_fs.show();

    //hide the current fieldset with style
    current_fs.animate({
      opacity: 0
    }, {
      step: function(now) {
        // for making fielset appear animation
        opacity = 1 - now;

        current_fs.css({
          'display': 'none',
          'position': 'relative'
        });
        previous_fs.css({
          'opacity': opacity
        });
      },
      duration: 500
    });
    setProgressBar(--current);
  });

  function setProgressBar(curStep) {
    var percent = parseFloat(100 / steps) * curStep;
    percent = percent.toFixed();
    $(".progress-bar")
      .css("width", percent + "%")
  }

  $(".submit").click(function() {
    return false;
  })

});


function reply_upvote(upvote,post_id,category,reply_id) {
            upvote += 1
            console.log(upvote)
              $.ajax({
                  url: "/reply/upvote",
                  type: "POST",
                  data:{
                          upvote : upvote,
                          post_id : post_id,
                          category : category,
                          reply_id : reply_id
                          } ,
                  success: function(){
                          update()
                  },
                  error: function (xhr) {
                      alert('error');
                  }
              })
              return false;
          }

          function upvote(upvote,post_id,category) {
            upvote += 1
              $.ajax({
              url: "/upvote",
              type: "POST",
              data:{
                      upvote : upvote,
                      post_id : post_id,
                      category : category
                      } ,
              success: function(){
                      update()
              },
              error: function (xhr) {
                  alert('error');
              }
          })
          return false;
          }

          function update(){
              $("#forum").load(location.href + " #forum");
          }
