var myInterval, AttemptedAns = [], TotalTime = 0, time_dict = {}, delay = 1000, myStartExamInterval;

function NextQuestion(e) {
    var active_div_id = $(".test-questions").find("li.active").find("a").attr("data-href");
    var question_id = $(".questionId"+ active_div_id).val();
    saveUnanswered(question_id, getTimeSpent(active_div_id));

    var t = $(".test-questions").find("li.active");
    if (CheckNextPrevButtons(), t.is(":last-child")) 
        return !1;
    $(".test-questions").find("li").removeClass("active"), 
    t.next().addClass("active"), OpenCurrentQue(t.next().find("a")), e && (t.find("a").addClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"));
    var a = t.attr("data-seq");
    $(".nav-tab-sections").find("li").removeClass("active"), $(".nav-tab-sections").find("li[data-id=" + a + "]").addClass("active"), CheckQueAttemptStatus()
}

function openDialogModal(alert_text) {
    var modal = $("#myModal");

// Get the <span> element that closes the modal
  var span = $(".close")[0];
  modal.find("alert-text").text(alert_text);
   modal.css('display', 'block');

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.css('display', 'none');
}
}
  

function PrevQuestion(e) {
    var active_div_id = $(".test-questions").find("li.active").find("a").attr("data-href");
    var question_id = $(".questionId"+ active_div_id).val();
    saveUnanswered(question_id, getTimeSpent(active_div_id));

    var t = $(".test-questions").find("li.active");
    if (CheckNextPrevButtons(), t.is(":first-child")) return !1;
    $(".test-questions").find("li").removeClass("active"), t.prev().addClass("active"), OpenCurrentQue(t.prev().find("a"));
    var a = t.attr("data-seq");
    $(".nav-tab-sections").find("li").removeClass("active"), $(".nav-tab-sections").find("li[data-id=" + a + "]").addClass("active"), CheckQueAttemptStatus()

}

function CheckNextPrevButtons() {
    var e = $(".test-questions").find("li.active");
    $("#btnPrevQue").removeAttr("disabled"), $("#btnNextQue").removeAttr("disabled"), e.is(":first-child") ? $("#btnPrevQue").attr("disabled", "disabled") : e.is(":last-child") && $("#btnNextQue").attr("disabled", "disabled")
}

function pad(e, t) {
    for (var a = e + ""; a.length < t;) a = "0" + a;
    return a
}

function OpenCurrentQue(e) {
    
    $(".tab-content").hide(), $("#lblQueNumber").text(e.text()), $("#" + e.attr("data-href")).show();
    var t = e.parent().attr("data-seq");
    
    $(".nav-tab-sections").find("li").removeClass("active"), 
    $(".nav-tab-sections").find("li[data-id=" + t + "]").addClass("active"), CheckQueAttemptStatus()

    var active_div_id = $(".test-questions").find("li.active").find("a").attr("data-href");
    var question_id = $(".questionId"+ active_div_id).val();
    saveUnanswered(question_id, getTimeSpent(active_div_id));
}

function getTimeSpent(active_div_id) {
    var time_spent = (parseInt($("#"+active_div_id).find("#time_spent_value").val()));
    time_spent = time_spent ? time_spent : 0;
    return active_div_id in time_dict ? time_dict[active_div_id] : time_spent;            
}



function CoundownTimer(e) {
    var t = 60 * e;
    myInterval = setInterval(function () {
        myTimeSpan = 1e3 * t, $(".timer-title").text(GetTime(myTimeSpan)),
            t < 600 ? ($(".timer-title").addClass("time-ending"),
                $(".timer-title").removeClass("time-started")) : ($(".timer-title").addClass("time-started"),
                $(".timer-title").removeClass("time-ending")), t > 0 ? t -= 1 : CleartTimer()
    }, 1e3)
}

