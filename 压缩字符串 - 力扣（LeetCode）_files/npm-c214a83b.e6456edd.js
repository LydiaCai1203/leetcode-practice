/*! For license information please see npm-c214a83b.e6456edd.js.LICENSE */
(window["nojMonomainWebpackJsonpproduction"]=window["nojMonomainWebpackJsonpproduction"]||[]).push([[184],{ssRi:function(n,U,V){(function(T,W){var L;(function(n){var r=true&&U&&!U.nodeType&&U;var e=true&&T&&!T.nodeType&&T;var o=typeof W=="object"&&W;if(o.global===o||o.window===o||o.self===o){n=o}var t,g=2147483647,b=36,C=1,x=26,i=38,f=700,j=72,A=128,I="-",u=/^xn--/,a=/[^\x20-\x7E]/,c=/[\x2E\u3002\uFF0E\uFF61]/g,l={overflow:"Overflow: input needs wider integers to process","not-basic":"Illegal input >= 0x80 (not a basic code point)","invalid-input":"Invalid input"},s=b-C,k=Math.floor,E=String.fromCharCode,p;function F(n){throw new RangeError(l[n])}function d(n,r){var e=n.length;var o=[];while(e--){o[e]=r(n[e])}return o}function h(n,r){var e=n.split("@");var o="";if(e.length>1){o=e[0]+"@";n=e[1]}n=n.replace(c,".");var t=n.split(".");var i=d(t,r).join(".");return o+i}function m(n){var r=[],e=0,o=n.length,t,i;while(e<o){t=n.charCodeAt(e++);if(t>=55296&&t<=56319&&e<o){i=n.charCodeAt(e++);if((i&64512)==56320){r.push(((t&1023)<<10)+(i&1023)+65536)}else{r.push(t);e--}}else{r.push(t)}}return r}function w(n){return d(n,function(n){var r="";if(n>65535){n-=65536;r+=E(n>>>10&1023|55296);n=56320|n&1023}r+=E(n);return r}).join("")}function y(n){if(n-48<10){return n-22}if(n-65<26){return n-65}if(n-97<26){return n-97}return b}function M(n,r){return n+22+75*(n<26)-((r!=0)<<5)}function R(n,r,e){var o=0;n=e?k(n/f):n>>1;n+=k(n/r);for(;n>s*x>>1;o+=b){n=k(n/s)}return k(o+(s+1)*n/(n+i))}function v(n){var r=[],e=n.length,o,t=0,i=A,f=j,u,a,c,l,s,p,d,h,v;u=n.lastIndexOf(I);if(u<0){u=0}for(a=0;a<u;++a){if(n.charCodeAt(a)>=128){F("not-basic")}r.push(n.charCodeAt(a))}for(c=u>0?u+1:0;c<e;){for(l=t,s=1,p=b;;p+=b){if(c>=e){F("invalid-input")}d=y(n.charCodeAt(c++));if(d>=b||d>k((g-t)/s)){F("overflow")}t+=d*s;h=p<=f?C:p>=f+x?x:p-f;if(d<h){break}v=b-h;if(s>k(g/v)){F("overflow")}s*=v}o=r.length+1;f=R(t-l,o,l==0);if(k(t/o)>g-i){F("overflow")}i+=k(t/o);t%=o;r.splice(t++,0,i)}return w(r)}function S(n){var r,e,o,t,i,f,u,a,c,l,s,p=[],d,h,v,w;n=m(n);d=n.length;r=A;e=0;i=j;for(f=0;f<d;++f){s=n[f];if(s<128){p.push(E(s))}}o=t=p.length;if(t){p.push(I)}while(o<d){for(u=g,f=0;f<d;++f){s=n[f];if(s>=r&&s<u){u=s}}h=o+1;if(u-r>k((g-e)/h)){F("overflow")}e+=(u-r)*h;r=u;for(f=0;f<d;++f){s=n[f];if(s<r&&++e>g){F("overflow")}if(s==r){for(a=e,c=b;;c+=b){l=c<=i?C:c>=i+x?x:c-i;if(a<l){break}w=a-l;v=b-l;p.push(E(M(l+w%v,0)));a=k(w/v)}p.push(E(M(a,0)));i=R(e,h,o==t);e=0;++o}}++e;++r}return p.join("")}function J(n){return h(n,function(n){return u.test(n)?v(n.slice(4).toLowerCase()):n})}function O(n){return h(n,function(n){return a.test(n)?"xn--"+S(n):n})}t={version:"1.4.1",ucs2:{decode:m,encode:w},decode:v,encode:S,toASCII:O,toUnicode:J};if(true){!(L=function(){return t}.call(U,V,U,T),L!==undefined&&(T.exports=L))}else{}})(this)}).call(this,V("aYSr")(n),V("fRV1"))}}]);