charset="utf-8";
var amz668 = window.myfunction;
amz668 = {
    "deleteSuperUrl":function(obj){
      $(obj).closest("tr").addClass(function(){
          return "slideRemove";
      });
       setTimeout(function() {
           $(obj).closest("tr").remove();
       }, 1005);
      layer.msg("删除成功！");
    },
    "copySuperUrl":function(obj){
      var _text = $(obj).attr("data-url");
      this.copyTextToClipboard(_text);
    },
    "copyTextToClipboard":function(text) {
      var input = document.createElement("input");
      input.style.position = 'fixed';
      input.style.top = 0;
      input.style.left = 0;
      input.style.width = '2em';
      input.style.height = '2em';
      input.style.padding = 0;
      input.style.border = 'none';
      input.style.outline = 'none';
      input.style.boxShadow = 'none';
      input.style.background = 'transparent';
      input.value = text;
      document.body.appendChild(input);
      input.select();
      try {
        var successful = document.execCommand('copy');
        var msg = successful ? '成功复制，可前往贴粘。' : '复制失败';
        layer.msg(msg);
      } catch (err) {
        layer.msg('复制失败！！');
      }
      document.body.removeChild(input);
    },
    "deleteInventory":function(obj){
      var data = $(obj).attr("data");
      layer.confirm('确定删除该Asin（'+ data +'）吗？', {
        anim: 3,
        shade: .1,
        btn: ['确定','取消']
      }, function(){
        $(obj).attr("href",$(obj).attr("data-href"));
        console.log( $(obj).attr("href"));
        $(obj).closest(".user").addClass(function(){
            return "flipOutRemove";
        });
        setTimeout(function(){
          $.get($(obj).attr("data-href"),{},function(){
            console.log("successful");
          });
        },1510);
        layer.msg('删除成功！', {icon: 1});
      }, function(){
         time: 20
      });
    },
    "refreshInventory":function(){
      layer.msg("刷新成功！",{icon:1});
    },
     "renewalInventory":function(){
      layer.msg("续期成功！",{icon:1});
    },
    "viewInventory":function(id){
      layer.open({
        type: 1,
        area: ['700px', '300px'],
        title: ' ',
        shade: .7,
        shadeClose:true,
        maxmin: true,
        anim: 1,
        content: $("#id_"+id)
      });
    },
    "tab":function(obj,peer,tabCon,Class){
        $(obj).children().click(function(){
          var index = $(obj).children().index(this);
          $(this).addClass(Class).siblings(peer).removeClass(Class);
          $(tabCon).eq(index).stop(false,true).slideDown(500).siblings(tabCon).slideUp(500);
        });
      return this;
    },
    "getSetSelectIndex":function(){
      get = function(){
        var index = $("#id_country").get(0).selectedIndex;
        sessionStorage.setItem("select_index",index);
        sessionStorage.setItem("href",document.location.href);
        console.log(index);
        console.log(document.location.href);
      };
      set = function(){
        var _index = sessionStorage.getItem("select_indexs");
        var _href = sessionStorage.getItem("href");
        var thisHref = document.location.href;
        if(_index && (_href === thisHref)){
            $("#id_country").get(0).selectedIndex = _index;
        }
      };
      set();
      return this;
    },
    "common":function(){
      //首页过渡效果
      // mot = function(){
      //    var fade = {transform: 'translateY(0)',opacity: 1};
      //    $("#main_body").css(fade);
      //    return this;
      // },
      indexSeeMore = function(){
        $(".l_text").click(function(){
          if($(this).data("flag")){
            $(this).siblings(".line").show();
            $(this).parent().siblings(".div_hide").stop(false,true).fadeOut("slow");
            $(this).data("flag",false);
          }else{
            $(this).siblings(".line").hide();
            $(this).parent().siblings(".div_hide").stop(false,true).fadeIn("slow");
            $(this).data("flag",true);
          }
        });
        return this;
      },
      goTop = function(min_height){
        var gotoTop_html = '<div id="gotoTop" title="回到顶部" style="display:none;position: fixed;top: 80%;right: 3%;cursor: pointer;width: 50px;height: 50px;bordre:10px solid #f00; background: url(http://www.amz668.com/static/images/ToTop.png) no-repeat;background-size: cover;"></div>';
        $("body").append(gotoTop_html);
        $("#gotoTop").click(function(){$('html,body').animate({scrollTop:0},700);});
        min_height ? min_height = min_height : min_height = 600;
        $(window).scroll(function(){
          if($(window).scrollTop() > min_height){
              $("#gotoTop").slideDown(500);
          }else{
              $("#gotoTop").slideUp(500);
          };
        });
        return this;
      },
      google = function(){
        document.searchForm.action = "https://www.google.com.hk/search?";
        document.getElementById("search_keyword").name ="q";
        document.searchForm.submit();
        document.searchForm.action = "http://www.baidu.com/s";
        document.getElementById("search_keyword").name ="wd";
      },
      closeMessage = function(){
        $(".close").click(function(){
          $(this).parent().parent(".messages").remove();
        });
        return this;
      },
      addSourceForLink = function(){
        $("#main_body a").each(function(i,c){
          this.search ? this.search = this.search + "&utm_source=amz668.com": this.search = "?utm_source=amz668.com";
        });
        return this;
      },
      getTheTime = function(){
        Date.prototype.format = function(format){
          var o={
            "M+":this.getMonth()+1,
            "d+":this.getDate(),
            "h+":this.getHours(),
            "m+":this.getMinutes(),
            "s+":this.getSeconds(),
            "q+":["\u6625","\u590f","\u79cb","\u51ac"][Math.floor((this.getMonth()+3)/3)-1],
            "S":this.getMilliseconds(),
            "W":["\u4e00","\u4e8c","\u4e09","\u56db","\u4e94","\u516d","\u65e5"][(this.getDay()==0)?6:this.getDay()-1]
          };
          if(/(y+)/.test(format)){
            format=format.replace(RegExp.$1,(this.getFullYear()+"").substr(4-RegExp.$1.length));
          };
          for(var k in o){
            if(new RegExp("("+k+")").test(format)){
              format=format.replace(RegExp.$1,RegExp.$1.length==1?o[k]:("00"+o[k]).substr((""+o[k]).length));
            }
          };
          return format;
        };
        calcTime = function(bj_time,timeOffset){
          var utctime = bj_time.getTime() + (bj_time.getTimezoneOffset() * 60000);
          var dataTime = new Date(utctime + (3600000*timeOffset));
          return dataTime;
        };
        getTimes = function(){
          var bj_time = new Date();
          $("#us").html(calcTime(bj_time,-4).format("MM-dd hh:mm:ss"));
          $("#wa").html(calcTime(bj_time,-7).format("MM-dd hh:mm:ss"));
          $("#fr").html(calcTime(bj_time,2).format("MM-dd hh:mm:ss"));
          $("#es").html(calcTime(bj_time,2).format("MM-dd hh:mm:ss"));
          $("#it").html(calcTime(bj_time,2).format("MM-dd hh:mm:ss"));
          $("#littleJapan").html(calcTime(bj_time,9).format("MM-dd hh:mm:ss"));
          $("#uk").html(calcTime(bj_time,1).format("MM-dd hh:mm:ss"));
          $("#de").html(calcTime(bj_time,2).format("MM-dd hh:mm:ss"));
        };
        setInterval("getTimes()",1000);
        return this;
      },
      addFavorite = function(){
        if (window.sidebar && window.sidebar.addPanel) {
          window.sidebar.addPanel(document.title, window.location.href, '');
        } else if (window.external && ('AddFavorite' in window.external)) {
          window.external.AddFavorite(location.href, document.title);
        } else if (window.opera && window.print) {t
          this.title = document.title;
          return true;
        } else {
          alert('您的浏览器不支持此操作,请按 ' + (navigator.userAgent.toLowerCase().indexOf('mac') != -1 ? 'Command/Cmd' : 'Ctrl') + ' + D 手动收藏.');
        }
        return this;
      },
      submitForm = function(){
        $('#log_form').submit(function(event) {
          event.preventDefault();
          $('#gif').css('display', 'block');
        });
        return this;
      };
      submitForm();
      indexSeeMore().goTop(100).closeMessage().addSourceForLink().getTheTime();
      return this;
    },
    doAjax: function (){
      // st
      $("#st").click(function(e){
        if(!$('#id_asin').val().trim()){
          return;
        }
        var params = {
          'asin': $('#id_asin').val().trim(),
          'country': $('#id_country option:selected').val()
        };
        $.ajax({
          url: 'create_post/',
          type: 'POST',
          dataType:'json',
          data: params,
          success: function(data) {
              $('#result').empty();
              $('#id_asin').val('');

              if(data.keyword){$('#result').append(
              "<td>"+ data.country +"</td>"+
              "<td><img src='"+ data.img +"' width='70'></td>"+
              "<td><a href='"+ data.url +"' target=\"_blank\">" + data.asin + "</a></td>"+
              "<td>"+ data.title +"</td>"+
              "<td>"+ data.keyword + "</td>");}

              else {$('#result').append(
              "<td>"+ data.country +"</td>"+
              "<td><img src='"+ data.img +"' width='70'></td>"+
              "<td><a href='"+ data.url +"' target=\"_blank\">" + data.asin + "</a></td>"+
              "<td>"+ data.title +"</td>"+
              "<td></td>");}

              $('#gif').css('display', 'none');
              if(data.title){$("#resultDiv").show();}
              $("#st").removeAttr("disabled");
              if(data.response){alert(data.response);}
          },
          error: function(err) {
            layer.msg("请求出错了！请换个浏览器重试！");
          }
        });
      });

     //库存
    //$("#inven").click(function(){
    //  if(!$('#id_asin').val().trim()){
    //   return;
    //   }
    //   var params = {
    //   'asin': $('#id_asin').val().trim(),
    //   'country': $('#id_country option:selected').val()
    //   };
    //   $.ajax({
    //    url: 'create_post/',
    //       type: 'POST',
    //       data: params,
    //   success: function(data) {
    //       $('#result').empty();
    //       $('#id_asin').val('');
    //       if(data.response){alert(data.response);}
    //       var action = "";
    //       if(data.inventory_to_user){ action = "<span>正在跟踪竞品信息</span>";}
    //       else {action = "<a href='javascript:;'"+" data-id="+ data.id +" data-action='add_monitor'  class='add_monitor add_btn' >添加到跟踪竞品 </a>";}
//
    //    $('#result').append(
    //     "<td align='center'><img src='"+ data.img +"' width=70 > &emsp;"+ data.asin +"</td>"+
    //       "<td align='center'>"+ data.title+"</td>"+
    //        "<td align='center'>"+data.inventory+"</td>"+
    //         "<td align='center'>"+data.bsr_rank+"</td>"+
    //       "<td align='center'>"+data.price+"</td>"+
    //          "<td align='center'>"+action+"</td>");
//
    //          $('#gif').css('display', 'none');
            //debugger;
    //          if(data.title){$("#resultDiv").show();}
    //          $("#inven").removeAttr("disabled");
    //       },
    //       error: function(err) {
    //        layer.msg("请求出错了！请重试。");
    //       }
    //     });
    //});
    },

};
amz668.getSetSelectIndex().common().tab(".amz_country","li",".amzCon","active");

  // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

$("#closeone,#closetwo").click(function(){
    $(".attention.one,.two").fadeOut("slow");
});
$("#closethree").click(function(){
    $(".attention.three").fadeOut("slow");
});
$("#scrollTop").click(function(){
    $(document.body).animate({scrollTop:$(document.body).offset().top},1000);
});

// var flag = false;
// $(".l_text").click(function(){
//     if(flag){
//         $(this).siblings(".line").show();
//         //$(this).parent().parent("li").next("li").css("border-top","none");
//         $(this).parent().siblings(".div_hide").stop(false,true).fadeOut("slow");
//         flag = false;
//     }else{
//         //console.log($(this).parent());
//         $(this).siblings(".line").hide();
//        //$(this).parent().parent("li").next("li").css("border-top","1px solid #ccc");
//         $(this).parent().siblings(".div_hide").stop(false,true).fadeIn("slow");
//         flag = true;
//     }
// });

