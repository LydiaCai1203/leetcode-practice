(window["nojMonomainWebpackJsonpproduction"]=window["nojMonomainWebpackJsonpproduction"]||[]).push([[130],{KQfC:function(t,n,e){"use strict";var a=e("ERkP");var r=e.n(a);var o=e("W/Kd");var s=e.n(o);var i=e("aWzz");var c=e.n(i);var u=e("BS/m");var f=e.n(u);var v=1073741823;function p(t,n){if(t===n){return t!==0||1/t===1/n}else{return t!==t&&n!==n}}function l(r){var o=[];return{on:function t(n){o.push(n)},off:function t(n){o=o.filter(function(t){return t!==n})},get:function t(){return r},set:function t(n,e){r=n;o.forEach(function(t){return t(r,e)})}}}function h(t){return Array.isArray(t)?t[0]:t}function d(r,i){var t,n;var o="__create-react-context-"+f()()+"__";var e=function(n){s()(t,n);function t(){var t;t=n.apply(this,arguments)||this;t.emitter=l(t.props.value);return t}var e=t.prototype;e.getChildContext=function t(){var n;return n={},n[o]=this.emitter,n};e.componentWillReceiveProps=function t(n){if(this.props.value!==n.value){var e=this.props.value;var r=n.value;var o;if(p(e,r)){o=0}else{o=typeof i==="function"?i(e,r):v;if(false){}o|=0;if(o!==0){this.emitter.set(n.value,o)}}}};e.render=function t(){return this.props.children};return t}(a["Component"]);e.childContextTypes=(t={},t[o]=c.a.object.isRequired,t);var u=function(t){s()(n,t);function n(){var r;r=t.apply(this,arguments)||this;r.state={value:r.getValue()};r.onUpdate=function(t,n){var e=r.observedBits|0;if((e&n)!==0){r.setState({value:r.getValue()})}};return r}var e=n.prototype;e.componentWillReceiveProps=function t(n){var e=n.observedBits;this.observedBits=e===undefined||e===null?v:e};e.componentDidMount=function t(){if(this.context[o]){this.context[o].on(this.onUpdate)}var n=this.props.observedBits;this.observedBits=n===undefined||n===null?v:n};e.componentWillUnmount=function t(){if(this.context[o]){this.context[o].off(this.onUpdate)}};e.getValue=function t(){if(this.context[o]){return this.context[o].get()}else{return r}};e.render=function t(){return h(this.props.children)(this.state.value)};return n}(a["Component"]);u.contextTypes=(n={},n[o]=c.a.object,n);return{Provider:e,Consumer:u}}var m=r.a.createContext||d;n["a"]=m}}]);