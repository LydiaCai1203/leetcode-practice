(window["nojMonomainWebpackJsonpproduction"]=window["nojMonomainWebpackJsonpproduction"]||[]).push([[227],{bqB3:function(t,n,e){"use strict";var r="http://www.w3.org/1999/xhtml";var i={svg:"http://www.w3.org/2000/svg",xhtml:r,xlink:"http://www.w3.org/1999/xlink",xml:"http://www.w3.org/XML/1998/namespace",xmlns:"http://www.w3.org/2000/xmlns/"};var u=function(t){var n=t+="",e=n.indexOf(":");if(e>=0&&(n=t.slice(0,e))!=="xmlns")t=t.slice(e+1);return i.hasOwnProperty(n)?{space:i[n],local:t}:t};function o(e){return function(){var t=this.ownerDocument,n=this.namespaceURI;return n===r&&t.documentElement.namespaceURI===r?t.createElement(e):t.createElementNS(n,e)}}function a(t){return function(){return this.ownerDocument.createElementNS(t.space,t.local)}}var s=function(t){var n=u(t);return(n.local?a:o)(n)};function c(){}var l=function(t){return t==null?c:function(){return this.querySelector(t)}};var f=function(t){if(typeof t!=="function")t=l(t);for(var n=this._groups,e=n.length,r=new Array(e),i=0;i<e;++i){for(var u=n[i],o=u.length,a=r[i]=new Array(o),s,c,f=0;f<o;++f){if((s=u[f])&&(c=t.call(s,s.__data__,f,u))){if("__data__"in s)c.__data__=s.__data__;a[f]=c}}}return new Xt(r,this._parents)};function h(){return[]}var p=function(t){return t==null?h:function(){return this.querySelectorAll(t)}};var v=function(t){if(typeof t!=="function")t=p(t);for(var n=this._groups,e=n.length,r=[],i=[],u=0;u<e;++u){for(var o=n[u],a=o.length,s,c=0;c<a;++c){if(s=o[c]){r.push(t.call(s,s.__data__,c,o));i.push(s)}}}return new Xt(r,i)};var _=function(t){return function(){return this.matches(t)}};var d=function(t){if(typeof t!=="function")t=_(t);for(var n=this._groups,e=n.length,r=new Array(e),i=0;i<e;++i){for(var u=n[i],o=u.length,a=r[i]=[],s,c=0;c<o;++c){if((s=u[c])&&t.call(s,s.__data__,c,u)){a.push(s)}}}return new Xt(r,this._parents)};var y=function(t){return new Array(t.length)};var m=function(){return new Xt(this._enter||this._groups.map(y),this._parents)};function g(t,n){this.ownerDocument=t.ownerDocument;this.namespaceURI=t.namespaceURI;this._next=null;this._parent=t;this.__data__=n}g.prototype={constructor:g,appendChild:function(t){return this._parent.insertBefore(t,this._next)},insertBefore:function(t,n){return this._parent.insertBefore(t,n)},querySelector:function(t){return this._parent.querySelector(t)},querySelectorAll:function(t){return this._parent.querySelectorAll(t)}};var x=function(t){return function(){return t}};var w="$";function S(t,n,e,r,i,u){var o=0,a,s=n.length,c=u.length;for(;o<c;++o){if(a=n[o]){a.__data__=u[o];r[o]=a}else{e[o]=new g(t,u[o])}}for(;o<s;++o){if(a=n[o]){i[o]=a}}}function b(t,n,e,r,i,u,o){var a,s,c={},f=n.length,l=u.length,h=new Array(f),p;for(a=0;a<f;++a){if(s=n[a]){h[a]=p=w+o.call(s,s.__data__,a,n);if(p in c){i[a]=s}else{c[p]=s}}}for(a=0;a<l;++a){p=w+o.call(t,u[a],a,u);if(s=c[p]){r[a]=s;s.__data__=u[a];c[p]=null}else{e[a]=new g(t,u[a])}}for(a=0;a<f;++a){if((s=n[a])&&c[h[a]]===s){i[a]=s}}}var A=function(t,n){if(!t){p=new Array(this.size()),c=-1;this.each(function(t){p[++c]=t});return p}var e=n?b:S,r=this._parents,i=this._groups;if(typeof t!=="function")t=x(t);for(var u=i.length,o=new Array(u),a=new Array(u),s=new Array(u),c=0;c<u;++c){var f=r[c],l=i[c],h=l.length,p=t.call(f,f&&f.__data__,c,r),v=p.length,_=a[c]=new Array(v),d=o[c]=new Array(v),y=s[c]=new Array(h);e(f,l,_,d,y,p,n);for(var m=0,g=0,w,A;m<v;++m){if(w=_[m]){if(m>=g)g=m+1;while(!(A=d[g])&&++g<v);w._next=A||null}}}o=new Xt(o,r);o._enter=a;o._exit=s;return o};var E=function(){return new Xt(this._exit||this._groups.map(y),this._parents)};var N=function(t,n,e){var r=this.enter(),i=this,u=this.exit();r=typeof t==="function"?t(r):r.append(t+"");if(n!=null)i=n(i);if(e==null)u.remove();else e(u);return r&&i?r.merge(i).order():i};var C=function(t){for(var n=this._groups,e=t._groups,r=n.length,i=e.length,u=Math.min(r,i),o=new Array(r),a=0;a<u;++a){for(var s=n[a],c=e[a],f=s.length,l=o[a]=new Array(f),h,p=0;p<f;++p){if(h=s[p]||c[p]){l[p]=h}}}for(;a<r;++a){o[a]=n[a]}return new Xt(o,this._parents)};var P=function(){for(var t=this._groups,n=-1,e=t.length;++n<e;){for(var r=t[n],i=r.length-1,u=r[i],o;--i>=0;){if(o=r[i]){if(u&&o.compareDocumentPosition(u)^4)u.parentNode.insertBefore(o,u);u=o}}}return this};var L=function(e){if(!e)e=T;function t(t,n){return t&&n?e(t.__data__,n.__data__):!t-!n}for(var n=this._groups,r=n.length,i=new Array(r),u=0;u<r;++u){for(var o=n[u],a=o.length,s=i[u]=new Array(a),c,f=0;f<a;++f){if(c=o[f]){s[f]=c}}s.sort(t)}return new Xt(i,this._parents).order()};function T(t,n){return t<n?-1:t>n?1:t>=n?0:NaN}var B=function(){var t=arguments[0];arguments[0]=this;t.apply(null,arguments);return this};var q=function(){var t=new Array(this.size()),n=-1;this.each(function(){t[++n]=this});return t};var M=function(){for(var t=this._groups,n=0,e=t.length;n<e;++n){for(var r=t[n],i=0,u=r.length;i<u;++i){var o=r[i];if(o)return o}}return null};var D=function(){var t=0;this.each(function(){++t});return t};var O=function(){return!this.node()};var V=function(t){for(var n=this._groups,e=0,r=n.length;e<r;++e){for(var i=n[e],u=0,o=i.length,a;u<o;++u){if(a=i[u])t.call(a,a.__data__,u,i)}}return this};function j(t){return function(){this.removeAttribute(t)}}function k(t){return function(){this.removeAttributeNS(t.space,t.local)}}function R(t,n){return function(){this.setAttribute(t,n)}}function H(t,n){return function(){this.setAttributeNS(t.space,t.local,n)}}function I(n,e){return function(){var t=e.apply(this,arguments);if(t==null)this.removeAttribute(n);else this.setAttribute(n,t)}}function U(n,e){return function(){var t=e.apply(this,arguments);if(t==null)this.removeAttributeNS(n.space,n.local);else this.setAttributeNS(n.space,n.local,t)}}var z=function(t,n){var e=u(t);if(arguments.length<2){var r=this.node();return e.local?r.getAttributeNS(e.space,e.local):r.getAttribute(e)}return this.each((n==null?e.local?k:j:typeof n==="function"?e.local?U:I:e.local?H:R)(e,n))};var G=function(t){return t.ownerDocument&&t.ownerDocument.defaultView||t.document&&t||t.defaultView};function X(t){return function(){this.style.removeProperty(t)}}function J(t,n,e){return function(){this.style.setProperty(t,n,e)}}function W(n,e,r){return function(){var t=e.apply(this,arguments);if(t==null)this.style.removeProperty(n);else this.style.setProperty(n,t,r)}}var Y=function(t,n,e){return arguments.length>1?this.each((n==null?X:typeof n==="function"?W:J)(t,n,e==null?"":e)):$(this.node(),t)};function $(t,n){return t.style.getPropertyValue(n)||G(t).getComputedStyle(t,null).getPropertyValue(n)}function F(t){return function(){delete this[t]}}function K(t,n){return function(){this[t]=n}}function Q(n,e){return function(){var t=e.apply(this,arguments);if(t==null)delete this[n];else this[n]=t}}var Z=function(t,n){return arguments.length>1?this.each((n==null?F:typeof n==="function"?Q:K)(t,n)):this.node()[t]};function tt(t){return t.trim().split(/^|\s+/)}function nt(t){return t.classList||new et(t)}function et(t){this._node=t;this._names=tt(t.getAttribute("class")||"")}et.prototype={add:function(t){var n=this._names.indexOf(t);if(n<0){this._names.push(t);this._node.setAttribute("class",this._names.join(" "))}},remove:function(t){var n=this._names.indexOf(t);if(n>=0){this._names.splice(n,1);this._node.setAttribute("class",this._names.join(" "))}},contains:function(t){return this._names.indexOf(t)>=0}};function rt(t,n){var e=nt(t),r=-1,i=n.length;while(++r<i)e.add(n[r])}function it(t,n){var e=nt(t),r=-1,i=n.length;while(++r<i)e.remove(n[r])}function ut(t){return function(){rt(this,t)}}function ot(t){return function(){it(this,t)}}function at(t,n){return function(){(n.apply(this,arguments)?rt:it)(this,t)}}var st=function(t,n){var e=tt(t+"");if(arguments.length<2){var r=nt(this.node()),i=-1,u=e.length;while(++i<u)if(!r.contains(e[i]))return false;return true}return this.each((typeof n==="function"?at:n?ut:ot)(e,n))};function ct(){this.textContent=""}function ft(t){return function(){this.textContent=t}}function lt(n){return function(){var t=n.apply(this,arguments);this.textContent=t==null?"":t}}var ht=function(t){return arguments.length?this.each(t==null?ct:(typeof t==="function"?lt:ft)(t)):this.node().textContent};function pt(){this.innerHTML=""}function vt(t){return function(){this.innerHTML=t}}function _t(n){return function(){var t=n.apply(this,arguments);this.innerHTML=t==null?"":t}}var dt=function(t){return arguments.length?this.each(t==null?pt:(typeof t==="function"?_t:vt)(t)):this.node().innerHTML};function yt(){if(this.nextSibling)this.parentNode.appendChild(this)}var mt=function(){return this.each(yt)};function gt(){if(this.previousSibling)this.parentNode.insertBefore(this,this.parentNode.firstChild)}var wt=function(){return this.each(gt)};var At=function(t){var n=typeof t==="function"?t:s(t);return this.select(function(){return this.appendChild(n.apply(this,arguments))})};function xt(){return null}var St=function(t,n){var e=typeof t==="function"?t:s(t),r=n==null?xt:typeof n==="function"?n:l(n);return this.select(function(){return this.insertBefore(e.apply(this,arguments),r.apply(this,arguments)||null)})};function bt(){var t=this.parentNode;if(t)t.removeChild(this)}var Et=function(){return this.each(bt)};function Nt(){return this.parentNode.insertBefore(this.cloneNode(false),this.nextSibling)}function Ct(){return this.parentNode.insertBefore(this.cloneNode(true),this.nextSibling)}var Pt=function(t){return this.select(t?Ct:Nt)};var Lt=function(t){return arguments.length?this.property("__data__",t):this.node().__data__};var Tt={};var Bt=null;if(typeof document!=="undefined"){var qt=document.documentElement;if(!("onmouseenter"in qt)){Tt={mouseenter:"mouseover",mouseleave:"mouseout"}}}function Mt(e,t,n){e=Dt(e,t,n);return function(t){var n=t.relatedTarget;if(!n||n!==this&&!(n.compareDocumentPosition(this)&8)){e.call(this,t)}}}function Dt(e,r,i){return function(t){var n=Bt;Bt=t;try{e.call(this,this.__data__,r,i)}finally{Bt=n}}}function Ot(t){return t.trim().split(/^|\s+/).map(function(t){var n="",e=t.indexOf(".");if(e>=0)n=t.slice(e+1),t=t.slice(0,e);return{type:t,name:n}})}function Vt(u){return function(){var t=this.__on;if(!t)return;for(var n=0,e=-1,r=t.length,i;n<r;++n){if(i=t[n],(!u.type||i.type===u.type)&&i.name===u.name){this.removeEventListener(i.type,i.listener,i.capture)}else{t[++e]=i}}if(++e)t.length=e;else delete this.__on}}function jt(s,c,f){var l=Tt.hasOwnProperty(s.type)?Mt:Dt;return function(t,n,e){var r=this.__on,i,u=l(c,n,e);if(r)for(var o=0,a=r.length;o<a;++o){if((i=r[o]).type===s.type&&i.name===s.name){this.removeEventListener(i.type,i.listener,i.capture);this.addEventListener(i.type,i.listener=u,i.capture=f);i.value=c;return}}this.addEventListener(s.type,u,f);i={type:s.type,name:s.name,value:c,listener:u,capture:f};if(!r)this.__on=[i];else r.push(i)}}var kt=function(t,n,e){var r=Ot(t+""),i,u=r.length,o;if(arguments.length<2){var a=this.node().__on;if(a)for(var s=0,c=a.length,f;s<c;++s){for(i=0,f=a[s];i<u;++i){if((o=r[i]).type===f.type&&o.name===f.name){return f.value}}}return}a=n?jt:Vt;if(e==null)e=false;for(i=0;i<u;++i)this.each(a(r[i],n,e));return this};function Rt(t,n,e,r){var i=Bt;t.sourceEvent=Bt;Bt=t;try{return n.apply(e,r)}finally{Bt=i}}function Ht(t,n,e){var r=G(t),i=r.CustomEvent;if(typeof i==="function"){i=new i(n,e)}else{i=r.document.createEvent("Event");if(e)i.initEvent(n,e.bubbles,e.cancelable),i.detail=e.detail;else i.initEvent(n,false,false)}t.dispatchEvent(i)}function It(t,n){return function(){return Ht(this,t,n)}}function Ut(t,n){return function(){return Ht(this,t,n.apply(this,arguments))}}var zt=function(t,n){return this.each((typeof n==="function"?Ut:It)(t,n))};var Gt=[null];function Xt(t,n){this._groups=t;this._parents=n}function Jt(){return new Xt([[document.documentElement]],Gt)}Xt.prototype=Jt.prototype={constructor:Xt,select:f,selectAll:v,filter:d,data:A,enter:m,exit:E,join:N,merge:C,order:P,sort:L,call:B,nodes:q,node:M,size:D,empty:O,each:V,attr:z,style:Y,property:Z,classed:st,text:ht,html:dt,raise:mt,lower:wt,append:At,insert:St,remove:Et,clone:Pt,datum:Lt,on:kt,dispatch:zt};var Wt=Jt;var Yt=function(t){return typeof t==="string"?new Xt([[document.querySelector(t)]],[document.documentElement]):new Xt([[t]],Gt)};var $t=function(t){return Yt(s(t).call(document.documentElement))};var Ft=0;function Kt(){return new Qt}function Qt(){this._="@"+(++Ft).toString(36)}Qt.prototype=Kt.prototype={constructor:Qt,get:function(t){var n=this._;while(!(n in t))if(!(t=t.parentNode))return;return t[n]},set:function(t,n){return t[this._]=n},remove:function(t){return this._ in t&&delete t[this._]},toString:function(){return this._}};var Zt=function(){var t=Bt,n;while(n=t.sourceEvent)t=n;return t};var tn=function(t,n){var e=t.ownerSVGElement||t;if(e.createSVGPoint){var r=e.createSVGPoint();r.x=n.clientX,r.y=n.clientY;r=r.matrixTransform(t.getScreenCTM().inverse());return[r.x,r.y]}var i=t.getBoundingClientRect();return[n.clientX-i.left-t.clientLeft,n.clientY-i.top-t.clientTop]};var nn=function(t){var n=Zt();if(n.changedTouches)n=n.changedTouches[0];return tn(t,n)};var en=function(t){return typeof t==="string"?new Xt([document.querySelectorAll(t)],[document.documentElement]):new Xt([t==null?[]:t],Gt)};var rn=function(t,n,e){if(arguments.length<3)e=n,n=Zt().changedTouches;for(var r=0,i=n?n.length:0,u;r<i;++r){if((u=n[r]).identifier===e){return tn(t,u)}}return null};var un=function(t,n){if(n==null)n=Zt().touches;for(var e=0,r=n?n.length:0,i=new Array(r);e<r;++e){i[e]=tn(t,n[e])}return i};e.d(n,"c",function(){return _});e.d(n,"d",function(){return nn});e.d(n,"e",function(){return u});e.d(n,"f",function(){return Yt});e.d(n,"g",function(){return Wt});e.d(n,"h",function(){return l});e.d(n,"i",function(){return p});e.d(n,"j",function(){return $});e.d(n,"k",function(){return rn});e.d(n,"b",function(){return Bt});e.d(n,"a",function(){return Rt})}}]);