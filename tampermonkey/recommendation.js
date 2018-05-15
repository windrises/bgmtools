// ==UserScript==
// @name         漫海拾贝
// @namespace    https://windrises.net
// @version      0.8
// @description  在Bangumi条目页查看相似条目，在首页查看个性化推荐条目，在个人设置页面修改设置，另外还可以查看历史推荐和好友推荐
// @author       windrises
// @run-at       document-end
// @grant        GM_xmlhttpRequest
// @connect      bangumi.brightsphere.xyz
// @require      http://code.jquery.com/jquery-1.8.3.min.js
// @include      /^(https?://bgm\.tv|http://(bgm\.tv|bangumi\.tv|chii\.in))/($|subject|user|settings|anime/list)/
// ==/UserScript==

(function() {
    var url = location.pathname;
    url = url.split("/");
    var user_name = $("#headerNeue2").find("[class='avatar']");
    var user_id = "";
    if (user_name.length == 0) user_name = "";
    else {
    	user_id = user_name.children().css("background-image");
    	user_id = user_id.substring(user_id.lastIndexOf("/") + 1, user_id.lastIndexOf(".jpg"));
    	user_name = user_name.attr("href");
    	user_name = user_name.substr(user_name.indexOf("user/") + 5);
        if (user_id == "icon") user_id = user_name;
    }
    if (url.length == 2 && url[1] == "" && user_name != "") index(user_name, user_id);
    else if (url.length == 3 && url[1] == "subject") subject(url[2]);
    else if (url.length == 4 && url[3] == "friends" && user_name == url[2]) user(user_name, user_id);
    else if (url.length == 5 && url[1] + url[2] == "animelist" && user_name == url[3]) recommended(user_name, user_id);
    else if (url.length >= 2 && url[1] == "settings" && user_name != "") settings(user_name, user_id);
})();

function index_show(ret, index_cnt) {
	if (ret.error) return;
	var html = '';
    for (var i = index_cnt * 3; i < Math.min((index_cnt + 1 ) * 3, ret.index.length); i ++) {
    	var x = ret.index[i];
		html += '<div class="mainItem" style="width:170px; margin: 5px 0px 5px 50px">' +
        '<a href="/subject/' + x.id + '" title="' + x.name + '" class="rcmdIndexTitle">' +
		'<div class="image" style="width:160px; height:220px; background:#000 url(' + x.img + ') 50%">' +
		'<div class="overlay" style="width:160px; height:220px;">' +
		'<p class="title" style="width:100px; height:50px; left:40px; top:80%">' + x.name + '</p>' +
		'</div>' +
		'</div>' +
		'</a>' +
		'</div>';
	}
	$("#featuredItems").html(html);
	$(".rcmdIndexTitle").on("mouseover", function() {
		$(this).find('p').css('top', '30%');
	});
	$(".rcmdIndexTitle").on("mouseout", function() {
		$(this).find('p').css('top', '80%');
	});
}

function index(user_name, user_id) {
    $("#prgCatrgoryFilter > li > a").click(function() {
        $("#featuredItems").hide();
        $("#prgManagerMain").show();
        $("#listWrapper").css("width", "240px");
        $("#listWrapper > div").eq(0).css("width", "240px");
        $("#listWrapper > div > div").eq(0).css("width", "240px");
	});
    $("#prgCatrgoryFilter").append('<li><a id="dailyRcmdBtn" href="javascript:void(0);">每日推荐</a></li>');
    var index_cnt = 0;
    var rcmd = '';
    $("#dailyRcmdBtn").on("click", function() {
        $("#prgCatrgoryFilter").find("[class='focus']").removeClass("focus");
        $("#dailyRcmdBtn").addClass("focus");
        $("#prgManagerMain").hide();
        var html = '<ul id="featuredItems" class="featuredItems">' +
    		'</ul>';
    	if ($("#featuredItems").length == 0) $("#prgManager").append(html);
        if ($("#featuredItems > div").length != 0) {
	        if ($("#featuredItems").is(":hidden")) $("#featuredItems").show();
	        else {
	        	index_cnt = (index_cnt + 1) % Math.floor((rcmd.index.length + 2) / 3);
	        	index_show(rcmd, index_cnt);
	        }
	    } else {
	    	$.getJSON("https://windrises.net/bgmtools/recommend/api?type=index&user_name=" + user_name + "&user_id=" + user_id, function(ret){
	    		rcmd = ret;
	    		index_show(ret, 0);
	    	});
	    }
    });
}

