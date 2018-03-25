$(document).ready(function () {
    var path = location.pathname.split('/');
    if (path[path.length - 1] != "api"){
        var url = location.search;
        if (url.indexOf('?') != -1) {
            url = url.substr(1);
            url = url.split("&");
            var id = "", rank = "", period = "", check = "", cat = "";
            var flag = 1;
            for (var x in url) {
                x = url[x].split("=");
                if (x.length != 2) {
                    flag = 0;
                    break;
                }
                if (x[0] == "id") id = x[1];
                else if (x[0] == "rank") rank = x[1];
                else if (x[0] == "period") period = x[1];
                else if (x[0] == "check") check = x[1];
                else if (x[0] == "category") cat = x[1];
                else{
                    flag = 0;
                    break;
                }
            }
            if (check == "") check = 'true';
            if (cat == "") cat = 'anime';
            if (check != "true" && check != "false") flag = 0;
            if (flag == 0) $("#alert").text("请求出错");
            else {
                run(id, rank, period, check, cat, 2);
                $("#check").attr("checked", check);
            }
        }
    }
    $(".part2").hide();
    $(".part1").show();
    bgmusume();

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
    if (history && history.pushState) {
        $(window).bind("popstate", function() {
            location.reload();
        });
    }

    function input_split(input) {
        input = input.replace(/(^\s+)|(\s+$)/g, "").replace(/\s+/g, " ");
        input = input.replace(/(\r\n)+/g, "|").replace(/\n+/g, "|").replace(/\s+/g, "|");
        return input;
    }
    $("#history_submit").click(function () {
        var id = $("#id_input").val();
        id = input_split(id);
        if (id != "") {
            var tid = id.split("|");
            id = "";
            for (var i in tid) {
                if (tid[i] != "") {
                    id += "|" + tid[i].substring(tid[i].lastIndexOf("/") + 1);
                }
            }
            id = id.substring(1);
        }
        var rank = $("#rank_input").val();
        rank = input_split(rank);
        var period = $("#period_input").val();
        period = input_split(period);
        var check = $("#check").is(":checked");
        var cat = $("#review_select").find("[selected='selected']").attr("value");
        run(id, rank, period, check, cat, 1);
    });

    function run(id, rank, period, check, cat, type) {
        if (id.length == 0 && rank.length == 0) {
            $("#alert").text("你还没有指定条目呢");
            return;
        } else if (id.length > 0 && rank.length > 0) {
            $("#alert").text("条目和名次检索只能选择一个哦");
            return;
        }
        $.ajax({
            type: 'POST',
            tradition: true,
            data: {id: id, rank: rank, period: period, check: check, category: cat},
            beforeSend: function () {
                bgmusume_run();
            },
            success: function (ret) {
                if (ret.error != undefined) {
                    $("#alert").text(ret.error);
                    bgmusume();
                    return;
                }
                $(".part1").hide();
                $(".part2").show();
                $("#alert").text("");
                if (history && type == 1){
                    var path = "";
                    if (id != "") path += "id=" + id;
                    if (rank != "") path += "category=" + cat + "&rank=" + rank;
                    if (period != "") path += "&period=" + period;
                    if (check == false) path += "&check=false";
                    history.pushState({}, "", location.pathname + "?" + path);
                }
                if (ret.type == 1) {
                    $('#multi-score_chart').hide();
                    $('#multi-rank_chart').hide();
                    $('#multi-people_chart').hide();
                    show_chart1(ret.data);
                } else {
                    $('#score_chart').hide();
                    show_chart2('multi-score_chart', '评分对比图', '分数', ret.data.score);
                    show_chart2('multi-rank_chart', '排名对比图', '名次', ret.data.rank);
                    show_chart2('multi-people_chart', '标记人数对比图', '人数', ret.data.people);
                }
                bgmusume();
            }
        });
    }

    function show_chart1(data) {
        $('#score_chart').show();
        $('#score_chart').highcharts({
            chart: {
                zoomType: 'xy'
            },
            title: {
                text: data.name + ' 评分走势图'
            },
            subtitle: {
                text: ''
            },
            xAxis: [{
                categories: data.time,
                crosshair: true
            }],
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                title: {
                    text: '分数',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                }
            }, { // Secondary yAxis
                gridLineWidth: 0,
                title: {
                    text: '名次',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                opposite: true,
                reversed: true
            }, { // Tertiary yAxis
                gridLineWidth: 0,
                title: {
                    text: '人数',
                    style: {
                        color: Highcharts.getOptions().colors[2]
                    }
                },
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[2]
                    }
                },
                opposite: true
            }],
            tooltip: {
                shared: true
            },
            legend: {
                // layout: 'vertical',
                align: 'left',
                x: 20,
                verticalAlign: 'top',
                y: 5,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
            },
            series: [{
                name: '评分',
                type: 'spline',
                yAxis: 0,
                data: data.score,
                tooltip: {
                    valueSuffix: ''
                }
            }, {
                name: '排名',
                type: 'spline',
                yAxis: 1,
                data: data.rank,
                marker: {
                    enabled: false
                },
                // dashStyle: 'shortdot',
                tooltip: {
                    valueSuffix: ''
                }
            }, {
                name: '标记人数',
                type: 'spline',
                yAxis: 2,
                data: data.people,
                tooltip: {
                    valueSuffix: ''
                }
            }],
            credits: {
                text: 'windrises.net',
                href: 'https://windrises.net'
            }
        });
    }

    function show_chart2(name, title, titley, data) {
        $("#" + name).show();
        var series = [];
        for (var i in data) {
            var series_data = [];
            for (var j in data[i].data) {
                var time = data[i].data[j][0];
                time = time.split('-');
                time = Date.UTC(parseInt(time[0]), parseInt(time[1]) - 1, parseInt(time[2]));
                series_data.push([time, data[i].data[j][1]]);
            }
            series.push({name: data[i].name, data: series_data});
        }
        var point = '4';
        if (titley != "分数") point = '0';
        var reversed = false;
        if (titley == "名次") reversed =true;
        var chart = Highcharts.chart(name, {
            chart: {
                type: 'spline'
            },
            title: {
                text: title
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                type: 'datetime',
                title: {
                    text: null
                }
            },
            yAxis: {
                title: {
                    text: titley
                },
                min: 0,
                reversed: reversed
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%b%e日}: {point.y:.' + point + 'f}'
            },
            plotOptions: {
                spline: {
                    marker: {
                        enabled: true
                    }
                }
            },
            series: series,
            credits: {
                text: 'windrises.net',
                href: 'https://windrises.net'
            }
        });
    }
});
