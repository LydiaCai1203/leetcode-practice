(window["nojMonomainWebpackJsonpproduction"]=window["nojMonomainWebpackJsonpproduction"]||[]).push([[223],{qHL8:function(n,t,r){"use strict";function e(n){if(!n.ok)throw new Error(n.status+" "+n.statusText);return n.blob()}var o=function(n,t){return fetch(n,t).then(e)};function u(n){if(!n.ok)throw new Error(n.status+" "+n.statusText);return n.arrayBuffer()}var i=function(n,t){return fetch(n,t).then(u)};var f=r("iPNY");function a(n){if(!n.ok)throw new Error(n.status+" "+n.statusText);return n.text()}var c=function(n,t){return fetch(n,t).then(a)};function s(e){return function(n,t,r){if(arguments.length===2&&typeof t==="function")r=t,t=undefined;return c(n,t).then(function(n){return e(n,r)})}}function h(n,t,r,e){if(arguments.length===3&&typeof r==="function")e=r,r=undefined;var o=Object(f["b"])(n);return c(t,r).then(function(n){return o.parse(n,e)})}var v=s(f["a"]);var w=s(f["c"]);var p=function(o,u){return new Promise(function(n,t){var r=new Image;for(var e in u)r[e]=u[e];r.onerror=t;r.onload=function(){n(r)};r.src=o})};function d(n){if(!n.ok)throw new Error(n.status+" "+n.statusText);return n.json()}var m=function(n,t){return fetch(n,t).then(d)};function l(r){return function(n,t){return c(n,t).then(function(n){return(new DOMParser).parseFromString(n,r)})}}var x=l("application/xml");var b=l("text/html");var g=l("image/svg+xml")}}]);