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
                var flag = 0;
                if (pre.length != 0) {
                    var preid = pre.attr('id');
                    var tid = preid.split('-');
                    if (baseId == preid && tid.length == 2) {
                        flag = 1;
                        baseId = tid[0];
                        ul.append($("<li>").append($("<a>").text('全年').attr('id', baseId).attr('href', 'javascript:void(0);')));
                        var premonth = parseInt(tid[1]);
                        for (var i = 1; i < 13; i++) {
                            if (i != premonth)
                                ul.append($("<li>").append($("<a>").text(i + '月').attr('id', baseId + '-' + i).attr('href', 'javascript:void(0);')));
                        }
                    }
                }
                if (flag == 0) {
                    for (var i = 1; i < 13; i++)
                        ul.append($("<li>").append($("<a>").text(i + '月').attr('id', baseId + '-' + i).attr('href', 'javascript:void(0);')));
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
    var interval = '';
    function bgmusume() {
        if(interval != ''){
            clearInterval(interval);
            interval = '';
        }
        var rand = 1 + Math.floor(Math.random()*6);
        $("#bgmusume").attr('class', 'bg musume_' + rand);
        $("#bgmusume").css("background-position", -40 * (rand - 1) + 'px ' + 0 + 'px');
    }
    function bgmusume_run() {
        var pos = 0;
        var speed = -10;
        function move() {
            if(pos <= -240) pos = 0;
            $("#bgmusume").css("background-position", pos + 'px ' + 0 + 'px');
            pos = pos + speed;
        }
        interval = setInterval(move, 120);
    }
    function scroll() {
        window.scrollBy(0, -120);
        var scrolldelay = setTimeout(scroll, 10);
        var sTop = document.documentElement.scrollTop + document.body.scrollTop + window.pageYOffset;
        if(sTop <= 0) clearTimeout(scrolldelay);
    }

    var global_time = "last";
    var url = location.search;
    if (url.indexOf('?') != -1) {
        url = url.substr(1);
        url = url.split("&");
        var time = "", sort = "", page = "";
        var flag = 1;
        for (var x in url) {
            x = url[x].split("=");
            if (x.length != 2) {
                flag = 0;
                break;
            }
            if (x[0] == "time") time = x[1];
            else if (x[0] == "sort") sort = x[1];
            else if (x[0] == "p") page = x[1];
            else {
                flag = 0;
                break;
            }
        }
        if (time == "") time = "now";
        if (sort == "") sort = "name-0";
        if (page == "") page = "1";
        if (flag == 0) alert("请求出错");
        else {
            global_time = time;
            if (run(time, sort, page, '', 2) == 1){
                $("#browserTools").find("[class='l focus']").removeClass('focus');
                var type = $("#browserTools").find("[name='"+ sort +"']");
                if (type.length == 0) {
                    var tsort = sort.split("-");
                    var tsort = tsort[0] + "-" + (parseInt(tsort[1]) + 1) % 2;
                    $("#browserTools").find("[name='"+ tsort +"']").attr("name", sort);
                }
                $("#browserTools").find("[name='"+ sort +"']").addClass('focus');
            }
        }
    }
    $(".part2").hide();
    $(".part1").show();
    bgmusume();
    chiiLib.airTimeMenu.init();

    $("#airTimeMenu").on('click', 'a', function () {
        var id = $(this).attr('id');
        var pre = $("#airTimeMenu").find("[class='l focus']");
        var tid = '';
        if (pre.length != 0) {
            var preid = pre.attr('id');
            if(id == preid) return;
            pre.removeClass('focus');
            tid = preid.split('-');
            if(tid.length == 2){
                pre.text(tid[0] + '年');
                pre.attr('id', tid[0]);
            }
        }
        if(id == 'now'){
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
        var sort = $("#browserTools").find("[class='l focus']").attr('name');
        run(id, sort, '1', '', 1);
    });

    $("#browserTools a").click(function () {
        if ($(this).attr('class') == 'l focus') {
            var name = $(this).attr('name');
            name = name.split('-');
            var tp = (parseInt(name[1]) + 1) % 2;
            name = name[0] + '-' + tp;
            $(this).attr('name', name);
        }
        $(this).siblings().removeClass('focus');
        $(this).addClass('focus');
        var sort = $(this).attr('name');
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        run(time, sort, '1', '', 1);
    });

    $("#multipage").on("click", 'a', function () {
        if($(this).attr('class') != 'p') return;
        var page = $(this).text();
        var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
        var sort = $("#browserTools").find("[class='l focus']").attr('name');
        var curpage = $("#multipage strong").text();
        run(time, sort, page, curpage, 1);
    });

    $("#multipage").on('keydown','a', function (e) {
        if(e.keyCode == 13){
            var page = $("#pageinput2").val();
            var time = $("#airTimeMenu").find("[class='l focus']").attr('id');
            var sort = $("#browserTools").find("[class='l focus']").attr('name');
            run(time, sort, page, '', 1);
        }
    });
    if (history && history.pushState) {
        $(window).bind("popstate", function() {
            location.reload();
        });
    }

    function run(time, sort, page, curpage, type) {
        if (time == undefined)
            time = global_time;
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {time: time, sort: sort, page: page, curpage: curpage},
            beforeSend: function () {
                scroll();
                bgmusume_run();
            },
            success: function (ret) {
                if (ret.error != undefined) {
                    bgmusume();
                    alert("请求出错");
                    return 0;
                }
                select_click(ret);
                if (history && type == 1){
                    var path = "time=" + time + "&sort=" + sort + "&p=" + ret.page;
                    history.pushState({}, "", location.pathname + "?" + path);
                }
            }
        });
        return 1;
    }

    function pageshow(page, maxpage) {
        page = parseInt(page);
        maxpage = parseInt(maxpage);
        var str = '';
        var start = page - 2;
        var end = page + 7;
        if(start < 1) start = 1;
        if(end > maxpage) end = maxpage;
        if(page > 3)
            str += '<a href="javascript:void(0);" class="p">|‹</a>';
        if(page > 1)
            str += '<a href="javascript:void(0);" class="p">‹‹</a>';
        for(var i = start; i < page; i ++)
            str += '<a href="javascript:void(0);" class="p">' + i + '</a>';
        str += '<strong class="p_cur">' + page + '</strong>';
        for(var i = page + 1; i <= end; i ++)
            str += '<a href="javascript:void(0);" class="p">' + i + '</a>';
        if(page < maxpage)
            str += '<a href="javascript:void(0);" class="p">››</a>';
        if(page < maxpage - 7)
            str += '<a href="javascript:void(0);" class="p">›|</a>';
        str += '<a class="p_pages" style="padding: 0">\
                <input id="pageinput1" class="inputtext" style="width:30px;" type="text" name="custompage"></a>';
        str += '<span class="p_edge">(&nbsp;' + page + '&nbsp;/&nbsp;' + maxpage + '&nbsp;)</span>';
        str = str.replace('pageinput1', 'pageinput2');
        $("#multipage").html(str);
    }

    function select_click(ret) {
        bgmusume();
        $(".part1").hide();
        $(".part2").show();
        var str = '';
        for (var i in ret.data) {
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
            <ul class="collectMenu">\
            <li>\
            <a target="_blank" href="/bgmtools/review/chart/?id=' + x['id'] +'" title="查看 ' + x['namejp'] + ' 评分走势图" class="collect_btn chiiBtn thickbox"><span>查看</span></a>\
            </li>\
            </ul>\
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
        pageshow(ret.page, ret.maxpage);
    }

});