function CountUpTimer(e) {
    var t = 60 * e;
    myStartExamInterval = setInterval(function () {
        myTimeSpan = 1e3 * t, $(".count-timer-title").text(GetTime(myTimeSpan)), t < 600 ?
            ($(".count-timer-title").addClass("time-started"),
                $(".count-timer-title").removeClass("time-ending")) : ($(".count-timer-title").addClass("time-ending"),
                $(".count-timer-title").removeClass("time-started")), t > 0 ? t -= 1 : StartExam()
    }, 1e3)
}

function StartExam() {
    $("#btn_proceed").attr("disabled", false);
    clearInterval(myStartExamInterval);
}

function check_instruction() {
            if ($('#' + "en" + '_ch').prop("checked") == false) {
                    // alert('Please accept terms and conditions before proceeding.');
                    openDialogModal('Please accept terms and conditions before proceeding.');
            } else {
                    $('.exam-instruction').hide();
                    
                    $('.exam-countdown').hide();
                    $('.exam-paper').show();
                    $('.exam-paper').removeClass('hide').show();
                    
                    return $.ajax({
                 url: '/quiz/ajax/save_status',
                data: {
                'answer_paper_id': $('#paperId').val(),
                'status': 'instruction_read'
        },
        dataType: 'json',
        tryCount: 0,
        retryLimit: 3
    });}}

function CleartTimer() {
    clearInterval(myInterval), $("title").text("Time Out"), $("#btnYesSubmitConfirm").trigger("click")
}

function GetTime(e) {
    parseInt(e % 1e3 / 100);
    var t = parseInt(e / 1e3 % 60),
        a = parseInt(e / 6e4 % 60),
        n = parseInt(e / 36e5 % 24);
    return (n = n < 10 ? "0" + n : n) + ":" + (a = a < 10 ? "0" + a : a) + ":" + (t < 10 ? "0" + t : t)
}

function pretty_time_string(e) {
    return (e < 10 ? "0" : "") + e
}

function CheckQueExists(e) {
    $.each(AttemptedAns, function (t, a) {
        void 0 !== a && a[1] == e && AttemptedAns.splice(t, 1)
    })
}

function CheckQueAttemptStatus() {
    var e = 0,
        t = 0,
        a = 0,
        n = 0,
        s = 0,
        i = 0;
    $(".test-questions").find("li").each(function () {
        var r = $(this);
        e += 1, r.children().hasClass("que-save") ? a += 1 : r.children().hasClass("que-save-mark") ? n += 1 : r.children().hasClass("que-mark") ? s += 1 : r.children().hasClass("que-not-answered") ? t += 1 : i += 1
    }), $(".lblTotalQuestion").text(e), $(".lblNotAttempted").text(t), $(".lblTotalSaved").text(a), $(".lblTotalSaveMarkForReview").text(n), $(".lblTotalMarkForReview").text(s), $(".lblNotVisited").text(i)
}

function saveAnswer(question_id, answer_key, status, time_spent) {
    return $.ajax({
        url: '/quiz/ajax/save_answer/',
        data: {
            'answer_paper_id': $('#paperId').val(),
            'question_id': question_id,
            'answer_key': answer_key,
            'status': status,
            'time_taken': time_spent
        },
        dataType: 'json',
        tryCount: 0,
        retryLimit: 3
    });

}

function saveUnanswered(question_id, time_spent) {
    return $.ajax({
        url: '/quiz/ajax/save_unanswered/',
        data: {
            'answer_paper_id': $('#paperId').val(),
            'question_id': question_id,
            'time_taken': time_spent 
        },
        dataType: 'json',
        tryCount: 0,
        retryLimit: 3
    });
}


