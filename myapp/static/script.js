var chiiLib = {
    airTimeMenu: {
        settings: {
            'target': $("#airTimeMenu > li.airYear"),
            'yearTestRegex': /(\d{4})$/
        },
        init: function () {
            var ul = chiiLib.airTimeMenu.settings.target;
            if (ul.html() == null) {
                return;
            }
            var anchors = ul.find("a");
            var increased = 0;
            var tmoutMoveHandle;
            var tmoutOutHandle;
            chiiLib.airTimeMenu.closeFuture(anchors);
            ul.mouseout(function (event) {
                clearTimeout(tmoutMoveHandle);
                clearTimeout(tmoutOutHandle);
                tmoutOutHandle = chiiLib.airTimeMenu.tmoutEventOut();
                return false;
            });
            ul.mousemove(function (event) {
                clearTimeout(tmoutOutHandle);
                clearTimeout(tmoutMoveHandle);
                tmoutMoveHandle = chiiLib.airTimeMenu.tmoutEventMove(this);
                return false;
            });
            $("#pastAirTime").click(function (event) {
                chiiLib.airTimeMenu.updateYearAnchors('-', increased, ul, anchors);
                return false;
            });
            $("#futureAirTime").click(function (event) {
                chiiLib.airTimeMenu.updateYearAnchors('+', increased, ul, anchors);
                return false;
            });
        },
        tmoutEventMove: function (target) {
            return setTimeout(function () {
                var self = $(target);
                if (self.children().is('ul')) {
                    return false;
                }
                var prevUl = $('#airMonthMenu');
                prevUl.attr('id', 'airMonthMenuPrev');
                var ul = $("<ul>").attr('id', 'airMonthMenu');
                var baseId = self.find('a').attr('id');
                var pre = $("#airTimeMenu").find("[class='l focus']");
                var preid = pre.attr('id');
                var tid = preid.split('-');
                if(baseId == preid && tid.length == 2){
                    baseId = tid[0];
                    ul.append($("<li>").append($("<a>").text('全年').attr('id', baseId).attr('href', 'javascript:void(0);')));
                    var premonth = parseInt(tid[1]);
                    for (var i = 1; i < 13; i++) {
                        if(i != premonth) {
                            ul.append($("<li>").append($("<a>").text(i + '月').attr('id', baseId + '-' + i).attr('href', 'javascript:void(0);')));
                        }
                    }
                }else {
                    for (var i = 1; i < 13; i++) {
                        ul.append($("<li>").append($("<a>").text(i + '月').attr('id', baseId + '-' + i).attr('href', 'javascript:void(0);')));
                    }
                }
                ul.hide();
                self.append(ul);
                //self.find('> a').addClass('focus')
                ul.fadeIn(50);
                // prevUl.parent().find('> a').removeClass('focus');
                prevUl.fadeOut('fast', 'swing', function () {
                    prevUl.remove();
                });
            }, 5);
        },
        tmoutEventOut: function () {
            return setTimeout(function () {
                $menu = $('#airMonthMenu');
                $menu.fadeOut('fast', 'swing', function () {
                    //$menu.parent().find('> a').removeClass('focus');
                    $menu.remove();
                }, 'fast');
            }, 10);
        },
        closeFuture: function (anchors) {
            var id = anchors[0].id;
            var date = new Date();
            var yearTestRegex = chiiLib.airTimeMenu.settings.yearTestRegex;
            yearTestRegex.test(id);
            if (RegExp.$1 >= date.getFullYear()) {
            } else {
                var ul = chiiLib.airTimeMenu.settings.target;
                increased = -parseInt((date.getFullYear() - RegExp.$1) / ul.length);
            }
        },
        updateYearAnchors: function (sign, increased, ul, anchors) {
            var id = '';
            var newYear = 0;
            var year = 0;
            sign == '+' ? increased++ : increased--;
            date = new Date();
            if (increased < 0) {
                $("#futureAirTime").css('visibility', 'visible');
            } else if (increased == 0) {
                $("#futureAirTime").css('visibility', 'hidden');
            }
            anchRoll = function (num) {
                var yearTestRegex = chiiLib.airTimeMenu.settings.yearTestRegex;
                increment = parseInt(sign + 1);
                for (var i = 0; i < ul.length; i++) {
                    id = anchors[i].id;
                    yearTestRegex.test(id);
                    year = RegExp.$1;
                    newYear = eval(parseInt(year) + increment);
                    anchors[i].id = newYear;
                    anchors[i].innerHTML = anchors[i].innerHTML.replace(/^\d{4}/, newYear);
                }
                if (--num == 0) {
                    return;
                } else {
                    setTimeout('anchRoll( ' + num + ');', 40);
                }
            };
            anchRoll(ul.length);
        }
    }
};
$(document).ready(function () {
    var interval = ''
    function bgmusume() {
        if(interval != ''){
            clearInterval(interval);
            interval = '';
        }
        var rand = 1 + Math.floor(Math.random()*6)
        $("#bgmusume").attr('class', 'bg musume_' + rand);
        $("#bgmusume").css("background-position", -40 * (rand - 1) + 'px ' + 0 + 'px');
    }
    function bgmusume_run(status) {
        var pos = 0;
        var speed = -10;
        function move() {
            if(pos <= -240) {
                pos = 0;
            }
            $("#bgmusume").css("background-position", pos + 'px ' + 0 + 'px');
            pos = pos + speed;
        }
        interval = setInterval(move, 120);
    }
    function scroll() {
        window.scrollBy(0, -60);
        scrolldelay = setTimeout(scroll, 20);
        var sTop = document.documentElement.scrollTop + document.body.scrollTop;
        if(sTop == 0) clearTimeout(scrolldelay);
    }

    function pageshow(page, maxpage, part) {
        page = parseInt(page);
        maxpage = parseInt(maxpage);
        str = '';
        var start = page - 2;
        var end = page + 7;
        if(start < 1){
            start = 1;
        }
        if(end > maxpage){
            end = maxpage;
        }
        if(page > 3){
            str += '<a href="javascript:void(0);" class="p">|‹</a>';
        }
        if(page > 1){
            str += '<a href="javascript:void(0);" class="p">‹‹</a>';
        }
        for(var i = start; i < page; i ++){
            str += '<a href="javascript:void(0);" class="p">' + i + '</a>';
        }
        str += '<strong class="p_cur">' + page + '</strong>';
        for(var i = page + 1; i <= end; i ++){
            str += '<a href="javascript:void(0);" class="p">' + i + '</a>';
        }
        if(page < maxpage){
            str += '<a href="javascript:void(0);" class="p">››</a>';
        }
        if(page < maxpage - 7){
            str += '<a href="javascript:void(0);" class="p">›|</a>';
        }
        str += '<a class="p_pages" style="padding: 0px">\
                <input id="pageinput1" class="inputtext" style="width:30px;" type="text" name="custompage"></a>';
        str += '<span class="p_edge">(&nbsp;' + page + '&nbsp;/&nbsp;' + maxpage + '&nbsp;)</span>';
        if(part == 'part1'){
            $("#multipage1").html(str);
        }else{
            str = str.replace('pageinput1', 'pageinput2');
            $("#multipage2").html(str);
        }
    }

    function part1show(ret) {
        str = '';
        for (i in ret.data) {
            var x = ret.data[i];
            str += '<a href="javascript:void(0);" class="l level1">' + x[0] + '</a><small class="grey">(' + x[1] + ')</small> &nbsp;';
        }
        $("#tagList").html(str);
        pageshow(ret.page, ret.maxpage, 'part1');
    }

    function part1() {
        bgmusume();
        $(".part2").hide();
        $(".part1").show();
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part1', data : '', page : '1', curpage : ''},
            success: function (ret) {
                part1show(ret);
            }
        });
    }
    part1();
    chiiLib.airTimeMenu.init();

    function select_click(ret) {
        bgmusume();
        $(".part1").hide();
        $(".part2").show();
        str = '';
        for (i in ret.data) {
            var x = ret.data[i];
            str += '\
            <li id="item_' + x['id'] + '" class="item odd clearit">\
            <a href="https://bgm.tv/subject/' + x['id'] + '" class="subjectCover cover ll">\
            <span class="image">\
            <img src="' + x['img'] + '" class="cover">\
            </span>\
            <span class="overlay"></span>\
            </a>\
            <div class="inner">\
            <div id="collectBlock_' + x['id'] + '" class="collectBlock tip_i">\
            \
            </div>\
            <h3>\
            <a href="https://bgm.tv/subject/' + x['id'] + '" class="l">' + x['namechs'] + '</a> <small class="grey">' + x['namejp'] + '</small>\
            </h3>';
            if (x['rank'] != '123456789') {
                str += '<span class="rank"><small>Rank </small>' + x['rank'] + '</span>';
            }
            str += '\
            <p class="info tip">' + x['tip'] + '</p>\
            <p class="rateInfo">\
            <span class="' + x['starstr'] + '"></span> <small class="fade">' + x['star'] + '</small> <span class="tip_j">' + x['votes'] + '</span>\
            </p>\
            </div>\
            </li>';
        }
        $("#browserItemList").html(str);
        str = '';
        for (i in ret.tag) {
            var x = ret.tag[i];
            str += '<li><a href="javascript:void(0);" class="l"><span>' + x[0] + '(' + x[1] + ')</span></a></li>'
        }
        $("#select").html(str);
        pageshow(ret.page, ret.maxpage, 'part2');
    }

    $("#tagList").on('click', 'a', function () {
        var data = $(this).text();
        $("#result").append('<li><a href="javascript:void(0);" class="l"><span>' + data + '</span></a></li>');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part1', data : data, page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });

    $("#select").on('click', 'li', function () {
        var copy = $(this).clone();
        copytext = copy.text();
        copytext = copytext.substring(0, copytext.lastIndexOf('('));
        copy.children().text(copytext);
        var flag = 1;
        $("#result li").each(function () {
            if (copytext == $(this).text()) {
                flag = 0;
            }
        });
        if (flag == 0) {
            return;
        }
        $("#result").append(copy);
        var tag = '';
        $("#result li").each(function () {
            tag += $(this).text() + '&';
        });
        var cat = $("#cat > li [class='l focus']").text();
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        var sort = $("#browserTools").find("[class='l focus']").attr('id');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag : tag, cat : cat, time : time, sort : sort, page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });

    $("#cat").on('click', 'li', function () {
        if ($(this).attr('class') == 'l focus') {
            return;
        }
        var tag = '';
        $("#result li").each(function () {
            tag += $(this).text() + '&';
        });
        var cat = $(this).text();
        $(this).siblings().children().removeClass('focus');
        $(this).children().addClass('focus');
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        var sort = $("#browserTools").find("[class='l focus']").attr('id');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag : tag, cat : cat, time : time, sort : sort, page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });

    $("#airTimeMenu").on('click', 'a', function () {
        var id = $(this).attr('id');
        var pre = $("#airTimeMenu").find("[class='l focus']");
        var preid = pre.attr('id');
        if(id == preid) {
            return;
        }
        pre.removeClass('focus');
        var tid = preid.split('-');
        if(tid.length == 2){
            pre.text(tid[0] + '年');
            pre.attr('id', tid[0]);
        }
        if(id == 'timeall'){
            $(this).addClass('focus');
        } else if(id.length == 4){
            if(tid.length == 2 && tid[0] == id){
                $(this).parent().parent().prev().addClass('focus');
            }else{
                $(this).addClass('focus');
            }
        } else{
            var year = $(this).parent().parent().prev();
            year.text(id);
            year.addClass('focus');
            year.attr('id', id);
        }
        var tag = '';
        $("#result li").each(function () {
            tag += $(this).text() + '&';
        });
        var cat = $("#cat > li [class='l focus']").text();
        var sort = $("#browserTools").find("[class='l focus']").attr('id');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag : tag, cat : cat, time : id, sort : sort, page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });

    function dosearch() {
        var text = $("#search_text").val();
        text = text.replace(/(^\s*)|(\s*$)/g, "");
        if (text.length == 0) {
            return;
        }
        text = text.split(/\s+|,|，/);
        var flag = 0;
        for(i in text){
            text[i] = text[i].replace(/(^\s*)|(\s*$)/g, "");
            if(text[i].length == 0){
                continue;
            } else if(text[i].length > 100){
                alert('呜呜呜，标签太长啦~');
            } else {
                var flag1 = 1;
                $("#result li").each(function () {
                    if (text[i] == $(this).text()) {
                        flag1 = 0;
                    }
                });
                if(flag1 == 1) {
                    flag = 1;
                    $("#result").append('<li><a href="javascript:void(0);" class="l"><span>' + text[i] + '</span></a></li>');
                }
            }
        }
        if(flag == 0){
            return;
        }
        $("#search_text").val('');
        var tag = '';
        $("#result li").each(function () {
            tag += $(this).text() + '&';
        });
        var cat = $("#cat > li [class='l focus']").text();
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        var sort = $("#browserTools").find("[class='l focus']").attr('id');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag : tag, cat : cat, time : time, sort : sort, page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    }

    $("#search").click(function () {
        dosearch();
    });
    $("#search_text").keydown(function (e) {
        if(e.keyCode == 13){
            dosearch();
        }
    });

    $("#browserTools a").click(function () {
        if ($(this).attr('class') == 'l focus') {
            var id = $(this).attr('id');
            id = id.split(' ');
            var tp = (parseInt(id[1]) + 1) % 2;
            id = id[0] + ' ' + tp;
            $(this).attr('id', id);
        }
        $(this).siblings().removeClass('focus');
        $(this).addClass('focus');
        var sort = $(this).attr('id');
        var tag = '';
        $("#result li").each(function () {
            tag += $(this).text() + '&';
        });
        var cat = $("#cat > li [class='l focus']").text();
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag : tag, cat : cat, time : time, sort : sort, page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });

    $("#result").on("click", 'li', function () {
        $(this).remove();
        var tag = '';
        $("#result li").each(function () {
            tag += $(this).text() + '&';
        });
        var cat = $("#cat > li [class='l focus']").text();
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        var sort = $("#browserTools").find("[class='l focus']").attr('id');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag: tag, cat: cat, time : time, sort : sort, page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });

    $("#multipage1").on("click", 'a', function () {
        if($(this).attr('class') != 'p'){
            return;
        }
        var page = $(this).text();
        var curpage = $("#multipage1 strong").text();
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part1', data : '', page : page, curpage : curpage},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                part1show(ret);
            }
        });
    });

    $("#multipage1").on('keydown','a', function (e) {
        if(e.keyCode == 13){
            var page = $("#pageinput1").val();
            $.ajax({
                type: 'POST',
                tradition: true,
                data: {part : 'part1', data : '', page : page, curpage : ''},
                beforeSend: function () {
                    scroll();
                    bgmusume_run();
                },
                success: function (ret) {
                    part1show(ret);
                }
            });
        }
    });

    $("#multipage2").on("click", 'a', function () {
        if($(this).attr('class') != 'p'){
            return;
        }
        var page = $(this).text();
        var tag = '';
        $("#result li").each(function () {
            tag += $(this).text() + '&';
        });
        var cat = $("#cat > li [class='l focus']").text();
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        var sort = $("#browserTools").find("[class='l focus']").attr('id');
        var curpage = $("#multipage2 strong").text();
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag: tag, cat: cat, time : time, sort : sort, page : page, curpage : curpage},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });

    $("#multipage2").on('keydown','a', function (e) {
        if(e.keyCode == 13){
            var page = $("#pageinput2").val();
            var tag = '';
            $("#result li").each(function () {
                tag += $(this).text() + '&';
            });
            var cat = $("#cat > li [class='l focus']").text();
            var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
            var sort = $("#browserTools").find("[class='l focus']").attr('id');
            $.ajax({
                type: 'POST',
                tradition: true,
                data: {part : 'part2', tag: tag, cat: cat, time : time, sort : sort, page : page, curpage : ''},
                beforeSend: function () {
                    scroll();
                    bgmusume_run();
                },
                success: function (ret) {
                    select_click(ret);
                }
            });
        }
    });

    $("#alltag").click(function () {
        part1();
    });

    $("#allanime").click(function () {
        $("#result").children().remove();
        $("#cat").children().children().removeClass('focus');
        $("#cat").children('li:first-child').children('a:first-child').addClass('focus');
        var pre = $("#airTimeMenu").find("[class='l focus']");
        var preid = pre.attr('id');
        pre.removeClass('focus');
        var tid = preid.split('-');
        if(tid.length == 2){
            pre.text(tid[0] + '年');
            pre.attr('id', tid[0]);
        }
        $("#timeall").addClass('focus');
        $("#browserTools").children().removeClass('focus');
        $("#browserTools").children('a:first-child').addClass('focus');
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {part : 'part2', tag: '', cat: '全部', time : 'timeall', sort : 'sortbyname 0', page : '1', curpage : ''},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                select_click(ret);
            }
        });
    });
});