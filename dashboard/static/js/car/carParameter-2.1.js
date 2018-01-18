wd.scrollFloat = function(e, t, n) {
    var r = this,
    i = document.getElementById(e),
    s = {
        w: this.css(i, "width").replace(/px/gi, ""),
        h: this.css(i, "height").replace(/px/gi, "")
    },
    o = this.abs.point(this.dom.id(t)),
    u = this.dom.id("config_nav_temp"),
    a = "_" + e,
    f = function() {
        var e = r.dom.create("div");
        e.id = a,
        e.className = i.className,
        e.style.cssText = i.style.cssText,
        e.innerHTML = i.innerHTML,
        r.css(e, {
            top: "0px",
            left: "0px",
            display: "none",
            width: wd.browsers.fireFox || wd.browsers.isIE || wd.browsers.opera ? "195px": "196px",
            position: wd.browsers.isIE6 ? "absolute": "fixed"
        }),
        n && r.css(e, n),
        document.body.appendChild(e)
    },
    l = function() {
        var e = r.abs.scroll();
        o = r.abs.point(r.dom.id(t)),
        e.top > o.y ? wd.browsers.isIE6 ? r.css(i, {
            position: "absolute",
            top: e.top + "px",
            left: o.x + "px"
        }) : (r.css(i, {
            position: "fixed",
            left: o.x - e.left + "px",
            top: "0px"
        }), r.css(u, "display", "block")) : (r.css(i, {
            position: "relative",
            left: "0px",
            top: "0px"
        }), r.css(u, "display", "none"))
    },
    c = function() {
        var e = r.abs.scroll();
        o = r.abs.point(r.dom.id(t)),
        e.left > o.x ? wd.browsers.isIE6 ? r.css(i, {
            position: "absolute",
            display: "block",
            top: "0px",
            left: e.left - o.x + "px"
        }) : r.css(i, {
            position: "fixed",
            display: "block",
            left: "0px",
            top: o.y - e.top + "px"
        }) : r.css(i, "display", "none")
    },
    h = function() {
        var e = r.abs.scroll(),
        n = r.dom.id(a);
        o = r.abs.point(r.dom.id(t)),
        e.left > o.x ? wd.browsers.isIE6 ? r.css(n, {
            display: "block",
            top: (e.top == 0 ? e.top + o.y: e.top < o.y ? o.y: e.top) + "px",
            left: e.left + "px",
            border: "1px solid #D9E5F3",
            fontSize: "12px"
        }) : r.css(n, {
            display: "block",
            top: (e.top == 0 ? o.y: e.top < o.y ? o.y - e.top: 0) + "px",
            left: "0px",
            border: "1px solid #D9E5F3",
            fontSize: "12px"
        }) : r.css(n, "display", "none")
    };
    return this.top = function(e) {
        e ? l() : (r.handler.addEvent(window, "scroll", l), r.handler.addEvent(window, "resize", l), r.handler.addEvent(window, "load", l))
    },
    this.left = function() {
        r.handler.addEvent(window, "scroll", c),
        r.handler.addEvent(window, "resize", c),
        r.handler.addEvent(window, "load", c),
        c()
    },
    this.absTop = function(e) {
        e ? (wd.browsers.isIE6 && r.css(this.dom.id(a), {
            top: "0"
        }), h()) : (this.dom.id(a) || f(), r.handler.addEvent(window, "scroll", h), r.handler.addEvent(window, "resize", h), r.handler.addEvent(window, "load", h))
    },
    this
};
var addedCarList = [],
paramConfig = function(e, t) {
    var n = this,
    r = {
        nav: function() {
            return '<table cellspacing="0"  width="320" cellpadding="0" class="tbset">    <tbody>        <tr>            <th>                <div id="config_setbox" class="setbox">                    <label><input type="checkbox" value="high" ' + (n.Data.high ? 'checked="checked"': "") + ' name="radioShow">高亮显示差异参数</label>' + '                    <label><input type="checkbox" value="hide" ' + (n.Data.hide ? 'checked="checked"': "") + '  name="radioShow">隐藏相同参数</label>' + "                    <p>注：●标配  ○选配  -无</p>" + "                </div>" + "            </th>" + "            #LIST#" + "        </tr>" + "    </tbody>" + "</table>"
        }
    },
    i = wd.dom.id("config_nav"),
    s = wd.dom.id("config_data"),
    o = wd.dom.id("config_side");
    this.Data = {
        carList: [],
        allList: [],
        transmission: [],
        pailiang: [],
        horsePower: [],
        year: [],
        carNum: 0,
        hide: !1,
        high: !1,
        isPust: !0,
        isCheckBox: !0,
        curSpecCss: "#F0F3F8",
        twolCell: {
            "发动机特有技术": 0,
            "前悬挂类型": 0,
            "后悬挂类型": 0,
            "多媒体系统": 0
        },
        navMeto: {
            isAdd: !0,
            item: []
        },
        jiucuo: !1,
        know: !1
    },
    this.init = function() {
        if (!config || !option || config.returncode != 0 || option.returncode != 0) return;
        this.isTop(),
        this.initYearList(),
        this.initPailiangList(),
        this.initHorsePowerList(),
        this.initBianshuList();
        var e = this.selectCar().join(",");
        this.responseNav(e),
        this.responseContent(e),
        this.scrollFloat(),
        this.selectEvent(),
        this.MoveOrDel(),
        this.Data.navMeto.isAdd = !1,
        this.repsonseNavScrollLeft(),
        this.navScrollLeft(),
        this.woyaojiucuo()
    },
    this.isContain = function(e, t) {
        var n = t.length,
        r = 0,
        i = !1;
        for (; r < n; r++) if (t[r] == e) {
            i = !0;
            break
        }
        return i
    },
    this.initYearList = function() {
        var e = config.result.paramtypeitems[0].paramitems[1].valueitems,
        t = e.length,
        n = 0;
        for (; n < t; n++) {
            if (this.isContain(e[n].specid, addedCarList)) continue;
            this.Data.year.push(e[n].value)
        }
    },
    this.initPailiangList = function() {
        var e = config.result.paramtypeitems[0].paramitems,
        t = e.length,
        n = 0;
        for (; n < t; n++) {
            var r = e[n].name;
            if (r == "排量(L)") {
                var i = e[n].valueitems,
                s = 0,
                o = i.length;
                for (; s < o; s++) {
                    if (this.isContain(i[s].specid, addedCarList)) continue;
                    this.Data.pailiang.push(i[s].value)
                }
            }
        }
    },
    this.initHorsePowerList = function() {
        var e = config.result.paramtypeitems[2].paramitems,
        t = e.length,
        n = 0;
        for (; n < t; n++) {
            var r = e[n].name;
            if (r == "最大马力(Ps)") {
                var i = e[n].valueitems,
                s = 0,
                o = i.length;
                for (; s < o; s++) {
                    if (this.isContain(i[s].specid, addedCarList)) continue;
                    this.Data.horsePower.push(i[s].value)
                }
            }
        }
    },
    this.initBianshuList = function() {
        var e = config.result.paramtypeitems[0].paramitems,
        t = e.length,
        n = 0;
        for (; n < t; n++) {
            var r = e[n].name;
            if (r == "变速箱类型") {
                var i = e[n].valueitems,
                s = 0,
                o = i.length;
                for (; s < o; s++) {
                    if (this.isContain(i[s].specid, addedCarList)) continue;
                    this.Data.transmission.push(i[s].value)
                }
            }
        }
    },
    this.scrollFloat = function(e) {
        if (e) {
            if (wd.browsers.isIE6) {
                var e = document.documentElement.scrollLeft + document.body.scrollLeft,
                t = document.body.scrollHeight,
                n = document.documentElement.scrollTop + document.body.scrollTop;
                t < n && (setTimeout(function() {
                    var e = wd.abs.scroll();
                    posXY = wd.abs.point(wd.dom.id("content")),
                    wd.css(wd.dom.id("config_nav"), {
                        position: "absolute",
                        top: e.top + "px",
                        left: posXY.x + "px"
                    })
                },
                100), window.scrollTo(e, t))
            }
            wd.scrollFloat("config_side", "config_data").left(),
            wd.scrollFloat("config_nav", "content").top(!0),
            wd.scrollFloat("config_setbox", "content").absTop(!0)
        } else wd.scrollFloat("config_nav", "content").top(),
        wd.scrollFloat("config_side", "config_data").left(),
        wd.scrollFloat("config_setbox", "content").absTop()
    },
    this.responseNav = function(e) {
        var t = arguments.length,
        n = 0,
        s = [],
        o = config.result.paramtypeitems[0].paramitems[0].valueitems,
        u = o.length,
        a = 0;
        this.Data.carList = [],
        this.Data.allList = [];
		if(config.result.seriesid!=105380){
			for (; a < u; a++) {
				this.Data.allList.push(o[a].specid);
				if (t == 1 && this.Data.isCheckBox && e.indexOf("-" + a + "-") == -1) continue;
				s.push("<td>"),
				s.push('<div class="carbox">'),
				s.push('<div><a href="http://auto.chexun.com/' + config.result.seriesEnglish + "/" + o[a].specid + '/">' + o[a].value + '</a></div>'),
				s.push("<p>"),
				s.push('<a target="_self" href="javascript:void(0);"  rel="' + o[a].specid + '" class="switch_left">左移</a>'),
				s.push('<a class="btn_del" href="javascript:void(0);" rel="' + o[a].specid + '" target="_self">删除</a>'),
				s.push('<a target="_self" href="javascript:void(0);"  rel="' + o[a].specid + '" class="switch_right">右移</a>'),
				s.push("</p>"),
				s.push("</div>"),
				s.push("</td>"),
				this.Data.carList.push(o[a].specid)
			}
		}

		if(config.result.seriesid==105380){
			for (; a < u; a++) {
				this.Data.allList.push(o[a].specid);
				if (t == 1 && this.Data.isCheckBox && e.indexOf("-" + a + "-") == -1) continue;
				s.push("<td>"),
				s.push('<div class="carbox">'),
				s.push('<div class="carboxTit"><a href="http://auto.chexun.com/' + config.result.seriesEnglish + "/" + o[a].specid + '/">' + o[a].value + '</a><a target=_blank href="http://mall2.chexun.com/Subject/savannah/index.html?3" class="dians"><img src="http://i0.chexun.net/images/auto/2015-06/icon_d.png"/></a></div>'),
				s.push("<p>"),
				s.push('<a target="_self" href="javascript:void(0);"  rel="' + o[a].specid + '" class="switch_left">左移</a>'),
				s.push('<a class="btn_del" href="javascript:void(0);" rel="' + o[a].specid + '" target="_self">删除</a>'),
				s.push('<a target="_self" href="javascript:void(0);"  rel="' + o[a].specid + '" class="switch_right">右移</a>'),
				s.push("</p>"),
				s.push("</div>"),
				s.push("</td>"),
				this.Data.carList.push(o[a].specid)
			}
		}

        n = this.Data.carList.length > 4 ? 0 : 4 - this.Data.carList.length;
        for (var f = 0; f < n; f++) s.push('<td><div class="carbox"></div></td>');
        this.Data.carNum = u,
        i.innerHTML = r.nav().replace("#LIST#", s.join(""))
    },
    this.isShowMove = function () {
        var tds = wd.dom.tag('td', i),
            len = tds.length,
            i = 0,
            endNum = 0;

        for (; i < len; i++) {
            if (wd.dom.byClass('btn_del', tds[i]).length > 0) {
                wd.css(wd.dom.byClass('switch_left', tds[i], 'a')[0], 'display', '');
                wd.css(wd.dom.byClass('switch_right', tds[i], 'a')[0], 'display', '');
                if (i == 0)
                    wd.css(wd.dom.byClass('switch_left', tds[i], 'a')[0], 'display', 'none');
                endNum = i;
            }
        }
        if (wd.dom.byClass('switch_right', tds[endNum], 'a').length > 0)
            wd.css(wd.dom.byClass('switch_right', tds[endNum], 'a')[0], 'display', 'none');
    },
    this.getCharactersLen = function(e) {
        var t = 0,
        n = 0,
        r;
        r = e.length;
        for (; n < r; n++) {
            var i = e.charCodeAt(n);
            i >= 1 && i <= 126 || 65376 <= i && i <= 65439 ? t++:t += 2
        }
        return t
    },
    this.getCharacters = {
        len: function(e) {
            var t = 0,
            n = 0,
            r;
            r = e.length;
            for (; n < r; n++) {
                var i = e.charCodeAt(n);
                i >= 1 && i <= 126 || 65376 <= i && i <= 65439 ? t++:t += 2
            }
            return t
        },
        sub: function(e, t) {
            return e.replace(/([\u0391-\uffe5])/ig, "$1a").substring(0, t).replace(/([\u0391-\uffe5])a/ig, "$1")
        }
    },
    this.responseContent = function(e) {
        var r = [],
        i = [],
        o = arguments.length,
        u = this.Data.carList.length > 4 ? 0 : 4 - this.Data.carList.length,
        a = this.Data.twolCell,
        f = this.Data.jiucuo;
        r.push('<div style="display: none;" class="fdbox" id="config_side">'),
        r.push('<table id="tab_side" cellspacing="0" cellpadding="0" class="tbcs">'),
        r.push("<tbody>");
        var l = function(s, f, l, c, h) {
            var p = a[s.name] == 0 ? !0 : !1;
            l = f + l,
            highlight = "",
            n.Data.high && !h && (highlight = 'class="highlight"'),
            r.push("<tr " + highlight + ' id="trs_' + l + '">'),
            r.push("<th " + (p ? 'class="twol"': "") + ">"),
            r.push("<div>" + s.name + "</div>"),
            r.push("</th>"),
            r.push("</tr>"),
            i.push("<tr " + highlight + ' id="tr_' + l + '">'),
            i.push("<th " + (p ? 'class="twol"': "") + ">"),
            i.push("<div >" + s.name + "</div>"),
            i.push("</th>");
            var d = s.valueitems,
            v = 0;
            for (var m = 0,
            g = d.length; m < g; m++) {
                if (o == 1 && this.Data.isCheckBox && e.indexOf("-" + m + "-") == -1) continue;
                var y = '<span style="display:none" class="jiucuo"><a modelId="' + d[m].specid + '" href="javascript:void(0);">纠错</a></span>';
                p ? (i.push("<td " + (d[m].specid == t || addedCarList.length > 0 && addedCarList[0] == d[m].specid ? 'style="background:' + n.Data.curSpecCss + ';"': "") + ">"), v = n.getCharacters.len(d[m].value), v > 44 ? i.push('<div title="' + d[m].value + '">' + n.getCharacters.sub(d[m].value, 44) + y + "</div>") : i.push("<div>" + d[m].value + y + "</div>"), i.push("</td>")) : i.push("<td " + (d[m].specid == t || addedCarList.length > 0 && addedCarList[0] == d[m].specid ? 'style="background:' + n.Data.curSpecCss + ';"': "") + "><div>" + (d[m].value == "0" ? "-": d[m].value) + y + " </div></td>")
            }
            for (var b = 0; b < u; b++) i.push("<td><div></div></td>");
            i.push("</tr>")
        },
        c = function(t, s, o, u) {
            var a = s,
            f = a.length,
            c = 0,
            p = "";
            for (var d = 0; d < f; d++) {
                var v = d + o,
                m = a[d].typeId;
                i.push('<table id="tab_' + v + '" cellspacing="0" cellpadding="0" class="tbcs">'),
                i.push("<tbody>"),
                r.push("<tr>"),
                r.push('<th show="1" id="sth_' + v + '" class="cstitle" style="border-right:none;">'),
                r.push("<h3><span>" + a[d].name + "</span></h3>"),
                r.push("</th>"),
                r.push("</tr>"),
                i.push("<tr>"),
                i.push('<th show="1" pid="tab_' + v + '" id="nav_meto_' + v + '" class="cstitle" colspan="' + ((this.Data.carList.length < 4 ? 4 : this.Data.carList.length) + 1) + '">'),
                i.push("<h3><span>" + a[d].name + "</span></h3>"),
                i.push("</th>"),
                i.push("</tr>"),
                this.Data.navMeto.isAdd && this.Data.navMeto.item.push({
                    name: a[d].name,
                    id: "nav_meto_" + v
                });
                if (showPara[m]) {
                	for (var g = 0,y = m == 1 ? showPara[m].length + 4 : showPara[m].length; g < y; g++) {
                        var b = null;
                        if (m == 1) {
                            if (g < t) continue;
                            g == 2 || g == 3 ? b = a[d][u + "items"][g] : b = h(showPara[m][g - 4], a[d][u + "items"])
                        } else b = h(showPara[m][g], a[d][u + "items"]);
                        if (b == null) continue;
                        n.Data.hide ? n.compare(b.valueitems, e) || l(b, v, c, m) : n.Data.high ? l(b, v, c, m, n.compare(b.valueitems, e)) : l(b, v, c, m),
                        g == y - 1 && (i.push("</tbody>"), i.push("</table>")),
                        c++
                    }
				}
            }
        },
        h = function(e, t) {
            var n = 0,
            r = t.length,
            i = null;
            for (; n < r; n++) if (t[n].id == e) {
                i = t[n];
                break
            }
            return i
        };
        c(2, config.result.paramtypeitems, 0, "param"),
        c(0, option.result.configtypeitems, 100, "config"),
        r.push("</tbody>"),
        r.push("</table>"),
        r.push("</div>"),
        i.push('<table cellspacing="0" cellpadding="0" class="tbcs" id="tab_999" style="width: 3500px;">'),

        i.push("</table>"),
        n.Data.isPust = !1,
        s.innerHTML = r.join("") + i.join(""),
        n.titleEvent(),
        n.mouseChangeCss(),
        this.isShowMove()
    },
    this.compare = function(e, t) {
        var n = !0,
        r = e.length,
        i = 0,
        s, o = !0;
        if (r == 0) return n;
        for (; i < r; i++) {
            if (t != undefined && this.Data.isCheckBox && t.indexOf("-" + i + "-") == -1) continue;
            if (o) {
                s = e[i].value,
                o = !1;
                continue
            }
            if (e[i].value != s) {
                n = !1;
                break
            }
        }
        return n
    },
    this.titleEvent = function() {
        function l(e, t) {
            var n = wd.dom.tag("tr", wd.dom.id("tab_" + e)),
            r = wd.dom.tag("tr", wd.dom.id("tab_side")),
            i = n.length,
            s = r.length,
            o = 1,
            u = 0;
            for (; o < i; o++) wd.css(n[o], "display", t);
            for (; u < s; u++) {
                var a = r[u];
                a.getAttribute("rel") == e && wd.css(a, "display", t)
            }
        }
        var e = wd.dom.byClass("cstitle", s, "th"),
        t = wd.dom.byClass("tbcs", s, "table"),
        n = e.length,
        r = 0,
        o = this,
        u = parseInt(wd.css(wd.dom.tag("table", i)[0], "width").replace(/px/gi, "")) + 1 + "px";
        for (var a = 1,
        f = t.length; a < f; a++) wd.css(t[a], {
            width: u
        });
        return
    },
    this.mouseChangeCss = function() {
        var e = wd.dom.tag("tr", s),
        t = e.length - 1,
        n = 0;
        for (; n < t; n++) wd.handler.addEvent(e[n], "mouseenter",
        function(e) {
            e = e || window.event;
            var t = e.currentTarget || e.srcElement,
            n = t.style.backgroundColor,
            r = t.id.replace("trs_", "").replace("tr_", "");
            if (n == "rgb(240, 243, 248)" || n == "#f0f3f8") return;
            wd.dom.id("trs_" + r) && (wd.css(wd.dom.id("trs_" + r), "background", "#f8f5f0"), wd.css(wd.dom.id("tr_" + r), "background", "#f8f5f0"))
        }),
        wd.handler.addEvent(e[n], "mouseleave",
        function(e) {
            e = e || window.event;
            var t = e.currentTarget || e.srcElement,
            n = t.style.backgroundColor,
            r = t.id.replace("trs_", "").replace("tr_", "");
            if (n == "rgb(240, 243, 248)" || n == "#f0f3f8") return;
            wd.dom.id("trs_" + r) && (wd.css(wd.dom.id("trs_" + r), "background", "#FFFFFF"), wd.css(wd.dom.id("tr_" + r), "background", "#FFFFFF"))
        }),
        e[n].onclick = function() {
            var e = this.id.replace("trs_", "").replace("tr_", ""),
            t = this.style.backgroundColor;
            t == "rgb(240, 243, 248)" || t == "#f0f3f8" ? wd.dom.id("trs_" + e) && (wd.css(wd.dom.id("trs_" + e), "backgroundColor", "#FFFFFF"), wd.css(wd.dom.id("tr_" + e), "backgroundColor", "#FFFFFF")) : wd.dom.id("trs_" + e) && (wd.css(wd.dom.id("trs_" + e), "backgroundColor", "#F0F3F8"), wd.css(wd.dom.id("tr_" + e), "backgroundColor", "#F0F3F8"))
        }
    },
    this.checkboxInit = function() {
        var e = wd.dom.tag("input"),
        t = e.length,
        n = 0;
        for (; n < t; n++) e[n].type == "checkbox" && (e[n].checked = !1)
    },
    this.selectEvent = function() {
        function i(n, r, i) {
            for (var s = 0; s < t; s++) e[s].type == "checkbox" && e[s].name == n && e[s].value == i && (e[s].checked = r)
        }
        var e = wd.dom.tag("input"),
        t = e.length,
        r = 0;
        for (; r < t; r++) e[r].type == "checkbox" && (e[r].onclick = function() {
            var e = n.selectCar().join(",");
            switch (this.name) {
            case "radioShow":
                i(this.name, this.checked, this.value);
                if ((n.Data.allList.length == 0 || n.Data.carList.length < 2) && this.checked) return;
                this.value == "hide" ? n.Data.hide = this.checked: this.value == "high" && (n.Data.high = this.checked);
                break;
            case "pailiang":
            case "horsePower":
            case "transmission":
            case "year":
                n.responseNav(e)
            }
            n.responseContent(e),
            n.scrollFloat(!0),
            n.selectEvent()
        })
    },
    this.selectCar = function() {
        function c(e, t, n) {
            var r = [],
            i = n.length;
            for (var s = 0,
            o = t.length; s < o; s++) for (var u = 0; u < i; u++) n[u] == t[s] && r.push(u);
            for (var a = 0; a < r.length; a++) r[a] = r[a] + addedCarList.length;
            if (addedCarList.length > 0) {
                var f = 0,
                l = addedCarList.length;
                for (; f < l; f++) r.unshift(f)
            }
            return r
        }
        function h(e) {
            var t = [];
            if (e != null) {
                e = e.split(",");
                for (var n in e) t.push(e[n])
            }
            return t
        }
        function p(e, t) {
            var n = [],
            r = e.length,
            i = t.length;
            return n = (e.join(",") + "|" + t.join(",")).match(/(\b[^,]+\b)(?!.*\b\1\b.*\|)(?=.*\|.*\b\1\b)/g),
            n == null ? [] : n
        }
        var e = wd.dom.tag("input"),
        t = e.length,
        r = "",
        i = [],
        s = [],
        hp = [],
        o = [],
        u = [],
        a = 0,
        f = 0;
        for (var l = 0; l < t; l++) if (e[l].type == "checkbox" && e[l].checked) switch (e[l].name) {
        case "pailiang":
            s.push(e[l].value),
            a++;
            break;
        case "horsePower":
            hp.push(e[l].value),
            a++;
            break;
        case "transmission":
            o.push(e[l].value),
            a++;
            break;
        case "year":
            u.push(e[l].value),
            a++
        }
        a > 0 ? this.Data.isCheckBox = !0 : this.Data.isCheckBox = !1,
        s.length > 0 && (s = c("pailiang", s, n.Data.pailiang), f++),
        hp.length > 0 && (hp = c("horsePower", hp, n.Data.horsePower), f++),
        o.length > 0 && (o = c("transmission", o, n.Data.transmission), f++),
        u.length > 0 && (u = c("year", u, n.Data.year), f++);
        var d = s.length,
        v = o.length,
        m = u.length,
        hl = hp.length;
        //f > 1 ? d > 0 && v > 0 && m > 0 ? i = p(s, p(o, u)) : d > 0 && v > 0 ? i = p(s, o) : d > 0 && m > 0 ? i = p(s, u) : v > 0 && m > 0 && (i = p(o, u)) : d > 0 ? i = s: v > 0 ? i = o: i = u;


        if(f > 1) {
        	if( d > 0 && v > 0 && m > 0 && hl > 0) {
        		i = p(s, p(o, p(u, hp)));
        	} else {
        		if( d > 0 && v > 0 && m > 0 ) {
    				i = p(s, p(o, u));
    			} else if( d > 0 && m > 0 && hl > 0) {
    				i = p(s, p(u, hp));
            	} else if( d > 0 && v > 0 && hl > 0) {
        			i = p(s, p(o, hp));
        		} else if( v > 0 && m > 0 && hl > 0) {
        			i = p(o, p(u, hp));
            	} else {
            		if(d > 0 && v > 0) {
    					i = p(s, o);
    				} else if(d > 0 && m > 0){
						i = p(s, u);
					} else if(d > 0 && hl > 0){
						i = p(s, hp);
					} else if(v > 0 && hl > 0){
						i = p(o, hp);
					} else if(m > 0 && hl > 0){
						i = p(u, hp);
					} else {
						i = p(u, o);

					}
            	}
        	}
		}
        else {
			if(d > 0) {
				i = s;
			} else if(v > 0) {
				i = o;
			} else if(hl > 0) {
				i = hp;
			} else {
				i = u;
			}
		}


        for (var g = 0,
        y = i.length; g < y; g++) i[g] = "-" + i[g] + "-";
        return i
    },
    this.MoveOrDel = function() {
        var e = function(e) {
            if (e == -1) return;
            var t = config.result.paramtypeitems,
            r = option.result.configtypeitems,
            i = function(e, t, n) {
                for (var r = 0,
                i = e.length; r < i; r++) for (var s = 0,
                o = e[r][n + "items"].length; s < o; s++) e[r][n + "items"][s].valueitems.splice(t, 1)
            };
            i(t, e, "param"),
            i(r, e, "config"),
            e < addedCarList.length ? addedCarList.splice(e, 1) : (n.Data.pailiang.splice(e, 1), n.Data.horsePower.splice(e, 1), n.Data.transmission.splice(e, 1), n.Data.year.splice(e, 1)),
            n.Data.carNum--
        },
        r = function(e) {
            var t = n.Data.allList,
            r = t.length,
            i = -1;
            for (var s = 0; s < r; s++) if (t[s] == e) {
                i = s;
                break
            }
            return i
        },
        o = function(e, t, s) {
            var o = wd.dom.tag("td", i),
            u = 0;
            switch (s) {
            case "l":
                u = wd.dom.byClass("btn_del", o[t - 2], "a")[0].getAttribute("rel");
                break;
            case "r":
                u = wd.dom.byClass("btn_del", o[t], "a")[0].getAttribute("rel")
            }
            var a = r(e),
            f = r(u),
            l = null,
            c = config.result.paramtypeitems,
            h = option.result.configtypeitems,
            p = function(e) {
                l = e[a],
                e[a] = e[f],
                e[f] = l
            };
            n.changeData(c, a, f, "param"),
            n.changeData(h, a, f, "config"),
            p(n.Data.pailiang),
            p(n.Data.horsePower),
            p(n.Data.transmission),
            p(n.Data.year),
            a < addedCarList.length && p(addedCarList)
        },
        u = function(e, t) {
            var n = wd.dom.tag("table", i)[0],
            r = wd.dom.tag("table", s),
            o = 0,
            u = 0,
            a = parseInt(wd.css(wd.dom.tag("table", i)[0], "width").replace(/px/gi, "")) + 1 + "px",
            f = function(t) {
                t ? n.rows[0].cells[e].innerHTML = '<div id="temp_' + o+++'" style="padding:0;width:160px;" class="carbox"></div>': n.rows[0].deleteCell(e);
                for (var i = 0,
                s = r.length - 1; i < s; i++) {
                    var u = wd.dom.tag("tr", r[i]),
                    a = u.length,
                    f = !0;
                    for (var l = 0; l < a; l++) u[l].cells.length > 1 && (t ? f ? (u[l].cells[e].innerHTML = '<div id="temp_' + o+++'"></div>', f = !1) : u[l].cells[e].innerHTML = "": u[l].deleteCell(e));
                    wd.css(r[i], {
                        width: "auto"
                    })
                }
            },
            l = function() {
                u++,
                u == o && t()
            };
            f(!0);
            for (var c = 0; c < o; c++) wd.animate(wd.dom.id("temp_" + c)).start({
                width: "0px"
            },
            250, l)
        },
        a = function(e, r, o, u) {
            var a = wd.dom.tag("table", i)[0],
            f = wd.dom.tag("table", s),
            l = a.rows[0].cells[r],
            c = wd.css(l, "width"),
            h = wd.dom.create("div"),
            p = wd.abs.scroll(l),
            d = wd.abs.point(l),
            v = wd.abs.point(wd.dom.id("content")),
            m,
            g = "background:#F0F3F8;",
            y = wd.css(i, "position");
            wd.css(h, {
                opacity: "0.5",
                position: "absolute",
                zIndex: "1300",
                top: v.y + "px",
                left: (y == "relative" ? d.x: p.left + d.x) + "px",
                width: c,
                background: "#F0F3F8",
                overflow: "hidden"
            });
            var b = '<div class="operation">   <table cellspacing="0" cellpadding="0" class="tbset">       <tbody>           <tr style="#COLOR#">               <td>#TOP#</td>           </tr>       </tbody>    </table> </div> ',
            w = '<table cellspacing="0" cellpadding="0" class="tbcs" style="width:160px;">     <tbody>         <tr style="#COLOR##HEIGHT#">             <td ' + (e == t ? 'style="background:' + n.Data.curSpecCss + ';"': "") + ">#CON#</td>" + "         </tr>" + "     </tbody>" + "</table>",
            E = '<table cellspacing="0" cellpadding="0" class="tbcs" style="width:160px;">     <tbody>         <tr style="#COLOR#height:87px;">             <td ' + (e == t ? 'style="background:' + n.Data.curSpecCss + ';"': "") + ">#CON#</td>" + "         </tr>" + "     </tbody>" + "</table>",
            S = '<table cellspacing="0" cellpadding="0" class="tbcs" style="width:160px;">     <tbody>         <tr>             <th class="cstitle"><h3></h3></th>         </tr>     </tbody></table>',
            x = [];
            x.push('<div class="pzbox" ' + (wd.css(i, "position") == "relative" ? "": 'style="position:relative;top:' + (p.top - v.y) + 'px"') + ">"),
            x.push(b.replace("#TOP#", l.innerHTML)),
            x.push("</div>"),
            x.push('<table class="tbcs" style="width:160px;" cellpadding="0" cellspacing="0"><tbody><tr><th class="cstitle"><h3></h3></th></tr></tbody></table>'),
            x.push('<div class="pzbox">'),
            x.push('<div class="conbox">');
            for (var T = 1,
            N = f.length - 1; T < N; T++) {
                var C = wd.dom.tag("tr", f[T]),
                k = C.length;
                T != 1 && x.push(S);
                for (var L = 0; L < k; L++) {
                    if (C[L].style.display == "none") break;
                    if (C[L].cells.length > 1) {
                        var A = C[L].style.backgroundColor,
                        O = C[L].cells[0].className == "twol";
                        A == "rgb(240, 243, 248)" || A == "#f0f3f8" ? x.push(w.replace("#CON#", C[L].cells[r].innerHTML).replace("#COLOR#", g).replace("#HEIGHT#", O ? "height:51px;": "height:29px;")) : x.push(w.replace("#CON#", C[L].cells[r].innerHTML).replace("#COLOR#", "").replace("#HEIGHT#", O ? "height:51px;": "height:29px;"))
                    }
                }
            }
            x.push("</div>"),
            x.push("</div>"),
            h.innerHTML = x.join(""),
            document.body.appendChild(h);
            switch (o) {
            case "l":
                m = (y == "relative" ? d.x: p.left + d.x) - parseInt(c.replace(/px/gi, "")) + "px";
                break;
            case "r":
                m = (y == "relative" ? d.x: p.left + d.x) + parseInt(c.replace(/px/gi, "")) + "px"
            }
            wd.animate(h).start({
                left: m
            },
            350,
            function() {
                document.body.removeChild(h),
                setTimeout(function() {
                    u();
                    var e = n.selectCar().join(",");
                    n.responseNav(e),
                    n.responseContent(e),
                    n.scrollFloat(!0),
                    n.selectEvent()
                },
                10)
            })
        };
        i.onclick = function(t) {
            function c(e) {
//                if (wd.browsers.isIE) {
                    e();
                    var t = n.selectCar().join(",");
                    n.responseNav(t),
                    n.responseContent(t),
                    n.scrollFloat(!0),
                    n.selectEvent()
//                } else
//                	u(f,
//                function() {
//                    e();
//                    var t = n.selectCar().join(",");
//                    n.responseNav(t),
//                    n.responseContent(t),
//                    n.scrollFloat(!0),
//                    n.selectEvent()
//                })
            }
            function h(e) {
                e();
                var t = n.selectCar().join(",");
                n.responseNav(t),
                n.responseContent(t),
                n.scrollFloat(!0),
                n.selectEvent()
            }
            t = t || window.event;
            var i = t.target || t.srcElement,
            s = i,
            f;
            if (!i.className && (i.className != "btn_del" || i.className != "switch_left" || i.className != "switch_right")) return;
            while (s && s.tagName != "TD") s = s.parentNode;
            s && (f = s.cellIndex);
            switch (i.className) {
            case "btn_del":
                var l = i.getAttribute("rel");
                c(function() {
                    e(r(l))
                });
                break;
            case "switch_left":
                var l = i.getAttribute("rel");
//                wd.browsers.isIE ? h(function() {
//                    o(l, f, "l")
//                }) : a(l, f, "l",
//                function() {
//                    o(l, f, "l")
//                });
                h(function() {
                    o(l, f, "l")
                })
                break;
            case "switch_right":
                var l = i.getAttribute("rel");
//                wd.browsers.isIE ? h(function() {
//                    o(l, f, "r")
//                }) : a(l, f, "r",
//                function() {
//                    o(l, f, "r")
//                })
                h(function() {
                    o(l, f, "r")
                })
            }
        }
    },
    this.changeData = function(e, t, n, r) {
        var i = null;
        for (var s = 0,
        o = e.length; s < o; s++) for (var u = 0,
        a = e[s][r + "items"].length; u < a; u++) i = e[s][r + "items"][u].valueitems[t],
        e[s][r + "items"][u].valueitems[t] = e[s][r + "items"][u].valueitems[n],
        e[s][r + "items"][u].valueitems[n] = i
    },
    this.isTop = function() {
        if (!t || t == "" || t == "0") return;
        var e = config.result.paramtypeitems,
        n = option.result.configtypeitems,
        r = e[0].paramitems[0].valueitems,
        i = r.length,
        s = 0,
        o = 0,
        u = 0;
        for (; u < i; u++) if (r[u].specid == t) {
            o = u;
            break
        }
        s != o && (this.changeData(e, s, o, "param"), this.changeData(n, s, o, "config"))
    },
    this.repsonseNavScrollLeft = function() {
        var e = document.getElementById("content"),
        t = document.createElement("div"),
        n = 0,
        r = this.Data.navMeto.item.length,
        i = [];
        t.id = "navScrollLeft",
        t.className = "followcon",
        t.style.display = "none";
        if (r > 0) {
            i.push('<ul class="folul">');
            for (; n < r; n++) i.push('<li id="folli' + (n + 1) + '"><a target="_self" href="javascript:void(0)">' + this.Data.navMeto.item[n].name + "</a></li>");
            i.push("</ul>"),
            i.push('<ul class="gnq">'),
            i.push('<li class="fhdb"><a target="_self" href="#">返回顶部</a></li>'),
            i.push("</ul>"),
            t.innerHTML = i.join("")
        }
        e.appendChild(t),
        t = null
    },
    this.navScrollLeft = function() {
        var e = this,
        t, n = wd.dom.id("navScrollLeft"),
        r = n.getElementsByTagName("li"),
        i = wd.dom.id("content"),
        s = 110,
        o = wd.browsers.isIE6,
        u = function() {
            var t = wd.abs.point(i),
            u = wd.abs.point(wd.dom.id(e.Data.navMeto.item[0].id)),
            a = wd.abs.scroll(),
            f = n.style,
            l = [];
            if (a.top > u.y - s) {
                var c = "display:block;position:" + (o ? "absolute": "fixed") + ";top:" + (o ? a.top + s: s) + "px;left:" + (t.x - 104 - (o ? 5 : a.left)) + "px";
                f.cssText = c
            } else {
                var h = "display:block;position:absolute;top:" + u.y + "px;left:" + (t.x - 104 - (o ? 5 : 0)) + "px";
                f.cssText = h
            }
            for (var p in e.Data.navMeto.item) l.push({
                dom: wd.dom.id(e.Data.navMeto.item[p].id),
                index: p
            });
            for (var d = 0,
            v = l.length; d < v; d++) {
                var m = wd.abs.point(l[d].dom).y + wd.dom.id(l[d].dom.getAttribute("pid")).offsetHeight - 35 - (s + d * 28);
                if (m > a.top) {
                    for (var g = 0,
                    y = r.length; g < y; g++) r[g].className === "active" && (r[g].className = "");
                    r[d].className = "active";
                    break
                }
            }
        };
        wd.handler.addEvent(n, "click",
        function(t) {
            t = t || window.event;
            var n = t.target || t.srcElement,
            i = wd.abs.scroll(),
            o = 0;
            if (n.tagName.toLowerCase() === "a" && n.id != "pickError" && n.id != "iknow") {
                for (var u = 0,
                a = r.length; u < a; u++) r[u].className == "active" && (r[u].className = "");
                for (var f in e.Data.navMeto.item) if (e.Data.navMeto.item[f].name == n.innerHTML) {
                    o = f;
                    break
                }
                window.scrollTo(i.left, wd.abs.point(wd.dom.id(e.Data.navMeto.item[o].id)).y - s - parseInt(f) * 28)
            }
        }),
        t = setInterval(function() {
            u()
        },
        10),
        wd.handler.addEvent(window, "scroll", u),
        wd.handler.addEvent(window, "resize", u),
        setTimeout(function() {
            clearInterval(t),
            wd.handler.addEvent(window, "scroll", u),
            wd.handler.addEvent(window, "resize", u)
        },
        1e4)
    },

    this.getCarNameById = function(e) {
        var t = config.result.paramtypeitems[0].paramitems[0].valueitems,
        n = t.length,
        r = 0,
        i = "";
        for (; r < n; r++) if (t[r].specid == e) {
            i = t[r].value;
            break
        }
        return i
    },
    this.setCookie = function(e, t) {
        var n = 30,
        r = new Date;
        r.setTime(r.getTime() + n * 24 * 60 * 60 * 1e3),
        document.cookie = e + "=" + escape(t) + ";expires=" + r.toGMTString()
    },

    this.init()
}