/* Copyright 2008-9 Google Inc. All Rights Reserved. */ (function(){var k,l=this,m=function(a){var b=typeof a;if("object"==b)if(a){if(a instanceof Array)return"array";if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if("[object Window]"==c)return"object";if("[object Array]"==c||"number"==typeof a.length&&"undefined"!=typeof a.splice&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("splice"))return"array";if("[object Function]"==c||"undefined"!=typeof a.call&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("call"))return"function"}else return"null";
else if("function"==b&&"undefined"==typeof a.call)return"object";return b},n=function(a){return"string"==typeof a},p=function(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var b=c.slice();b.push.apply(b,arguments);return a.apply(this,b)}},aa=Date.now||function(){return+new Date},r=function(a,b){a=a.split(".");var c=l;a[0]in c||!c.execScript||c.execScript("var "+a[0]);for(var d;a.length&&(d=a.shift());)a.length||void 0===b?c=c[d]?c[d]:c[d]={}:c[d]=b},t=function(a,b){function c(){}
c.prototype=b.prototype;a.v=b.prototype;a.prototype=new c;a.A=function(a,c,f){for(var d=Array(arguments.length-2),e=2;e<arguments.length;e++)d[e-2]=arguments[e];return b.prototype[c].apply(a,d)}};var u=function(a){if(Error.captureStackTrace)Error.captureStackTrace(this,u);else{var b=Error().stack;b&&(this.stack=b)}a&&(this.message=String(a))};t(u,Error);var ba=function(a,b){for(var c=a.split("%s"),d="",e=Array.prototype.slice.call(arguments,1);e.length&&1<c.length;)d+=c.shift()+e.shift();return d+c.join("%s")},v=String.prototype.trim?function(a){return a.trim()}:function(a){return a.replace(/^[\s\xa0]+|[\s\xa0]+$/g,"")},ca=String.prototype.repeat?function(a,b){return a.repeat(b)}:function(a,b){return Array(b+1).join(a)},w=function(a){a=String(a);var b=a.indexOf(".");-1==b&&(b=a.length);return ca("0",Math.max(0,2-b))+a},x=function(a,b){return a<b?
-1:a>b?1:0};var z=function(a,b){b.unshift(a);u.call(this,ba.apply(null,b));b.shift()};t(z,u);var A=function(a,b,c){if(!a){var d="Assertion failed";if(b)var d=d+(": "+b),e=Array.prototype.slice.call(arguments,2);throw new z(""+d,e||[]);}};var C=Array.prototype.indexOf?function(a,b,c){A(null!=a.length);return Array.prototype.indexOf.call(a,b,c)}:function(a,b,c){c=null==c?0:0>c?Math.max(0,a.length+c):c;if(n(a))return n(b)&&1==b.length?a.indexOf(b,c):-1;for(;c<a.length;c++)if(c in a&&a[c]===b)return c;return-1},da=Array.prototype.forEach?function(a,b,c){A(null!=a.length);Array.prototype.forEach.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=n(a)?a.split(""):a,f=0;f<d;f++)f in e&&b.call(c,e[f],f,a)},ea=Array.prototype.filter?function(a,
b,c){A(null!=a.length);return Array.prototype.filter.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=[],f=0,g=n(a)?a.split(""):a,h=0;h<d;h++)if(h in g){var B=g[h];b.call(c,B,h,a)&&(e[f++]=B)}return e},fa=function(a){var b=a.length;if(0<b){for(var c=Array(b),d=0;d<b;d++)c[d]=a[d];return c}return[]},D=function(a,b,c){A(null!=a.length);return 2>=arguments.length?Array.prototype.slice.call(a,b):Array.prototype.slice.call(a,b,c)};var E=function(a){var b=arguments.length;if(1==b&&"array"==m(arguments[0]))return E.apply(null,arguments[0]);for(var c={},d=0;d<b;d++)c[arguments[d]]=!0;return c};var F;a:{var ga=l.navigator;if(ga){var ha=ga.userAgent;if(ha){F=ha;break a}}F=""};var G=function(a){G[" "](a);return a};G[" "]=function(){};var ja=function(a,b){var c=ia;return Object.prototype.hasOwnProperty.call(c,a)?c[a]:c[a]=b(a)};var ka=-1!=F.indexOf("Opera"),H=-1!=F.indexOf("Trident")||-1!=F.indexOf("MSIE"),la=-1!=F.indexOf("Edge"),I=-1!=F.indexOf("Gecko")&&!(-1!=F.toLowerCase().indexOf("webkit")&&-1==F.indexOf("Edge"))&&!(-1!=F.indexOf("Trident")||-1!=F.indexOf("MSIE"))&&-1==F.indexOf("Edge"),J=-1!=F.toLowerCase().indexOf("webkit")&&-1==F.indexOf("Edge"),ma=function(){var a=l.document;return a?a.documentMode:void 0},K;
a:{var L="",M=function(){var a=F;if(I)return/rv\:([^\);]+)(\)|;)/.exec(a);if(la)return/Edge\/([\d\.]+)/.exec(a);if(H)return/\b(?:MSIE|rv)[: ]([^\);]+)(\)|;)/.exec(a);if(J)return/WebKit\/(\S+)/.exec(a);if(ka)return/(?:Version)[ \/]?(\S+)/.exec(a)}();M&&(L=M?M[1]:"");if(H){var N=ma();if(null!=N&&N>parseFloat(L)){K=String(N);break a}}K=L}
var na=K,ia={},O=function(a){return ja(a,function(){for(var b=0,c=v(String(na)).split("."),d=v(String(a)).split("."),e=Math.max(c.length,d.length),f=0;0==b&&f<e;f++){var g=c[f]||"",h=d[f]||"";do{g=/(\d*)(\D*)(.*)/.exec(g)||["","","",""];h=/(\d*)(\D*)(.*)/.exec(h)||["","","",""];if(0==g[0].length&&0==h[0].length)break;b=x(0==g[1].length?0:parseInt(g[1],10),0==h[1].length?0:parseInt(h[1],10))||x(0==g[2].length,0==h[2].length)||x(g[2],h[2]);g=g[3];h=h[3]}while(0==b)}return 0<=b})},P;var oa=l.document;
P=oa&&H?ma()||("CSS1Compat"==oa.compatMode?parseInt(na,10):5):void 0;!I&&!H||H&&9<=Number(P)||I&&O("1.9.1");H&&O("9");var Q=function(a,b,c){var d=document;c=c||d;var e=a&&"*"!=a?String(a).toUpperCase():"";if(c.querySelectorAll&&c.querySelector&&(e||b))return c.querySelectorAll(e+(b?"."+b:""));if(b&&c.getElementsByClassName){a=c.getElementsByClassName(b);if(e){c={};for(var f=d=0,g;g=a[f];f++)e==g.nodeName&&(c[d++]=g);c.length=d;return c}return a}a=c.getElementsByTagName(e||"*");if(b){c={};for(f=d=0;g=a[f];f++){var e=g.className,h;if(h="function"==typeof e.split)h=0<=C(e.split(/\s+/),b);h&&(c[d++]=g)}c.length=d;return c}return a};var pa=function(a){a=a.className;return n(a)&&a.match(/\S+/g)||[]},qa=function(a,b){for(var c=pa(a),d=D(arguments,1),e=c,f=0;f<d.length;f++)0<=C(e,d[f])||e.push(d[f]);c=c.join(" ");a.className=c},sa=function(a,b){var c=pa(a),d=D(arguments,1),c=ra(c,d).join(" ");a.className=c},ra=function(a,b){return ea(a,function(a){return!(0<=C(b,a))})};var ta=!H||9<=Number(P),ua=H&&!O("9");!J||O("528");I&&O("1.9b")||H&&O("8")||ka&&O("9.5")||J&&O("528");I&&!O("8")||H&&O("9");var R=function(a,b){this.type=a;this.currentTarget=this.target=b;this.defaultPrevented=this.m=!1};R.prototype.preventDefault=function(){this.defaultPrevented=!0};var S=function(a,b){R.call(this,a?a.type:"");this.relatedTarget=this.currentTarget=this.target=null;this.charCode=this.keyCode=this.button=this.screenY=this.screenX=this.clientY=this.clientX=this.offsetY=this.offsetX=0;this.metaKey=this.shiftKey=this.altKey=this.ctrlKey=!1;this.l=this.state=null;if(a){var c=this.type=a.type,d=a.changedTouches?a.changedTouches[0]:null;this.target=a.target||a.srcElement;this.currentTarget=b;if(b=a.relatedTarget){if(I){var e;a:{try{G(b.nodeName);e=!0;break a}catch(f){}e=
!1}e||(b=null)}}else"mouseover"==c?b=a.fromElement:"mouseout"==c&&(b=a.toElement);this.relatedTarget=b;null===d?(this.offsetX=J||void 0!==a.offsetX?a.offsetX:a.layerX,this.offsetY=J||void 0!==a.offsetY?a.offsetY:a.layerY,this.clientX=void 0!==a.clientX?a.clientX:a.pageX,this.clientY=void 0!==a.clientY?a.clientY:a.pageY,this.screenX=a.screenX||0,this.screenY=a.screenY||0):(this.clientX=void 0!==d.clientX?d.clientX:d.pageX,this.clientY=void 0!==d.clientY?d.clientY:d.pageY,this.screenX=d.screenX||0,
this.screenY=d.screenY||0);this.button=a.button;this.keyCode=a.keyCode||0;this.charCode=a.charCode||("keypress"==c?a.keyCode:0);this.ctrlKey=a.ctrlKey;this.altKey=a.altKey;this.shiftKey=a.shiftKey;this.metaKey=a.metaKey;this.state=a.state;this.l=a;a.defaultPrevented&&this.preventDefault()}};t(S,R);
S.prototype.preventDefault=function(){S.v.preventDefault.call(this);var a=this.l;if(a.preventDefault)a.preventDefault();else if(a.returnValue=!1,ua)try{if(a.ctrlKey||112<=a.keyCode&&123>=a.keyCode)a.keyCode=-1}catch(b){}};var va="closure_listenable_"+(1E6*Math.random()|0),wa=0;var xa=function(a,b,c,d,e){this.listener=a;this.f=null;this.src=b;this.type=c;this.h=!!d;this.i=e;this.key=++wa;this.c=this.g=!1},ya=function(a){a.c=!0;a.listener=null;a.f=null;a.src=null;a.i=null};var T=function(a){this.src=a;this.b={};this.j=0};T.prototype.add=function(a,b,c,d,e){var f=a.toString();a=this.b[f];a||(a=this.b[f]=[],this.j++);var g;a:{for(g=0;g<a.length;++g){var h=a[g];if(!h.c&&h.listener==b&&h.h==!!d&&h.i==e)break a}g=-1}-1<g?(b=a[g],c||(b.g=!1)):(b=new xa(b,this.src,f,!!d,e),b.g=c,a.push(b));return b};
var za=function(a,b){var c=b.type;if(c in a.b){var d=a.b[c],e=C(d,b),f;if(f=0<=e)A(null!=d.length),Array.prototype.splice.call(d,e,1);f&&(ya(b),0==a.b[c].length&&(delete a.b[c],a.j--))}};var U="closure_lm_"+(1E6*Math.random()|0),V={},Aa=0,Ca=function(){var a=Ba,b=ta?function(c){return a.call(b.src,b.listener,c)}:function(c){c=a.call(b.src,b.listener,c);if(!c)return c};return b},Da=function(a,b,c,d,e){if("array"==m(b))for(var f=0;f<b.length;f++)Da(a,b[f],c,d,e);else if(c=Ea(c),a&&a[va])a.s.add(String(b),c,!0,d,e);else{if(!b)throw Error("Invalid event type");var f=!!d,g=W(a);g||(a[U]=g=new T(a));c=g.add(b,c,!0,d,e);if(!c.f){d=Ca();c.f=d;d.src=a;d.listener=c;if(a.addEventListener)a.addEventListener(b.toString(),
d,f);else if(a.attachEvent)a.attachEvent(Fa(b.toString()),d);else throw Error("addEventListener and attachEvent are unavailable.");Aa++}}},Fa=function(a){return a in V?V[a]:V[a]="on"+a},Ha=function(a,b,c,d){var e=!0;if(a=W(a))if(b=a.b[b.toString()])for(b=b.concat(),a=0;a<b.length;a++){var f=b[a];f&&f.h==c&&!f.c&&(f=Ga(f,d),e=e&&!1!==f)}return e},Ga=function(a,b){var c=a.listener,d=a.i||a.src;if(a.g&&"number"!=typeof a&&a&&!a.c){var e=a.src;if(e&&e[va])za(e.s,a);else{var f=a.type,g=a.f;e.removeEventListener?
e.removeEventListener(f,g,a.h):e.detachEvent&&e.detachEvent(Fa(f),g);Aa--;(f=W(e))?(za(f,a),0==f.j&&(f.src=null,e[U]=null)):ya(a)}}return c.call(d,b)},Ba=function(a,b){if(a.c)return!0;if(!ta){if(!b)a:{b=["window","event"];for(var c=l,d;d=b.shift();)if(null!=c[d])c=c[d];else{b=null;break a}b=c}d=b;b=new S(d,this);c=!0;if(!(0>d.keyCode||void 0!=d.returnValue)){a:{var e=!1;if(0==d.keyCode)try{d.keyCode=-1;break a}catch(g){e=!0}if(e||void 0==d.returnValue)d.returnValue=!0}d=[];for(e=b.currentTarget;e;e=
e.parentNode)d.push(e);a=a.type;for(e=d.length-1;!b.m&&0<=e;e--){b.currentTarget=d[e];var f=Ha(d[e],a,!0,b),c=c&&f}for(e=0;!b.m&&e<d.length;e++)b.currentTarget=d[e],f=Ha(d[e],a,!1,b),c=c&&f}return c}return Ga(a,new S(b,this))},W=function(a){a=a[U];return a instanceof T?a:null},X="__closure_events_fn_"+(1E9*Math.random()>>>0),Ea=function(a){A(a,"Listener can not be null.");if("function"==m(a))return a;A(a.handleEvent,"An object listener must have handleEvent method.");a[X]||(a[X]=function(b){return a.handleEvent(b)});
return a[X]};var Z=function(a,b,c){"number"==typeof a?(this.a=Ia(a,b||0,c||1),Y(this,c||1)):(b=typeof a,"object"==b&&null!=a||"function"==b?(this.a=Ia(a.getFullYear(),a.getMonth(),a.getDate()),Y(this,a.getDate())):(this.a=new Date(aa()),a=this.a.getDate(),this.a.setHours(0),this.a.setMinutes(0),this.a.setSeconds(0),this.a.setMilliseconds(0),Y(this,a)))},Ia=function(a,b,c){b=new Date(a,b,c);0<=a&&100>a&&b.setFullYear(b.getFullYear()-1900);return b};k=Z.prototype;k.getFullYear=function(){return this.a.getFullYear()};
k.getYear=function(){return this.getFullYear()};k.getMonth=function(){return this.a.getMonth()};k.getDate=function(){return this.a.getDate()};k.getTime=function(){return this.a.getTime()};k.getUTCHours=function(){return this.a.getUTCHours()};k.setFullYear=function(a){this.a.setFullYear(a)};k.setMonth=function(a){this.a.setMonth(a)};k.setDate=function(a){this.a.setDate(a)};
k.add=function(a){if(a.w||a.u){var b=this.getMonth()+a.u+12*a.w,c=this.getYear()+Math.floor(b/12),b=b%12;0>b&&(b+=12);var d;a:{switch(b){case 1:d=0!=c%4||0==c%100&&0!=c%400?28:29;break a;case 5:case 8:case 10:case 3:d=30;break a}d=31}d=Math.min(d,this.getDate());this.setDate(1);this.setFullYear(c);this.setMonth(b);this.setDate(d)}a.o&&(b=new Date(this.getYear(),this.getMonth(),this.getDate(),12),a=new Date(b.getTime()+864E5*a.o),this.setDate(1),this.setFullYear(a.getFullYear()),this.setMonth(a.getMonth()),
this.setDate(a.getDate()),Y(this,a.getDate()))};k.toString=function(){return[this.getFullYear(),w(this.getMonth()+1),w(this.getDate())].join("")+""};var Y=function(a,b){a.getDate()!=b&&(b=a.getDate()<b?1:-1,a.a.setUTCHours(a.a.getUTCHours()+b))};Z.prototype.valueOf=function(){return this.a.valueOf()};E("A AREA BUTTON HEAD INPUT LINK MENU META OPTGROUP OPTION PROGRESS STYLE SELECT SOURCE TEXTAREA TITLE TRACK".split(" "));new Z(0,0,1);new Z(9999,11,31);H||la||J&&O("525");r("ae.init",function(){Ja();Ka();Da(window,"load",function(){});La()});
var Ja=function(){var a;a=document;if(a=n("ae-content")?a.getElementById("ae-content"):"ae-content"){a=Q("table","ae-table-striped",a);for(var b=0,c;c=a[b];b++){c=Q("tbody",null,c);for(var d=0,e;e=c[d];d++){e=Q("tr",null,e);for(var f=0,g;g=e[f];f++)f%2&&qa(g,"ae-even")}}}},Ka=function(){var a=Q(null,"ae-noscript",void 0);da(fa(a),function(a){sa(a,"ae-noscript")})},La=function(){l._gaq=l._gaq||[];l._gaq.push(function(){l._gaq._createAsyncTracker("UA-3739047-3","ae")._trackPageview()});(function(){var a=
document.createElement("script");a.src=("https:"==document.location.protocol?"https://ssl":"http://www")+".google-analytics.com/ga.js";a.setAttribute("async","true");document.documentElement.firstChild.appendChild(a)})()};r("ae.trackPageView",function(){l._gaq&&l._gaq._getAsyncTracker("ae")._trackPageview()});var Na=function(a){if(void 0==a||null==a||0==a.length)return 0;a=Math.max.apply(Math,a);return Ma(a)},Ma=function(a){var b=5;2>b&&(b=2);--b;return Math.ceil(a/b)*b},Oa=function(a,b,c){a=a.getSelection();1==a.length&&(a=a[0],null!=a.row&&(null!=b.starttime&&(c+="&starttime="+b.starttime),null!=b.endtime&&(c+="&endtime="+b.endtime),null!=b.latency_lower&&(c+="&latency_lower="+b.latency_lower),null!=b.latency_upper&&(c+="&latency_upper="+b.latency_upper),b=c+"&detail="+a.row,window.location.href=b))},
Pa=function(a,b,c,d,e){var f=new google.visualization.DataTable;f.addColumn("string","");f.addColumn("number","");f.addColumn({type:"string",role:"tooltip"});for(var g=0;g<b.length;g++)f.addRow(["",b[g],c[g]]);c=Math.max(10*b.length,200);b=Na(b);a=new google.visualization.ColumnChart(document.getElementById("rpctime-"+a));a.draw(f,{height:100,width:c,legend:"none",chartArea:{left:40},fontSize:11,vAxis:{minValue:0,maxValue:b,gridlines:{count:5}}});google.visualization.events.addListener(a,"select",
p(Oa,a,d,e))};r("ae.Charts.latencyHistogram",function(a,b,c){var d=new google.visualization.DataTable;d.addColumn("string","");d.addColumn("number","");for(var e=0;e<b.length;e++)d.addRow([""+a[e],b[e]]);for(e=b.length;e<a.length;e++)d.addRow([""+a[e],0]);b=Na(b);(new google.visualization.ColumnChart(document.getElementById("latency-"+c))).draw(d,{legend:"none",width:20*a.length,height:200,vAxis:{maxValue:b,gridlines:{count:5}}})});
r("ae.Charts.latencyTimestampScatter",function(a,b,c,d,e){var f=new google.visualization.DataTable;f.addColumn("number","Time (seconds from start)");f.addColumn("number","Latency");for(var g=0;g<a.length;g++)f.addRow([Math.round(a[g]-c),b[g]]);a=d.starttime?d.starttime:0;b=new google.visualization.ScatterChart(document.getElementById("LatencyVsTimestamp"));b.draw(f,{hAxis:{title:"Time (seconds from start of recording)",minValue:a},vAxis:{title:"Request Latency (milliseconds)",minValue:0},tooltip:{trigger:"none"},
legend:"none"});google.visualization.events.addListener(b,"select",p(Oa,b,d,e))});
r("ae.Charts.entityCountBarChart",function(a,b,c,d){var e=new google.visualization.DataTable;e.addColumn("string","");e.addColumn("number","Reads");e.addColumn({type:"string",role:"tooltip"});e.addColumn("number","Misses");e.addColumn({type:"string",role:"tooltip"});e.addColumn("number","Writes");e.addColumn({type:"string",role:"tooltip"});var f=50;f>b.length&&(f=b.length);for(var g=0;g<f;g++)e.addRow(["",b[g][1]-b[g][3],b[g][0],b[g][3],b[g][0],b[g][2],b[g][0]]);b=20*f;f=b+130;(new google.visualization.ColumnChart(document.getElementById(d+
"-"+a))).draw(e,{height:100,width:f,chartArea:{width:b},fontSize:10,isStacked:!0,vAxis:{minValue:0,maxValue:Ma(c),gridlines:{count:5}}})});
r("ae.Charts.rpcVariationCandlestick",function(a){var b=new google.visualization.DataTable;b.addColumn("string","");b.addColumn("number","");b.addColumn("number","");b.addColumn("number","");b.addColumn("number","");b.addRows(a);(new google.visualization.CandlestickChart(document.getElementById("rpcvariation"))).draw(b,{vAxis:{title:"RPC Latency variation (milliseconds)"},hAxis:{textPosition:"out",slantedText:!0,slantedTextAngle:45,textStyle:{fontSize:13}},height:250,chartArea:{top:10,height:100},
legend:"none",tooltip:{trigger:"none"}})});r("ae.Charts.totalTimeBarChart",function(a,b,c,d){for(var e=[],f=0;f<b.length;f++)e[f]=b[f]+" milliseconds";Pa(a,b,e,c,d)});r("ae.Charts.rpcTimeBarChart",function(a,b,c,d,e){var f=[],g=[],h=c.indices,B=c.times;c=c.stats;for(var q=0;q<b;q++)f[q]=0,g[q]=null;for(q=0;q<h.length;q++){f[h[q]]=B[q];b=c[q];var y="Calls: "+b[0];if(0<b[1]||0<b[2]||0<b[3])y+=" Entities";0<b[1]&&(y+=" R:"+b[1]);0<b[2]&&(y+=" W:"+b[2]);0<b[3]&&(y+=" M:"+b[3]);g[h[q]]=y}Pa(a,f,g,d,e)});})();