function CheckResult() {
    var n = 0
    $('#tbodyResult').html();
    var score = 0;
    var TotalQuestion = 0;
    var TotalAttempted = 0;
    var TotalCorrect = 0;
    var TotalWrong = 0;

    $(".test-questions").find("li").each(function () {
        var r = $(this);
        var a = r.find("a").attr("data-href");
        var currectAns = $("#" + a).find(".hdfCurrectAns").val();
        var currectQue = $("#" + a).find(".question-title").text();
        TotalQuestion = TotalQuestion + 1;
        var tr = $('<tr></tr>');
        tr.append('<td>' + currectQue + '</td>');
        var ansStatus = "Wrong";
        var selectedAns = '';
        if (r.children().hasClass("que-save") || r.children().hasClass("que-save-mark")) {
            $("#" + a).find("input[name='radios" + a + "']").each(function () {
                var e = $(this);
                if (e.is(':checked')) {
                    selectedAns = e.val();
                    if (e.val() == currectAns) {
                        ansStatus = "Correct";
                    }
                }
            });
            if (ansStatus == 'Correct') {
                score = score + 4;
                TotalCorrect = TotalCorrect + 1;
            } else {
                score = score - 1;
                TotalWrong = TotalWrong + 1;
            }
            TotalAttempted = TotalAttempted + 1;
        }
        if (r.children().hasClass("que-save") || r.children().hasClass("que-save-mark")) {
            tr.append('<td>' + selectedAns + '</td>');
        } else {
            tr.append('<td>---</td>');
        }
        if (r.children().hasClass("que-save") || r.children().hasClass("que-save-mark")) {
            if (ansStatus == 'Correct') {
                tr.append('<td><span class="label label-success">' + ansStatus + '</span></td>');
            } else {
                tr.append('<td><span class="label label-danger">' + ansStatus + '</span></td>');
            }
        } else {
            tr.append('<td>N/A</td>');
        }
        tr.append('<td>' + currectAns + '</td>');
        $('#tbodyResult').append(tr);
    });

    $.ajax({
        url: '/quiz/ajax/save_status/',
        data: {
            'paper_id': $('#paperId').val(),
            'status': 'submitted_by_user'
        },
        dataType: 'json',
        tryCount: 0,
        retryLimit: 3,

         success: function (data) {
           // do something
         },
        error: function (xhr, textStatus, errorThrown) {
            if(textStatus=='timeout') {
                this.tryCount++;
                if(this.tryCount <= this.retryLimit) {
                    // try again
                    $.ajax(this);
                    return;
                }
                return;
            }
            if(xhr.status == 500) {
                // handle error
            } else {
                // handle error
            }
        }
      });

    $('#lblRTotalQuestion').text(TotalQuestion);
    $('#lblRTotalAttempted').text(TotalAttempted);
    $('#lblRTotalCorrect').text(TotalCorrect);
    $('#lblRTotalWrong').text(TotalWrong);
    $('#lblRScore').text(score);
}

