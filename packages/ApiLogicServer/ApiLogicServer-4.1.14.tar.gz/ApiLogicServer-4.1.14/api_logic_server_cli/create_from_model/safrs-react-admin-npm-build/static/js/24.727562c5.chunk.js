(this["webpackJsonpreact-apilogicserver"]=this["webpackJsonpreact-apilogicserver"]||[]).push([[24],{1221:function(e,s,n){"use strict";n.r(s),n.d(s,"conf",(function(){return o})),n.d(s,"language",(function(){return t}));var o={brackets:[["{","}"],["[","]"],["(",")"]],autoClosingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:'"',close:'"'},{open:"'",close:"'"}],surroundingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:'"',close:'"'},{open:"'",close:"'"}]},t={defaultToken:"",tokenPostfix:".dockerfile",variable:/\${?[\w]+}?/,tokenizer:{root:[{include:"@whitespace"},{include:"@comment"},[/(ONBUILD)(\s+)/,["keyword",""]],[/(ENV)(\s+)([\w]+)/,["keyword","",{token:"variable",next:"@arguments"}]],[/(FROM|MAINTAINER|RUN|EXPOSE|ENV|ADD|ARG|VOLUME|LABEL|USER|WORKDIR|COPY|CMD|STOPSIGNAL|SHELL|HEALTHCHECK|ENTRYPOINT)/,{token:"keyword",next:"@arguments"}]],arguments:[{include:"@whitespace"},{include:"@strings"},[/(@variable)/,{cases:{"@eos":{token:"variable",next:"@popall"},"@default":"variable"}}],[/\\/,{cases:{"@eos":"","@default":""}}],[/./,{cases:{"@eos":{token:"",next:"@popall"},"@default":""}}]],whitespace:[[/\s+/,{cases:{"@eos":{token:"",next:"@popall"},"@default":""}}]],comment:[[/(^#.*$)/,"comment","@popall"]],strings:[[/\\'$/,"","@popall"],[/\\'/,""],[/'$/,"string","@popall"],[/'/,"string","@stringBody"],[/"$/,"string","@popall"],[/"/,"string","@dblStringBody"]],stringBody:[[/[^\\\$']/,{cases:{"@eos":{token:"string",next:"@popall"},"@default":"string"}}],[/\\./,"string.escape"],[/'$/,"string","@popall"],[/'/,"string","@pop"],[/(@variable)/,"variable"],[/\\$/,"string"],[/$/,"string","@popall"]],dblStringBody:[[/[^\\\$"]/,{cases:{"@eos":{token:"string",next:"@popall"},"@default":"string"}}],[/\\./,"string.escape"],[/"$/,"string","@popall"],[/"/,"string","@pop"],[/(@variable)/,"variable"],[/\\$/,"string"],[/$/,"string","@popall"]]}}}}]);
//# sourceMappingURL=24.727562c5.chunk.js.map