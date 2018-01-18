// JavaScript Document


/*弹出层关闭*/
$(function(){
	$('div.tcc a.close').click(function () { $('div.tcc').hide();$('div.bg').hide(); });
})
$(function(){
	$('.btnqx').click(function () { $('div.tcc').hide();$('div.bg').hide(); });
})
$(function(){
	$('#div2 .btntj').click(function () { $('div.tcc').hide();$('div.bg').hide(); });
})
function popup(popupName){
	var _scrollHeight = $(document).scrollTop(),//获取当前窗口距离页面顶部高度
	_scrollLeft = $(document).scrollLeft(),
	_windowHeight = $(window).height(),//获取当前窗口高度
	_windowWidth = $(window).width(),//获取当前窗口宽度
	_popupHeight = popupName.height(),//获取弹出层高度
	_popupWeight = popupName.width();//获取弹出层宽度
	_posiTop = (_windowHeight - _popupHeight)/2 + _scrollHeight;
	_posiLeft = (_windowWidth - _popupWeight)/2 + _scrollLeft;
	popupName.css({"left": _posiLeft + "px","top":_posiTop + "px","display":"block"});//设置position
}