function subject(id) {
    $.getJSON("https://windrises.net/bgmtools/recommend/api?type=subject&id=" + id, function(ret){
        if (ret.error) {
        	Bangumi_Plus(id);
        	return;
        }
        var html = '';
        if (ret.item.length > 0) {
        	html += '<div class="subject_section">' +
		    '<a id="moreItemBtn" href="javascript:void(0);" class="more">更多推荐 »</a>' +
		    '<h2 class="subtitle">相似条目</h2>' +
		    '<div class="content_inner clearit" align="left">' +
		    '<ul class="coversSmall">' +
		    '</ul>' +
		    '</div>' +
		    '</div>';
        }
        if (ret.sub.length > 0) {
        	html += '<div class="subject_section">' +
		    '<a id="moreSubBtn" href="javascript:void(0);" class="more">更多推荐 »</a>' +
		    '<h2 class="subtitle">可能喜欢</h2>' +
		    '<div class="content_inner clearit" align="left">' +
		    '<ul class="coversSmall">' +
		    '</ul>' +
		    '</div>' +
		    '</div>';
        }
        $("#columnSubjectHomeB").find("[class='subject_section']").eq(0).after(html);
        var item_cnt = 0;
    	var sub_cnt = 0;
    	var right = new Array(8, 24, 48);
        $("#moreItemBtn").on("click", function() {
			var html = '';
			for (var i = 0; i < Math.min(right[item_cnt], ret.item.length); i ++) {
	        	var x = ret.item[i];
	        	html += '<li class="clearit">' +
				    '<a href="/subject/' + x.id + '" class="avatar thumbTip">' +
				    '<span class="avatarNeue avatarSize75" style="background-image:url(' + x.img + ')"></span>' +
				    '</a>' +
				    '<p class="info"><a href="/subject/' + x.id + '" class="l">' + x.name +'</a></p>' +
				    '</li>';
			}
	        $("#columnSubjectHomeB").find("[class='subject_section']").eq(1).find("[class=coversSmall]").html(html);
	        item_cnt = (item_cnt + 1) % 3;
	    });
	    $("#moreSubBtn").on("click", function() {
	        var html = '';
			for (var i = 0; i < Math.min(right[sub_cnt], ret.sub.length); i ++) {
	        	var x = ret.sub[i];
	        	html += '<li class="clearit">' +
				    '<a href="/subject/' + x.id + '" class="avatar thumbTip">' +
				    '<span class="avatarNeue avatarSize75" style="background-image:url(' + x.img + ')"></span>' +
				    '</a>' +
				    '<p class="info"><a href="/subject/' + x.id + '" class="l">' + x.name +'</a></p>' +
				    '</li>';
			}
	        $("#columnSubjectHomeB").find("[class='subject_section']").eq(2).find("[class=coversSmall]").html(html);
	        sub_cnt = (sub_cnt + 1) % 3;
	    });
	    $("#moreItemBtn").trigger("click");
        $("#moreSubBtn").trigger("click");
        Bangumi_Plus(id);
    });
}

function user(user_name, user_id) {
    $("#headerProfile").find("[class='focus']").parent().after('<li><a id="rcmdUserBtn" href="javascript:void(0);">好友推荐</a></li>');
    $("#rcmdUserBtn").on("click", function() {
	    $("#headerProfile").find("[class='focus']").removeClass("focus");
	    $("#rcmdUserBtn").addClass("focus");
	    $.getJSON("https://windrises.net/bgmtools/recommend/api?type=user&user_name=" + user_name + "&user_id=" + user_id, function(ret){
	        if (ret.error) return;
	        var html = '';
			for (var i in ret.user) {
	        	var x = ret.user[i];
	        	html += '<li class="user" style="width:24%">' +
				'<div class="userContainer">' +
				'<strong>' +
				'<a href="/user/' + x.user_name + '" class="avatar">' +
				'<span class="userImage">' +
				'<img src="' + x.avatar + '" class="avatar"></span> ' + x.nick_name + '</a></strong>' +
				'</div>' +
				'</li>';
			}
	        $("#memberUserList").html(html);
	    });
	});
}

