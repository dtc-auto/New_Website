/* auto.js seven 2017-3-11 */

//下拉框
$.fn.selectBox = function(options){
	$.fn.selectBox.defaults = {
		txt:'.m-sel-txt',
		cont:'.m-sel-con',
		list:'.m-sel-con li'
	};
	return this.each(function(){
		var opts = $.extend({},$.fn.selectBox.defaults,options);
		var oTxt = $(this).find(opts.txt);
		var oCont = $(this).find(opts.cont);
		var oList = $(this).find(opts.list);

		oTxt.click(function(event){
            var e = event || window.event;
			if(e && e.stopPropagation){
				e.stopPropagation();
			}else{
				e.cancelBubble = true;
			};
            if(oCont.html()!= ''){
                oCont.show();
            };
        });
        oList.click(function(event){
            var e = event || window.event;
			if(e && e.stopPropagation){
				e.stopPropagation();
			}else{
				e.cancelBubble = true;
			};
            oTxt.find('span').text($(this).text());
            oCont.hide();
        });
        $(document).click(function(){
            oCont.hide();
        });
	});//each End
};//selectBox End

function addCompare(){
	jQuery('#compare').show();
	jQuery('#sideCompare').addClass('open');
};

jQuery(function(){

	//input提示文字
	jQuery('body').on('focus','.ccf-search input',function(){
		jQuery(this).addClass('current');
		jQuery(this).next('span').addClass('current');
	});
	jQuery('body').on('blur','.ccf-search input',function(){
		jQuery(this).removeClass('current');
		jQuery(this).next('span').removeClass('current');
	});
	//侧导航
	function sideBar(){
	    var bodyHeight = jQuery(document).height();
	    var winHeight = jQuery(window).height();
	    var winScrollTop = jQuery(window).scrollTop();
	    if(winScrollTop >= bodyHeight-winHeight-400){//侧边栏定位
	        jQuery("#side-nav").stop().animate({"bottom":winHeight+winScrollTop+440-bodyHeight},350);
	    }else{
	        jQuery("#side-nav").stop().animate({"bottom":"40px"},350);
	    };
	    /*if(winScrollTop>0){
	        jQuery("#side-nav").show();
	    }else{
	        jQuery("#side-nav").hide();
	    }*/
	};
	jQuery(window).scroll(function(){ sideBar(); });
	jQuery(window).resize(function(){ sideBar(); });
	//二维码
	jQuery('.side-wx').hover(function(){
		jQuery('#side-nav').find('.ewmbox').stop().fadeIn(350).animate({'left':'-382px'},150);
	},function(){
		jQuery('#side-nav').find('.ewmbox').css({'left':'-400px'}).hide();
	});
	//回到顶部
	jQuery('#gotop').click(function(){
		jQuery("html,body").animate({scrollTop:0},350);
	});
	//年份
	jQuery('.auto-year').hover(function(){
		$(this).find('.auto-year-con').show();
	},function(){
		$(this).find('.auto-year-con').hide();
	});
	//新闻切换
	jQuery('.car-news-hd li').click(function(){
		jQuery(this).addClass('cur').siblings('li').removeClass('cur');
		jQuery('.car-news-bd .car-news-list').hide();
		jQuery('.car-news-bd .car-news-list').eq(jQuery(this).index()).show();
	});
	//车型列表
	jQuery('.car-list-hd ul .sale-tab').click(function(){
		jQuery(this).addClass('car-list-cur').siblings('li').removeClass('car-list-cur');
		jQuery('#carListCont .car-list-bd').hide();
		jQuery('#carListCont .car-list-bd').eq(jQuery(this).index()).show();
	});
	//同级别车
	jQuery('.bdcar-ph-hd a').click(function(){
		jQuery(this).addClass('current').siblings('a').removeClass('current');
		jQuery('.bdcar-ph-bd').find('ul').hide().eq(jQuery(this).index()).show();
	});
	//经销商
	jQuery('.dealer-city').hover(function(){
		jQuery(this).find('.city-bd').show();
	},function(){
		jQuery(this).find('.city-bd').hide();
	});
	//车市行情
	jQuery('.car-hq-city').hover(function(){
		jQuery(this).find('.city-bd').show();
	},function(){
		jQuery(this).find('.city-bd').hide();
	});
	//车型对比
	jQuery('#sideCompare').click(function(){
		if(jQuery(this).hasClass('open')){
			jQuery(this).removeClass('open');
			jQuery('#compare').hide();
		}else{
			jQuery(this).addClass('open');
			jQuery('#compare').show();
		}
	});
	jQuery('#compare .cp-close').click(function(){
		jQuery('#sideCompare').removeClass('open');
		jQuery('#compare').hide();
	});
	//询价
	jQuery('.price-pop-hd .off').click(function(){
		jQuery('.price-pop,.cx-bg').hide();
	});
});

