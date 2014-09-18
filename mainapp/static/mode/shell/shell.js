(function(e){if(typeof exports=="object"&&typeof module=="object")e(require("../../lib/codemirror"));else if(typeof define=="function"&&define.amd)define(["../../lib/codemirror"],e);else e(CodeMirror)})(function(e){"use strict";e.defineMode("shell",function(){var e={};function t(t,n){var r=n.split(" ");for(var i=0;i<r.length;i++){e[r[i]]=t}}t("atom","true false");t("keyword","if then do else elif while until for in esac fi fin "+"fil done exit set unset export function");t("builtin","ab awk bash beep cat cc cd chown chmod chroot clear cp "+"curl cut diff echo find gawk gcc get git grep kill killall ln ls make "+"mkdir openssl mv nc node npm ping ps restart rm rmdir sed service sh "+"shopt shred source sort sleep ssh start stop su sudo tee telnet top "+"touch vi vim wall wc wget who write yes zsh");function n(t,n){if(t.eatSpace())return null;var s=t.sol();var f=t.next();if(f==="\\"){t.next();return null}if(f==="'"||f==='"'||f==="`"){n.tokens.unshift(r(f));return o(t,n)}if(f==="#"){if(s&&t.eat("!")){t.skipToEnd();return"meta"}t.skipToEnd();return"comment"}if(f==="$"){n.tokens.unshift(i);return o(t,n)}if(f==="+"||f==="="){return"operator"}if(f==="-"){t.eat("-");t.eatWhile(/\w/);return"attribute"}if(/\d/.test(f)){t.eatWhile(/\d/);if(t.eol()||!/\w/.test(t.peek())){return"number"}}t.eatWhile(/[\w-]/);var u=t.current();if(t.peek()==="="&&/\w+/.test(u))return"def";return e.hasOwnProperty(u)?e[u]:null}function r(e){return function(t,n){var r,o=false,s=false;while((r=t.next())!=null){if(r===e&&!s){o=true;break}if(r==="$"&&!s&&e!=="'"){s=true;t.backUp(1);n.tokens.unshift(i);break}s=!s&&r==="\\"}if(o||!s){n.tokens.shift()}return e==="`"||e===")"?"quote":"string"}}var i=function(e,t){if(t.tokens.length>1)e.eat("$");var n=e.next(),i=/\w/;if(n==="{")i=/[^}]/;if(n==="("){t.tokens[0]=r(")");return o(e,t)}if(!/\d/.test(n)){e.eatWhile(i);e.eat("}")}t.tokens.shift();return"def"};function o(e,t){return(t.tokens[0]||n)(e,t)}return{startState:function(){return{tokens:[]}},token:function(e,t){return o(e,t)}}});e.defineMIME("text/x-sh","shell")});