function recommended(user_name, user_id) {
	$("#headerProfile").find("[class=navSubTabs]").append('<li><a id="recommendedBtn" href="javascript:void(0);"><span>历史推荐</span></a></li>');
	$("#recommendedBtn").on("click", function() {
		$("#headerProfile").find("[class='focus']").removeClass("focus");
        $("#recommendedBtn").addClass("focus");
        $("#browserTools").hide();
        $.getJSON("https://windrises.net/bgmtools/recommend/?type=recommended&user_name=" + user_name + "&user_id=" + user_id, function(ret){
	    	if (ret.error) return;
	    	var html = "";
	    	for (var i in ret.recommended) {
	    		var x = ret.recommended[i];
	    		var namechs = x.namechs;
	        	if (namechs == "") namechs = x.name;
				html += '<li class="item even clearit">' +
					'<div class="inner">' +
					'<h3>' +
					'<a href="/subject/' + x.id + '" class="l">' + namechs + '</a> <small class="grey">' + x.name + '</small>' +
					'</h3>' +
					'<p class="info tip">' +
					'推荐日期：' + x.date;
				if (x.type.id != 0) {
					html += ' / 推荐来源：' + '<a href="/subject/' + x.type.id + '">' + x.type.name + '</a>';
				}
				html += '</p></div></li>';
			}
	    	$("#browserItemList").html(html);
	    	$("#multipage").hide();
	    	$("#columnSubjectBrowserB").hide();
	    });
	});
}

function settings(user_name, user_id) {
    $("#header > ul").append('<li><a id="rcmdSetBtn" href="javascript:void(0);"><span>漫海拾贝</span></a></li>');
    $("#rcmdSetBtn").on("click", function() {
        $("#header").find("[class='selected']").removeClass("selected");
        $("#rcmdSetBtn").addClass("selected");
        $.getJSON("https://windrises.net/bgmtools/recommend/?type=settings&user_name=" + user_name + "&user_id=" + user_id, function(ret){
	    	if (ret.error) return;
	    	var score_below = "", score_above = "", rank_below = "", rank_above = "", rating_below = "", rating_above = "";
	    	if (ret.score_below) score_below = ret.score_below;
	    	if (ret.score_above) score_above = ret.score_above;
	    	if (ret.rank_below) rank_below =ret.rank_below;
	    	if (ret.rank_above) rank_above = ret.rank_above;
	    	if (ret.rating_below) rating_below = ret.rating_below;
	    	if (ret.rating_above) rating_above = ret.rating_above;
	    	var html = '<form>' +
				   '<span class="text">' +
				   '<table align="center" width="98%" cellspacing="0" cellpadding="5" class="settings">' +
				   '<tbody>' +
				   '<tr><td valign="top" width="23%"></td>' +
				   '<td valign="top"><input id="updateBtn" class="inputBtn" value="同步数据" readonly unselectable="on" style="width:53px">' +
				   '<a id="alert_update" style="color: #F09199; font-size: 14px; padding: 20px"></a></td></tr>' +
				   '<tr><td valign="top" width="23%">减少推荐分数低于<br />的条目</td>' +
				   '<td valign="top"><input id="score_below" class="inputtext" type="text" value="' + score_below + '"></td></tr>' +
				   '<tr><td valign="top" width="23%">减少推荐分数高于<br />的条目</td>' +
				   '<td valign="top"><input id="score_above" class="inputtext" type="text" value="' + score_above + '"></td></tr>' +
				   '<tr><td valign="top" width="23%">减少推荐排名低于<br />的条目</td>' +
				   '<td valign="top"><input id="rank_below" class="inputtext" type="text" value="' + rank_below + '"></td></tr>' +
				   '<tr><td valign="top" width="23%">减少推荐排名高于<br />的条目</td>' +
				   '<td valign="top"><input id="rank_above" class="inputtext" type="text" value="' + rank_above + '"></td></tr>' +
				   '<tr><td valign="top" width="23%">减少推荐评分人数低于<br />的条目</td>' +
				   '<td valign="top"><input id="rating_below" class="inputtext" type="text" value="' + rating_below + '"></td></tr>' +
				   '<tr><td valign="top" width="23%">减少推荐评分人数高于<br />的条目</td>' +
				   '<td valign="top"><input id="rating_above" class="inputtext" type="text" value="' + rating_above + '"></td></tr>' +
				   '<tr><td valign="top" width="23%">过滤掉含有<br />标签的条目</td>' +
				   '<td valign="top"><input id="filter_tag" class="inputtext" type="text" placeholder="空格分割" value="' + ret.filter_tag + '"></td></tr>' +
				   '<tr><td valign="top" width="23%"></td>' +
				   '<td valign="top"><input id="submitBtn" class="inputBtn" value="确定" readonly unselectable="on" style="width:26px">' +
				   '<a id="alert_submit" style="color: #F09199; font-size: 14px; padding: 20px"></a></td></tr>' +
				   '</tbody></table>' +
				   '</span>' +
				   '</form>';
        	$("#columnA").html(html);
        	$("input[readonly]").on('focus', function() {
			    $(this).trigger('blur');
			});
        	$("#updateBtn").on("click", function() {
	        	$.ajax({
	        		url: "https://windrises.net/bgmtools/recommend",
		            type: "POST",
		            tradition: true,
		            data: {type: "settings_update", user_name: user_name, user_id: user_id},
		            success: function (ret) {
		            	ret = JSON.parse(ret);
		            	$("#alert_update").html(ret.status);
		            }
	        	});
	        });
	        $("#submitBtn").on("click", function() {
	        	var score_below = $("#score_below").attr("value");
	        	var score_above = $("#score_above").attr("value");
	        	var rank_below = $("#rank_below").attr("value");
	        	var rank_above = $("#rank_above").attr("value");
	        	var rating_below = $("#rating_below").attr("value");
	        	var rating_above = $("#rating_above").attr("value");
	        	var filter_tag = $("#filter_tag").attr("value");
	        	if (score_below == "") score_below = 0;
	        	if (score_above == "") score_above = 0;
	        	if (rank_below == "") rank_below = 0;
	        	if (rank_above == "") rank_above = 0;
	        	if (rating_below == "") rating_below = 0;
	        	if (rating_above == "") rating_above = 0;
	        	$.ajax({
	        		url: "https://windrises.net/bgmtools/recommend",
		            type: "POST",
		            tradition: true,
		            data: { type: "settings_submit", user_name: user_name, user_id: user_id,
		            		score_below: score_below, score_above: score_above,
		            		rank_below: rank_below, rank_above: rank_above,
		            		rating_below: rating_below, rating_above: rating_above,
		            		filter_tag: filter_tag},
		            success: function (ret) {
		            	ret = JSON.parse(ret);
		            	$("#alert_submit").html(ret.status);
		            }
	        	});
	        });
	    });
    });
}

