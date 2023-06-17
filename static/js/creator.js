$(document).ready(function(){
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var url_ = $("input[name=url]").val();
    $(".ubutton").click(function(){
        var quetions = [];
        var divs = $('#cont').children('.quetion');
        var count = divs.length;
        if (count == 0) {
            alert('У тесті має бути принаймні одне питання!')
        } else {
            $(divs).each(function(){
                var answers = [];
                var text = $(this).children('.q').text();
                var points = $(this).children('.p').text();
                var ans = $(this).children('.a');
                $(ans).each(function(){
                    var text = $(this).text();
                    var is_correct = false;
                    if (text.slice(3, 12) == "[CORRECT]") {
                        text = text.slice(13, text.length + 1);
                        is_correct = true;
                    } else {
                        text = text.slice(3, text.length + 1);
                    }
                    let answer = {
                        text : text,
                        is_correct : is_correct
                    };
                    answers.push(answer);
                });
                let quetion = {
                    text : text,
                    points : points,
                    ans : answers
                };
            quetions.push(quetion);
            });
            $.ajax({
                url: "",
                type: "post",
                data: {
                    qname : $('#newtestcont').children('.hi').children('input').val(),
                    desc : $('#newtestcont').children('textarea').val(),
                    hours : $('#newtestcont').children('.t_cont').children('.t1').val(),
                    minutes : $('#newtestcont').children('.t_cont').children('.t2').val(),
                    seconds : $('#newtestcont').children('.t_cont').children('.t3').val(),
                    pub_time : $('#newtestcont').children('.dt_cont').children('input').val(),
                    deadline : $('#newtestcont').children('.dt_cont2').children('input').val(),
                    m_points: $('#newtestcont').children('.m_points').children('input').val(),
                    q : JSON.stringify(quetions),
                    csrfmiddlewaretoken : csrf
                },
                success: function(response) {
                    window.location = url_;
                },
                error: function(response) {
                    console.log(0);
                }
            });
        };
    });

    $(".new_quetion_btn").click(function(){
        $("#cont").append(`
        <div class="unquetion" style="border:2px solid white; border-radius:5px; background: rgb(255,0,0);
        background: linear-gradient(90deg, rgba(255,0,0,0.2) 0%, rgba(222,222,222,0.2) 0%); padding: 5px">
        <p class="qname">Текст питання:
        <input class="longblock" name="q_name" type="text"></p>
        <p class="points">Кількість балів:
        <input class="shortblock" name="points" type="number"></p>
        <div class="ans_cont">
        </div>
        <button class="new_ans submission new_t_btn_s" type="button">Додати відповіть</button>
        <button class="post_quet submission new_t_btn_s" type="button">Зберегти питання</button>
        </div>
        `);
    });

    $('.ubutton').click(function(){
        if ($(this.parentNode).children('.hi').children('input:checked').length) {
            console.log(1);
        }; 
    });

    $('#cont').on('click', '.new_ans', function(){
        $(this.parentNode).children('.ans_cont').append(`
        <div class="ans">
        <p>Текст відповіді:</p>
        <input type="text" class="ans longblock lbplus" name="answer">
        <input class="correctness" type="checkbox" name="correct">Правильна відповідь</div>
        `);
    });

    $('#cont').on('click', '.post_quet', function(){
        var qname = $(this.parentNode).children('.qname').children('input').val();
        var points = $(this.parentNode).children('.points').children('input').val();
        var cnt = $(this.parentNode).children('.ans_cont').children();
        var count = $(this.parentNode).children('.ans_cont').children().length;
        var quetions = '';
        var cnter = 1;
        var cor = false;
        $(this.parentNode).children('.ans_cont').children().each(function(){
            if ($(this).children('.correctness').is(":checked")) {
                cor = true;
            }
        })
        if (count == 0 || cor == false) {
            alert("Питання має мати принаймні 1 правильна відповідь.");
        } else {
            $(cnt).each(function(){
                quetions += '<p class="a">'
                quetions += cnter;
                quetions += '. '
                cnter += 1;
                if ($(this).children('input:checked').length) {
                    quetions += '[CORRECT] ';
                };
                quetions += $(this).children('input.ans').val();
                quetions += '</p>';
            });
            var out = `<div class="quetion" style="border:2px solid white; border-radius:5px; background: rgb(255,0,0);
            background: linear-gradient(90deg, rgba(255,0,0,0.2) 0%, rgba(222,222,222,0.2) 0%);     padding: 5px"><b>Питання:</b> <p class="q">`
                + qname + '</p><b>Кількість балів:</b> <p style="display:inline" class="p">' + points 
                + '</p><br><b>Відповіді:</b>' + quetions + '</div>';
            $(this.parentNode).replaceWith(out);
        };
    });
});

