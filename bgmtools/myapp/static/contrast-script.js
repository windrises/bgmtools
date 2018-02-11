$(document).ready(function () {
    var path = location.pathname.split('/');
    path = path[path.length - 1];
    if (path != "") {
        var url = location.search;
        var cat = "", id1 = "", id2 = "";
        var flag = 1;
        if (path.indexOf("@") != -1) {
            cat = path.substring(0, path.indexOf("@"));
            path = path.substring(path.indexOf("@") + 1);
            path = path.split("&");
            if (path.length != 2) flag = 0;
            else {
                id1 = path[0];
                id2 = path[1];
            }
        } else if (url.indexOf("?") != -1) {
            url = url.substr(1);
            url = url.split("&");
            for (var x in url) {
                x = url[x].split("=");
                if (x.length != 2) {
                    flag = 0;
                    break;
                }
                if (x[0] == "category") cat = x[1];
                else if (x[0] == "id1") id1 = x[1];
                else if (x[0] == "id2") id2 = x[1];
                else {
                    flag = 0;
                    break;
                }
            }
        }
        if (cat != "anime" && cat != "book" && cat != "music" && cat != "game" && cat != "real")
            cat = "anime";
        if (flag == 0) alert("请求出错");
        else {
            run(cat, id1, id2);
        }
    }

    bgmusume();

    var interval = '';

    function bgmusume() {
        if (interval != '') {
            clearInterval(interval);
            interval = '';
        }
        var rand = 1 + Math.floor(Math.random() * 6);
        $("#bgmusume").attr('class', 'bg musume_' + rand);
        $("#bgmusume").css("background-position", -40 * (rand - 1) + 'px ' + 0 + 'px');
    }
    function bgmusume_run() {
        var pos = 0;
        var speed = -10;

        function move() {
            if (pos <= -240) pos = 0;
            $("#bgmusume").css("background-position", pos + 'px ' + 0 + 'px');
            pos = pos + speed;
        }

        interval = setInterval(move, 120);
    }

    if (history && history.pushState) {
        $(window).bind("popstate", function () {
            location.reload();
        });
    }

    function run(cat, id1, id2) {
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {cat: cat, id1: id1, id2: id2},
            beforeSend: function () {
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

});
