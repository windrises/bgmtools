// ==UserScript==
// @name         Bangumi时光机
// @namespace    https://windrises.net
// @version      0.1
// @description  在Bangumi条目页使用，用于查看条目评分走势
// @author       windrises
// @require      http://code.jquery.com/jquery-1.8.3.min.js
// @require      http://code.highcharts.com/highcharts.js
// @require      http://code.highcharts.com/modules/exporting.js
// @include      /^(https?://bgm\.tv|http://(bgm\.tv|bangumi\.tv|chii\.in))/subject/\d*($|/ep|/characters|/persons|/comments.*|/reviews|/board)
// ==/UserScript==

(function() {
    $("#headerSubject").find("[class='navTabs clearit']").append("<li><a id='subject_review' href='javascript:void(0);'>评分走势</a></li>");
    var url = location.pathname;
    url = url.split('/');
    var id = url[2];
    $("#subject_review").click(function(){
        var html = '<div id="columnInSubjectA" class="column">' +
                   '<div id="score_chart" style="width:740px;height:420px"></div>' +
                   '</div>' +
                   '<div id="columnInSubjectB" class="column">' +
                   '<div class="menu_inner">' +
                   '<a href="/subject/' + id + '" class="l">/ 返回条目页面</a>' +
                   '</div>' +
                   '<div class="menu_inner">' +
                   '<a href="https://windrises.net/bgmtools/review?id=' + id + '" class="l" target="_blank">/ 查看详情</a>' +
                   '</div>' +
                   '</div>' +
                   '</div>';
        var error_html = '<h2>出错了</h2>' +
                         '<p class="text">该条目暂时还未收录</p>';
        $("#wrapperNeue").find("[class='columns clearit']").html(html);
        $("#headerSubject").find("[class='focus']").removeClass("focus");
        $("#subject_review").addClass("focus");
        $.getJSON("https://windrises.net/bgmtools/review/chart/api?id=" + id, function(ret){
            if (ret.error){
                $("#columnInSubjectA").html(error_html);
            }else {
                show_chart(ret);
            }
        });
    });
})();

function call(a){}

function show_chart(data) {
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
            opposite: true
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