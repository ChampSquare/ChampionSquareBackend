$(document).ready(function(){
    $question_type = $("#id_question_type");
    $marks = $("#id_marks");
    $subject = $("#id_subject");

    function question_filter() {
        $.ajax({
            url: "/exam/ajax/questions/filter/",
            type: "POST",
            data: {
                question_type: $question_type.val(),
                subject: $subject.val(),
                marks: $marks.val()
            },
            dataType: "html",
            success: function(output) {
                var questions = $(output).filter("#questions").html();
                $("#filtered-questions").html(questions);
            }
        });
    }

    $question_type.change(function() {
        question_filter()
    });

    $marks.change(function() {
        question_filter()
    });

    $subject.change(function () {
       question_filter()
    });

    $("#checkall").change(function(){
        if($(this).prop("checked")) {
                $("#filtered-questions input:checkbox").each(function(index, element) {
                $(this).prop('checked', true);
                });
        }
        else {
                $("#filtered-questions input:checkbox").each(function(index, element) {
                $(this).prop('checked', false);
                });
        }
    });
});