$(document).ready(function () {
    $("#page01").show();
    // $(".exam-paper").show();
    $("#btn_proceed").attr("disabled", true);

    CoundownTimer(parseInt($("#hdfTestDuration").val()));
    CountUpTimer(parseInt($("#countdown_timer").val()));
    CheckNextPrevButtons();
    CheckQueAttemptStatus();
    
    setInterval(function() {
        var active_div_id = $(".test-questions").find("li.active").find("a").attr("data-href");
        $("#"+active_div_id).find(".time-spent").text(GetTime(getTimeSpent(active_div_id)+1000));
        time_dict[active_div_id] = getTimeSpent(active_div_id)+1000
        
    }, 1000);

    $("#btnPrevQue").click(function () {
        PrevQuestion(!0)
    });
    $("#btnNextQue").click(function () {
        NextQuestion(!0)
    });
    $(".test-ques").click(function () {
        var e = $(".test-questions").find("li.active").find("a");
        OpenCurrentQue($(this));
        $(".test-questions").find("li").removeClass("active"),
            $(this).parent().addClass("active"),
            $(this).hasClass("que-save") ||
            $(this).hasClass("que-save-mark") ||
            $(this).hasClass("que-mark") ||
            ($(this).addClass("que-not-answered"),
                $(this).removeClass("que-not-attempted")),
        e.hasClass("que-save") || e.hasClass("que-save-mark") ||
        e.hasClass("que-mark") || (e.addClass("que-not-answered"),
            e.removeClass("que-not-attempted"))
    });
    $(".btn-save-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            n = ($("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(), $("#" + a).find(".hdfCurrectAns").val(), !1);

        var question_type = $(".questionType"+ a).val();

        if(question_type !== "integer") {
            if ($("input[name='radios" + a + "']").each(function () {
                $(this).is(":checked") && (n = !0)
            }), 0 == n) {
                // alert("Please choose an option");
                // alert("Please choose an option");
                openDialogModal("Please choose an option first, then click on save");
                return !1
            }
            ;
        } else {
            $("input[name='answer" + a + "']").each(function ()
                {
                if( $(this).val().length === 0) {
                    // alert("Please enter an integer");
                    // alert("Please enter a numeric value!");
                    openDialogModal("Please enter a numeric value first, then click on save");

                    throw new Error('This is not an error. This is just to abort javascript');
                }
            });
        }

        var answer_key = $("input[name='radios" + a + "']:checked").val(),
            question_id = $(".questionId"+ a).val();
        if(question_type === "integer") {
            answer_key = $("#answer"+a).val();
        }

        $(answer_key), t.find("a").removeClass("que-save-mark"), t.find("a").removeClass("que-mark"), t.find("a").addClass("que-save"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()
     saveAnswer(question_id, answer_key, "answered", getTimeSpent(a))
    });

    $(".btn-save-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            n = ($("#" + a).find(".hdfQuestionID").val(),
                $("#" + a).find(".hdfPaperSetID").val(),
                $("#" + a).find(".hdfCurrectAns").val(),
                $("#" + a).find(".hdfCurrectAns").val(), !1);

        var question_type = $(".questionType"+ a).val();

        if(question_type !== "integer") {
            if ($("input[name='radios" + a + "']").each(function () {
                $(this).is(":checked") && (n = !0)
            }), 0 == n) {
                alert("Please choose an option");
                return !1
            }
            ;
        } else {
            $("input[name='answer" + a + "']").each(function ()
                {
                if( $(this).val().length === 0 ) {
                    // alert("Please enter an integer");
                    openDialogModal("Please enter a numeric value first, then click on save");

                    throw new Error('This is not an error. This is just to abort javascript');
                }
            });
        }

        var answer_key = $("input[name='radios" + a + "']:checked").val(),
            question_id = $(".questionId"+ a).val();

        if(question_type === "integer") {
            answer_key = $("#answer"+a).val();
        }

        $(answer_key), t.find("a").removeClass("que-save"), t.find("a").removeClass("que-mark"), t.find("a").addClass("que-save-mark"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()

        saveAnswer(question_id, answer_key, "4", getTimeSpent(a));

    });
    $(".btn-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href");
        var question_type = $(".questionType"+ a).val();

        var answer_key = $("input[name='radios" + a + "']:checked").val(),
            question_id = $(".questionId"+ a).val();

        if(question_type === "integer") {
            answer_key = $("#answer"+a).val();
        }

        $("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(), $("#" + a).find(".hdfCurrectAns").val(), $("#" + a).find(".hdfCurrectAns").val(), t.find("a").removeClass("que-save-mark"), t.find("a").removeClass("que-save"), t.find("a").addClass("que-mark"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()
        saveAnswer(question_id, answer_key, "marked", getTimeSpent(a));

    });
    $(".btn-reset-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href");
        $("#" + a).attr("data-queid"), t.find("a").removeClass("saved-que"),
            $("input[name='radios" + a + "']:checked").each(function () {
                $(this).prop("checked", !1).change()
            }), $("input[name='chk" + a + "']").each(function () {
                $(this).prop("checked", !1).change()
            }), $("input[type=checkbox]").prop("checked", !1).change(),
            $("input[name='answer"+ a + "']").val(""), a = t.find("a").attr("data-href"),
            $("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(),
            $("#" + a).find(".hdfCurrectAns").val(), $("#" + a).find(".hdfCurrectAns").val(),
            t.find("a").removeClass("que-save-mark"),
            t.find("a").removeClass("que-mark"),
            t.find("a").removeClass("que-save"),
            t.find("a").removeClass("que-not-attempted"),
            t.find("a").addClass("que-not-answered"),
            //NextQuestion(!1),
            CheckQueAttemptStatus()

        $.ajax({
        url: '/quiz/ajax/clear_answer/',
        data: {
            'answer_paper_id': $('#paperId').val(),
            'question_id': $(".questionId"+ a).val(),
            'time_taken': getTimeSpent(a)
        },
        dataType: 'json',
        tryCount: 0,
        retryLimit: 3
    });

    });
    $(".btn-submit-all-answers").click(function (e) {
        e.preventDefault(), $(this),
            $(".test-questions").find("li").each(function () {
                var e = $(this),
                    t = !1;
                if (e.children().hasClass("que-save") ? t = !0 : e.children().hasClass("que-save-mark") && (t = !0), t) {
                    var a = e.find("a").attr("data-href");
                    //console.log(a), $("#" + a);
                    $("#" + a).find(".hdfCurrectAns").val();
                    $("#" + a).find("input[name='radios" + a + "']").each(function () {
                        var e = $(this);
                        e.is(":checked") && e.val()
                    });
                }
            }),
            $(".exam-paper").hide(),
            $(".stream_1").hide(),
            $("#divdrplngcng").hide()

            $(".exam-summery").show(),
            CheckQueAttemptStatus()
    });
    $("#btnYesSubmit").on("click", function (e) {
        e.preventDefault(), $(".exam-confirm").show(), $("#divdrplngcng").hide(), $(".exam-summery").hide()
    });
    $("#btnNoSubmit").on("click", function (e) {
        e.preventDefault(), $(".exam-paper").show(), $(".stream_1").show(), $(".exam-summery").hide(), $("#divdrplngcng").show()
    });
    $("#btnYesSubmitConfirm").on("click", function (e) {
        e.preventDefault(),$(".exam-paper").hide(), $(".exam-thankyou").show(), $("#divdrplngcng").hide(), $(".exam-confirm").hide(), CheckResult();
    });
    $("#btnNoSubmitConfirm").on("click", function (e) {
        e.preventDefault(), $(".exam-paper").show(), $(".stream_1").show(), $(".exam-confirm").hide(), $("#divdrplngcng").show()
    });
    $('.drplanguage').on('change', function (e) {
        e.preventDefault();
        var newlang = 'English';

        if ($(this).val() == 'english') {
            newlang = 'English';
        } else if ($(this).val() == 'hindi') {
            newlang = 'Hindi';
        } else if ($(this).val() == 'gujarati') {
            newlang = 'Gujarati';
        }
        var currentLang = $('#hdfCurrentLng').val();
        $('.question-height > .img-responsive').each(function (index, item) {
            var currentImg = $(this);
            var currentImgSrc = currentImg.attr('src');
            currentImg.attr('src', currentImgSrc.replace(currentLang, newlang) + '?' + new Date());
        });
        $('#hdfCurrentLng').val(newlang);
    });
    $('.stream_1').on('click', function (e) {
        e.preventDefault();
        var current_herf = $(this).attr('data-href');
        var a = $(".test-questions").find("li").find("a[data-href=" + current_herf + "]");
        a.trigger('click');
    });
    $('#btnViewResult').on('click', function (e) {
        e.preventDefault();
        CheckResult();
        $('.exam-result').show();
        $(".exam-thankyou").hide();
        $("#divdrplngcng").hide();
    });

    $('#btnRBack').on('click', function (e) {
        e.preventDefault();
        window.location.replace("/exam/start/4/");

    });
});