(function() {
    var a = {
        showWxRec: function(e, f) {
            layer.open({
                type: 1,
                shadeClose: true,
                title: "微信公众号",
                area: ["300px"],
                content: '<div style="padding:12px"><img src="' + e + '" width="200px" height="200px" style="margin:0 auto;"><p style="font-size: 14px; letter-spacing: 1px;">' + f + "</p></div>"
            })
        },
        showWeixinMessage: function(e) {
            layer.open({
                type: 1,
                title: "获取方式",
                area: ["300px", "280px"],
                content: '<div><img src="images/longxuanweixin.jpg" width="200px" height="200px" style="margin:0 auto;"><p style="text-align:center; font-size: 14px;">关注微信公众号，回复关键词：<span style="color:red;">' + e + "</span></p></div>"
            })
        },
        showDetailSites: function(e, f) {
            layer.open({
                type: 1,
                shadeClose: true,
                area: ["420px"],
                title: f,
                content: e
            })
        }
    };
    var d = {
        form: {
            siteName: ["麦克CRM", "番茄表单", "金数据", "腾讯问卷", "问卷星"],
            sites: ["http://www.mikecrm.com/", "https://fanqier.cn/", "https://jinshuju.net/", "https://wj.qq.com/", "https://www.sojump.com/"]
        },
        compressjpg: {
            siteName: ["美图秀秀网页版", "图丫丫", "ps在线版", "iLoveImg", "Editor.Pho.to", "图片识别为文字", "tinypng", "图好快", "optimizilla", "色彩笔", "贴图库-图片外链"],
            sites: ["http://xiuxiu.web.meitu.com/main.html", "http://www.tuyaya.com/", "http://www.uupoop.com/", "http://www.iloveimg.com/zh_cn", "http://editor.pho.to/zh/edit/", "http://www.onlineocr.net/", "https://tinypng.com/", "http://www.tuhaokuai.com/", "http://optimizilla.com/zh/", "http://www.secaibi.com/tools/", "http://www.tietuku.com/upload"]
        },
        pdftools: {
            siteName: ["Smallpdf", "iLovePDF", "迅捷PDF转换器", "pdf to word", "pdf to anything", "在线pdf转换器"],
            sites: ["https://smallpdf.com/cn", "http://www.ilovepdf.com/zh_cn", "http://app.xunjiepdf.com/", "http://www.convertpdftoword.net/", "http://pdf2doc.com/zh/", "http://www.pdf2go.com/zh/"]
        },
        giftools: {
            siteName: ["GIF搜索", "GIF编辑", "视频转GIF", "GIF压缩", "GIF裁剪", "GIf制作"],
            sites: ["http://soogif.com/", "http://www.soogif.com/editor", "http://soogif.com/video", "http://www.soogif.com/compress", "http://www.soogif.com/crop", "http://www.uupoop.com/gif/"]
        },
        hahaimg: {
            siteName: ["斗图终结者", "斗图啦", "装逼神器", "U表情包", "撸表情", "爱斗图", "斗图表情", "表情帝", "soogif搜索", "小猪动图", "weavesilk"],
            sites: ["http://zb.mkblog.cn/", "https://www.doutula.com/", "http://deepba.com/", "http://www.ubiaoqing.com/", "http://www.lubiaoqing.com/", "http://www.adoutu.com/pages/watchList.php", "http://md.itlun.cn/", "http://www.biaoqingdi.net/", "http://soogif.com/", "http://www.piggif.com/", "http://weavesilk.com/"]
        }
    };
    var b = function() {
        this.tab = $(".zhutikuang").find(".tab");
        this.tabUl = this.tab.find("li");
        this.jumpLocation = $(".jump");
        this.flipButton = $("#flip");
        this.rizhiDiv = $("#rizhi");
        this.wxInfo = $(".zhutikuang").find(".wx-info");
        this.siteDretails = $(".zhutikuang").find(".site-dretails");
        this.weixinRec = $(".zhutikuang").find(".weixin-rec");
        this.init()
    };
    b.prototype = {
        init: function() {
            this.bindEvents()
        },
        bindEvents: function() {
            var e = this;
            this.tab.on("click", "li", function() {
                var h = $(this);
                var f = h.index();
                var g = h.parents(".tab").next(".sites-details").find("div");
                h.addClass("current").siblings().removeClass("current");
                g.eq(f).fadeIn(150).siblings().hide()
            });
            this.jumpLocation.on("click", function() {
                $("html, body").animate({
                    scrollTop: $($(this).attr("info")).offset().top + "px"
                }, {
                    duration: 250,
                    easing: "swing"
                });
                return false
            });
            this.wxInfo.on("click", function() {
                var f = $(this);
                var g = f.find("a").attr("keywords");
                a.showWeixinMessage(g)
            });
            this.siteDretails.on("click", function() {
                var g = $(this);
                var h = g.find("a").attr("detailsInfo");
                var i = g.find("a").html();
                var f = e.getDetailInfo(h);
                a.showDetailSites(f, i)
            });
            this.weixinRec.on("click", function() {
                var h = $(this);
                var f = h.find("a").attr("wximgsrc");
                var g = h.find("a").attr("intro");
                a.showWxRec(f, g)
            });
            this.flipButton.on("click", function() {
                e.rizhiDiv.slideToggle()
            })
        },
        getDetailInfo: function(h) {
            var g = d[h];
            var e = "";
            for (var f = 0; f < g.siteName.length; f++) {
                e += '<li><a href="' + g.sites[f] + '" target="_blank">' + g.siteName[f] + "</a></li>"
            }
            e = '<div class="detail-sites"><ul>' + e + "</ul></div>";
            return e
        }
    };
    var c = new b()
})();