// from http://bgm.tv/group/topic/345713
function Bangumi_Plus(id) {
    'use strict';

    GM_request(`https://bangumi.brightsphere.xyz/api/subjects/${id}/`).then(JSON.parse).then(data => {
        let subjects = '';
        for (let i in data.recommendations) {
            let rmd = data.recommendations[i];
            let subtitle = '';
            if (rmd.auto) {
                continue;
            } else {
                subtitle = `${rmd.count}人推荐`;
            }
            let subject = rmd.subject;
            subjects += `<li>
						<span class="sub">${subtitle}</span>
						<a href="https://bangumi.brightsphere.xyz/recommendation/${rmd.key}" title="查看详情" class="avatar thumbTip"><span class="avatarNeue avatarSize75" style="background-image:url('${subject.cover.replace('http:','')}')"></span></a>
						<a href="/subject/${subject.id}" class="title">${subject.main_name}</a>
						</li>`;
        }
        let block = `<div class="subject_section">
					<div class="clearit">
					<div class="rr"><a href="https://bangumi.brightsphere.xyz/subject/${id}" class="chiiBtn"><span>关联推荐</span></a></div>
					<h2 class="subtitle">相关推荐</h2>
					</div>
					<div class="content_inner">
					<ul class="browserCoverMedium clearit">${subjects}</ul>
					</div>
					</div>`;
        $(".subject_section > .subtitle:contains('评论')").parent().before(block);
    });
    function GM_request(url, responseType, method) {
	    return new Promise(function(resolve, reject) {
	        GM_xmlhttpRequest({
	            method: method || 'GET',
	            url,
	            responseType,
	            onload: xhr => {
	                if (xhr.status >= 200 && xhr.status < 300) {
	                    resolve(xhr.response);
	                } else {
	                    reject(xhr);
	                }
	            },
	            onerror: xhr => {
	                reject(xhr);
	            }
	        });
	    });
	}
}
