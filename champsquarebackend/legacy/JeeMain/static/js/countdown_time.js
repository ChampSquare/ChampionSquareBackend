var myInterval, AttemptedAns = [], TotalTime = 0;


function CoundownTimer(e) {
    var t = 60 * e;
    myInterval = setInterval(function () {
        myTimeSpan = 1e3 * t,
            $(".timer-title").text(GetTime(myTimeSpan)),
            t < 600 ? ($(".timer-title").addClass("time-ending"),
                $(".timer-title").removeClass("time-started")) : ($(".timer-title").addClass("time-started"),
                $(".timer-title").removeClass("time-ending")), t > 0 ? t -= 1 : CleartTimer()
    }, 1e3)
}

function CleartTimer() {
    window.location.replace("/exam/start/2/");
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


$(document).ready(function () {
    CoundownTimer(parseInt($("#hdfTestDuration").val()));
    CheckNextPrevButtons();
    CheckQueAttemptStatus();
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
        if ($("input[name='radios" + a + "']").each(function () {
            $(this).is(":checked") && (n = !0)
        }), 0 == n) { alert("Please choose an option"); return !1 };

        var answer_key = $("input[name='radios" + a + "']:checked").val(),
            question_id = $(".questionId"+ a).val();

        $(answer_key), t.find("a").removeClass("que-save-mark"), t.find("a").removeClass("que-mark"), t.find("a").addClass("que-save"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()
     saveAnswer(question_id, answer_key, "2")
    });

    $(".btn-save-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href"),
            n = ($("#" + a).find(".hdfQuestionID").val(),
                $("#" + a).find(".hdfPaperSetID").val(),
                $("#" + a).find(".hdfCurrectAns").val(),
                $("#" + a).find(".hdfCurrectAns").val(), !1);
        if ($("input[name='radios" + a + "']").each(function () {
            $(this).is(":checked") && (n = !0)
        }), 0 == n) { alert("Please choose an option"); return !1 };

        var answer_key = $("input[name='radios" + a + "']:checked").val(),
            question_id = $(".questionId"+ a).val();

        $(answer_key), t.find("a").removeClass("que-save"), t.find("a").removeClass("que-mark"), t.find("a").addClass("que-save-mark"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()

        saveAnswer(question_id, answer_key, "4");

    });
    $(".btn-mark-answer").click(function (e) {
        e.preventDefault();
        var t = $(".test-questions").find("li.active"),
            a = t.find("a").attr("data-href");
        var answer_key = $("input[name='radios" + a + "']:checked").val(),
            question_id = $(".questionId"+ a).val();

        $("#" + a).find(".hdfQuestionID").val(), $("#" + a).find(".hdfPaperSetID").val(), $("#" + a).find(".hdfCurrectAns").val(), $("#" + a).find(".hdfCurrectAns").val(), t.find("a").removeClass("que-save-mark"), t.find("a").removeClass("que-save"), t.find("a").addClass("que-mark"), t.find("a").removeClass("que-not-answered"), t.find("a").removeClass("que-not-attempted"), NextQuestion(!1), CheckQueAttemptStatus()
        saveAnswer(question_id, answer_key, "3");

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
            $("input[type=text]").val(""), a = t.find("a").attr("data-href"),
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
        url: '/jee_main/ajax/clear_answer/',
        data: {
            'answer_paper_id': $('#paperId').val(),
            'question_id': $(".questionId"+ a).val()
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
        e.preventDefault(), $(".exam-thankyou").show(), $("#divdrplngcng").hide(), $(".exam-confirm").hide(), CheckResult();
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
        window.location.href = $('#hdfBaseURL').val() + "/#mocktests"
    });
});