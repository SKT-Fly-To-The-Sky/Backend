/* *********** */
/* Last Updata : 2018.08.08.
/* *********** */

/*
 * global variable : commonUI
 */
var commonUI = commonUI || {};

(function(){
    /**
     * Mobile Resize
     * @namespace isMobile
     * @example
     * commonUI.isMobile;
     */
    commonUI.isMobile = (function(){
        var isMobile = false;
        var screenSize = parseInt($(this).width());
        if( 768 > screenSize){
            isMobile = true;
        }

        $(window).bind('resize', function(){
            var reSize = parseInt($(this).width());
            if( 768 > reSize && commonUI.isMobile == false){
                commonUI.isMobile = true;
            }else if(768 <= reSize && commonUI.isMobile == true){
                commonUI.isMobile = false;
            }
        });

        return isMobile;
    })();
    
    /**
     * gnbLayer Event
     * @namespace gnbLayer
     * @example
     * commonUI.gnbLayer.open() = gnbLayer open;
     * commonUI.gnbLayer.close() = gnbLayer close;
     */
    commonUI.gnbLayer = (function(){
        var open, close, subEventBind;
    
        open = function(){
            $(".gnb_layer").show(100, function(){
                $(".gnb_layer>.inner").stop().animate({"right":"0"}, 450);
            });
            $(".gnb_layer").append("<div class='ovl'></div>");

            $(".gnb_layer .ovl").on("click", function(){
                commonUI.gnbLayer.close();
            });
        }
    
        close = function(){
            $(".gnb_layer>.inner").stop().animate({"right":"-100%"}, 450);

            setTimeout(function(){
                $(".gnb_layer").hide();
                $(".gnb_layer .ovl").remove();
            }, 450);
        }

        subEventBind = function(){
            $(".gnb_area button").on("click", function(){
                $(this).parent().siblings().removeClass("on");
                $(this).parent().toggleClass("on");
                $(this).next("ul").slideToggle(300);
                $(this).parent().siblings().find("ul").slideUp(300);
            })
        }

        $(window).load(function(){
            subEventBind();
        });

        return {
            open : open,
            close : close
        }
    })();
    
    /**
     * layer Event
     * @namespace layer
     * @example
     * commonUI.layer.open(target) = layer open;
     * commonUI.layer.close = layer close;
     */
    commonUI.layer = (function(){
        var open, close, _target = undefined;
    
        open = function(target){
            _target = $("." + target);
            _target.fadeIn();
    
            $(document).keydown(function(event){
                if(event.keyCode == '27'){
                    commonUI.layer.close();
                }
            });

            //business - social_info, business - city_info
            var layerPage = $(".social_info_page, .city_info_page");
            if(layerPage.length){
                $('.social_info_layer .slide_box , .social_info_layer .slide_nav').slick("refresh");
            }
        }
    
        close = function(){
            if( _target == 'undefined' ){
                _target = $(".layer");
            }
            
            //business - social_info, business - city_info
            var layerPage = $(".social_info_page, .city_info_page");
            if(layerPage.length){
                $('.social_info_layer .slide_box , .social_info_layer .slide_nav').slick('unslick');
            }
            _target.fadeOut();

            //layer 컨텐츠 스크롤 최상단으로
            setTimeout(function(){
                _target.find(".con").scrollTop(0,0);
            }, 100);
        }

        return {
            open : open,
            close : close
        }
    })();

    /**
     * page top move Event
     * @namespace topFn
     * @example
     * commonUI.topFn();
     **/
    commonUI.topFn = (function(){
        var move = (function(){
            $('html, body').stop().animate({scrollTop: 0}, 1000);
        })();

        return move;
    });

    /**
     * Tab Module
     * @namespace tabModule
     * @example
     * new commonUI.tabModule('selecter');
     * TabModule auto Apply Class Name = 'js_tab'
     */
    commonUI.tabModule = (function(){
        var tab = function(target){
            this.$tabWrap = $(target);
            this.$tabBtn = $(".js_tabBtn li button", this.$tabWrap);
            this.$tabCon = $(".js_tabCon", this.$tabWrap);
            this.eventBinding();
        };

        tab.prototype = {
            eventBinding : function(){
                var self = this;
                this.$tabBtn.on("click", function(){
                    self.activeEvent(this);
                });
            },
            activeEvent : function(tg){
                var $tg = $(tg).parent(), tgIdx = $tg.index();
                this.$tabBtn.parent().removeClass("on");
                this.$tabCon.removeClass("on");
                $tg.addClass("on");
                this.$tabCon.eq(tgIdx).addClass("on");
            }
        }

        return tab;
    })();

    /**
     * toggle Module
     * @namespace toggleModule
     * @example
     * //toggleModule Class Name = 'toggleMenu'
     **/
	commonUI.toggleModule = (function(){
		$(".toggleTit").on("click", function(){
			var target = $(this),
				targetUl = target.next("ul"),
				targetBtn = targetUl.find("button"),
				ulWidth = target.parent().width(),
				ulHeight = target.outerHeight();

			target.toggleClass("active");
			targetUl.css({"top":ulHeight,"width":ulWidth-2});
			targetBtn.css({"line-height":ulHeight-2+"px"});
			if(target.parent(".toggleMenu").hasClass("type2")){
				targetUl.css({"top":ulHeight,"width":ulWidth});
			}
			targetBtn.on("click", function(){
				var optTarget = $(this).html();
				$(this).closest(".toggleMenu").find(".toggleTit").removeClass("active").children("p").html(optTarget);
			});
		});
	});
})();

function loginClose(){
    $(".login_layer").fadeOut();
}

$(window).load(function(){
    $("#footer .fixed_btn .top button").on('click', function(){
        commonUI.topFn();
    });

	/* toggle Module */
    commonUI.toggleModule();
});

$(document).ready(function(){
    /* Tab Default Apply */
    $('.js_tab').each(function () {
        new commonUI.tabModule(this);
    });

    $(".date_picker input").datepicker();
    
    var $header = $("header"),
        $gnb = $(".gnb_layer");

    if(commonUI.isMobile){
        // console.log("mb");

    }else{
        // console.log("web");
        //pc_GNB
        $header.mouseenter(function(){
            $gnb.addClass("active");
        });
        $header.mouseleave(function(){
            $gnb.removeClass("active");
        });
    }

    $(window).bind("resize", function(){
        var reSize = parseInt($(this).width());
        if(768 > reSize){
            // console.log("mb");

        }else if(768 <= reSize) {
            // console.log("web");
            $header.mouseenter(function(){
                $gnb.addClass("active");
            });
            $header.mouseleave(function(){
                $gnb.removeClass("active");
            });

        }
    });
});
