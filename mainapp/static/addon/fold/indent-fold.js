(function(e){if(typeof exports=="object"&&typeof module=="object")e(require("../../lib/codemirror"));else if(typeof define=="function"&&define.amd)define(["../../lib/codemirror"],e);else e(CodeMirror)})(function(e){"use strict";e.registerHelper("fold","indent",function(t,i){var n=t.getOption("tabSize"),r=t.getLine(i.line);if(!/\S/.test(r))return;var o=function(t){return e.countColumn(t,null,n)};var f=o(r);var l=null;for(var u=i.line+1,s=t.lastLine();u<=s;++u){var a=t.getLine(u);var c=o(a);if(c>f){l=u}else if(!/\S/.test(a)){}else{break}}if(l)return{from:e.Pos(i.line,r.length),to:e.Pos(l,t.getLine(l).length)}})});