(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{318:function(e,t,n){var r=n(319),i=n(152)((function(e,t){return null==e?{}:r(e,t)}));e.exports=i},319:function(e,t,n){var r=n(320),i=n(149);e.exports=function(e,t){return r(e,t,(function(t,n){return i(e,n)}))}},320:function(e,t,n){var r=n(54),i=n(151),a=n(35);e.exports=function(e,t,n){for(var o=-1,s=t.length,c={};++o<s;){var f=t[o],u=r(e,f);n(u,f)&&i(c,a(f,e),u)}return c}},321:function(e,t,n){var r=n(28),i=n(322),a=n(150),o=Math.max,s=Math.min;e.exports=function(e,t,n){var c,f,u,l,d,p,v=0,h=!1,m=!1,y=!0;if("function"!=typeof e)throw new TypeError("Expected a function");function g(t){var n=c,r=f;return c=f=void 0,v=t,l=e.apply(r,n)}function b(e){return v=e,d=setTimeout(x,t),h?g(e):l}function w(e){var n=e-p;return void 0===p||n>=t||n<0||m&&e-v>=u}function x(){var e=i();if(w(e))return k(e);d=setTimeout(x,function(e){var n=t-(e-p);return m?s(n,u-(e-v)):n}(e))}function k(e){return d=void 0,y&&c?g(e):(c=f=void 0,l)}function j(){var e=i(),n=w(e);if(c=arguments,f=this,p=e,n){if(void 0===d)return b(p);if(m)return clearTimeout(d),d=setTimeout(x,t),g(p)}return void 0===d&&(d=setTimeout(x,t)),l}return t=a(t)||0,r(n)&&(h=!!n.leading,u=(m="maxWait"in n)?o(a(n.maxWait)||0,t):u,y="trailing"in n?!!n.trailing:y),j.cancel=function(){void 0!==d&&clearTimeout(d),v=0,c=p=f=d=void 0},j.flush=function(){return void 0===d?l:k(i())},j}},322:function(e,t,n){var r=n(14);e.exports=function(){return r.Date.now()}},323:function(e,t,n){e.exports=n(324)},324:function(e,t,n){var r,i,a;i=[t,e],void 0===(a="function"==typeof(r=function(e,t){"use strict";var n=function(){function e(){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.edges=[],this.Toposort=e}return e.prototype.add=function(e,t){if("string"!=typeof e||!e)throw new TypeError("Dependent name must be given as a not empty string");if((t=Array.isArray(t)?t:[t]).length>0){var n=t,r=Array.isArray(n),i=0;for(n=r?n:n[Symbol.iterator]();;){var a;if(r){if(i>=n.length)break;a=n[i++]}else{if((i=n.next()).done)break;a=i.value}var o=a;if("string"!=typeof o||!o)throw new TypeError("Dependency name must be given as a not empty string");this.edges.push([e,o])}}else this.edges.push([e]);return this},e.prototype.sort=function(){var e=this,t=[],n=this.edges,r=Array.isArray(n),i=0;for(n=r?n:n[Symbol.iterator]();;){var a;if(r){if(i>=n.length)break;a=n[i++]}else{if((i=n.next()).done)break;a=i.value}var o=b=a,s=Array.isArray(o),c=0;for(o=s?o:o[Symbol.iterator]();;){var f;if(s){if(c>=o.length)break;f=o[c++]}else{if((c=o.next()).done)break;f=c.value}var u=f;-1===t.indexOf(u)&&t.push(u)}}for(var l=t.length,d=new Array(t.length),p=function n(r,i){if(0!==i.length&&-1!==i.indexOf(r))throw new Error("Cyclic dependency found. "+r+" is dependent of itself.\nDependency chain: "+i.join(" -> ")+" => "+r);var a=t.indexOf(r);if(-1!==a){var o=!1;t[a]=!1;var s=e.edges,c=Array.isArray(s),f=0;for(s=c?s:s[Symbol.iterator]();;){var u;if(c){if(f>=s.length)break;u=s[f++]}else{if((f=s.next()).done)break;u=f.value}var p=u;p[0]===r&&(o=o||i.concat([r]),n(p[1],o))}d[--l]=r}},v=0;v<t.length;v++)if(!1!==(u=t[v])){t[v]=!1;var h=this.edges,m=Array.isArray(h),y=0;for(h=m?h:h[Symbol.iterator]();;){var g,b;if(m){if(y>=h.length)break;g=h[y++]}else{if((y=h.next()).done)break;g=y.value}(b=g)[0]===u&&p(b[1],[u])}d[--l]=u}return d},e.prototype.clear=function(){return this.edges=[],this},e}();t.exports=n})?r.apply(t,i):r)||(e.exports=a)},325:function(e){e.exports=JSON.parse('{"a":"h5p-741035c0caad0682ab29b77f4c592a20.html"}')},326:function(e){e.exports=JSON.parse('{"js":"application/javascript","json":"application/json","doc":"application/msword","pdf":"application/pdf","rtf":"text/rtf","xls":"application/vnd.ms-excel","ppt":"application/vnd.ms-powerpoint","odp":"application/vnd.oasis.opendocument.presentation","ods":"application/vnd.oasis.opendocument.spreadsheet","odt":"application/vnd.oasis.opendocument.text","pptx":"application/vnd.openxmlformats-officedocument.presentationml.presentation","xlsx":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document","swf":"application/x-shockwave-flash","xml":"text/xml","mp3":"audio/mpeg","m4a":"audio/x-m4a","ogg":"audio/ogg","wav":"audio/x-wav","otf":"font/otf","ttf":"font/ttf","woff":"font/woff","bmp":"image/x-ms-bmp","gif":"image/gif","jpeg":"image/jpeg","jpg":"image/jpeg","png":"image/png","svg":"image/svg+xml","tif":"image/tiff","tiff":"image/tiff","css":"text/css","csv":"text/csv","md":"text/markdown","txt":"text/plain","vtt":"text/vtt","mp4":"video/mp4","webm":"video/webm"}')},338:function(e,t,n){"use strict";n.r(t),n.d(t,"replacePaths",(function(){return Re})),n.d(t,"default",(function(){return We}));var r=n(52),i=n.n(r),a=n(88),o=n.n(a),s=n(318),c=n.n(s),f=n(137),u=n.n(f),l=n(321),d=n.n(l),p=n(86),v=n.n(p),h=n(323),m=n.n(h),y={},g=Uint8Array,b=Uint16Array,w=Uint32Array,x=new g([0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,0,0,0]),k=new g([0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,0,0]),j=new g([16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15]),P=function(e,t){for(var n=new b(31),r=0;r<31;++r)n[r]=t+=1<<e[r-1];var i=new w(n[30]);for(r=1;r<30;++r)for(var a=n[r];a<n[r+1];++a)i[a]=a-n[r]<<5|r;return[n,i]},O=P(x,2),S=O[0],C=O[1];S[28]=258,C[258]=28;for(var D=P(k,0),A=D[0],U=(D[1],new b(32768)),E=0;E<32768;++E){var L=(43690&E)>>>1|(21845&E)<<1;L=(61680&(L=(52428&L)>>>2|(13107&L)<<2))>>>4|(3855&L)<<4,U[E]=((65280&L)>>>8|(255&L)<<8)>>>1}var T=function(e,t,n){for(var r=e.length,i=0,a=new b(t);i<r;++i)++a[e[i]-1];var o,s=new b(t);for(i=0;i<t;++i)s[i]=s[i-1]+a[i-1]<<1;if(n){o=new b(1<<t);var c=15-t;for(i=0;i<r;++i)if(e[i])for(var f=i<<4|e[i],u=t-e[i],l=s[e[i]-1]++<<u,d=l|(1<<u)-1;l<=d;++l)o[U[l]>>>c]=f}else for(o=new b(r),i=0;i<r;++i)e[i]&&(o[i]=U[s[e[i]-1]++]>>>15-e[i]);return o},I=new g(288);for(E=0;E<144;++E)I[E]=8;for(E=144;E<256;++E)I[E]=9;for(E=256;E<280;++E)I[E]=7;for(E=280;E<288;++E)I[E]=8;var F=new g(32);for(E=0;E<32;++E)F[E]=5;var z=T(I,9,1),H=T(F,5,1),J=function(e){for(var t=e[0],n=1;n<e.length;++n)e[n]>t&&(t=e[n]);return t},R=function(e,t,n){var r=t/8|0;return(e[r]|e[r+1]<<8)>>(7&t)&n},N=function(e,t){var n=t/8|0;return(e[n]|e[n+1]<<8|e[n+2]<<16)>>(7&t)},W=function(e){return(e+7)/8|0},M=function(e,t,n){(null==t||t<0)&&(t=0),(null==n||n>e.length)&&(n=e.length);var r=new(e instanceof b?b:e instanceof w?w:g)(n-t);return r.set(e.subarray(t,n)),r},V=["unexpected EOF","invalid block type","invalid length/literal","invalid distance","stream finished","no stream handler",,"no callback","invalid UTF-8 data","extra field too long","date not in range 1980-2099","filename too long","stream finishing","invalid zip data"],$=function e(t,n,r){var i=new Error(n||V[t]);if(i.code=t,Error.captureStackTrace&&Error.captureStackTrace(i,e),!r)throw i;return i},B=function(e,t,n){var r=e.length;if(!r||n&&n.f&&!n.l)return t||new g(0);var i=!t||n,a=!n||n.i;n||(n={}),t||(t=new g(3*r));var o=function(e){var n=t.length;if(e>n){var r=new g(Math.max(2*n,e));r.set(t),t=r}},s=n.f||0,c=n.p||0,f=n.b||0,u=n.l,l=n.d,d=n.m,p=n.n,v=8*r;do{if(!u){s=R(e,c,1);var h=R(e,c+1,3);if(c+=3,!h){var m=e[(I=W(c)+4)-4]|e[I-3]<<8,y=I+m;if(y>r){a&&$(0);break}i&&o(f+m),t.set(e.subarray(I,y),f),n.b=f+=m,n.p=c=8*y,n.f=s;continue}if(1==h)u=z,l=H,d=9,p=5;else if(2==h){var b=R(e,c,31)+257,w=R(e,c+10,15)+4,P=b+R(e,c+5,31)+1;c+=14;for(var O=new g(P),C=new g(19),D=0;D<w;++D)C[j[D]]=R(e,c+3*D,7);c+=3*w;var U=J(C),E=(1<<U)-1,L=T(C,U,1);for(D=0;D<P;){var I,F=L[R(e,c,E)];if(c+=15&F,(I=F>>>4)<16)O[D++]=I;else{var V=0,B=0;for(16==I?(B=3+R(e,c,3),c+=2,V=O[D-1]):17==I?(B=3+R(e,c,7),c+=3):18==I&&(B=11+R(e,c,127),c+=7);B--;)O[D++]=V}}var q=O.subarray(0,b),_=O.subarray(b);d=J(q),p=J(_),u=T(q,d,1),l=T(_,p,1)}else $(1);if(c>v){a&&$(0);break}}i&&o(f+131072);for(var X=(1<<d)-1,G=(1<<p)-1,K=c;;K=c){var Q=(V=u[N(e,c)&X])>>>4;if((c+=15&V)>v){a&&$(0);break}if(V||$(2),Q<256)t[f++]=Q;else{if(256==Q){K=c,u=null;break}var Y=Q-254;if(Q>264){var Z=x[D=Q-257];Y=R(e,c,(1<<Z)-1)+S[D],c+=Z}var ee=l[N(e,c)&G],te=ee>>>4;ee||$(3),c+=15&ee;_=A[te];if(te>3){Z=k[te];_+=N(e,c)&(1<<Z)-1,c+=Z}if(c>v){a&&$(0);break}i&&o(f+131072);for(var ne=f+Y;f<ne;f+=4)t[f]=t[f-_],t[f+1]=t[f+1-_],t[f+2]=t[f+2-_],t[f+3]=t[f+3-_];f=ne}}n.l=u,n.p=K,n.b=f,n.f=s,u&&(s=1,n.m=d,n.d=l,n.n=p)}while(!s);return f==t.length?t:M(t,0,f)},q=new g(0),_=function(e,t){var n={};for(var r in e)n[r]=e[r];for(var r in t)n[r]=t[r];return n},X=function(e,t,n){for(var r=e(),i=e.toString(),a=i.slice(i.indexOf("[")+1,i.lastIndexOf("]")).replace(/ /g,"").split(","),o=0;o<r.length;++o){var s=r[o],c=a[o];if("function"==typeof s){t+=";"+c+"=";var f=s.toString();if(s.prototype)if(-1!=f.indexOf("[native code]")){var u=f.indexOf(" ",8)+1;t+=f.slice(u,f.indexOf("(",u))}else for(var l in t+=f,s.prototype)t+=";"+c+".prototype."+l+"="+s.prototype[l].toString();else t+=f}else n[c]=s}return[t,n]},G=[],K=function(e,t,n,r){var i;if(!G[n]){for(var a="",o={},s=e.length-1,c=0;c<s;++c)a=(i=X(e[c],a,o))[0],o=i[1];G[n]=X(e[s],a,o)}var f=_({},G[n][1]);return function(e,t,n,r,i){var a=new Worker(y[t]||(y[t]=URL.createObjectURL(new Blob([e+';addEventListener("error",function(e){e=e.error;postMessage({$e$:[e.message,e.code,e.stack]})})'],{type:"text/javascript"}))));return a.onmessage=function(e){var t=e.data,n=t.$e$;if(n){var r=new Error(n[0]);r.code=n[1],r.stack=n[2],i(r,null)}else i(null,t)},a.postMessage(n,r),a}(G[n][0]+";onmessage=function(e){for(var k in e.data)self[k]=e.data[k];onmessage="+t.toString()+"}",n,f,function(e){var t=[];for(var n in e)(e[n]instanceof g||e[n]instanceof b||e[n]instanceof w)&&t.push((e[n]=new e[n].constructor(e[n])).buffer);return t}(f),r)},Q=function(){return[g,b,w,x,k,j,S,A,z,H,U,V,T,J,R,N,W,M,$,B,ae,Y,Z]},Y=function(e){return postMessage(e,[e.buffer])},Z=function(e){return e&&e.size&&new g(e.size)},ee=function(e,t,n,r,i,a){var o=K(n,r,i,(function(e,t){o.terminate(),a(e,t)}));return o.postMessage([e,t],t.consume?[e.buffer]:[]),function(){o.terminate()}},te=function(e,t){return e[t]|e[t+1]<<8},ne=function(e,t){return(e[t]|e[t+1]<<8|e[t+2]<<16|e[t+3]<<24)>>>0},re=function(e,t){return ne(e,t)+4294967296*ne(e,t+4)};function ie(e,t,n){return n||(n=t,t={}),"function"!=typeof n&&$(7),ee(e,t,[Q],(function(e){return Y(ae(e.data[0],Z(e.data[1])))}),1,n)}function ae(e,t){return B(e,t)}var oe="undefined"!=typeof TextDecoder&&new TextDecoder;try{oe.decode(q,{stream:!0}),1}catch(e){}var se=function(e){for(var t="",n=0;;){var r=e[n++],i=(r>127)+(r>223)+(r>239);if(n+i>e.length)return[t,M(e,n-1)];i?3==i?(r=((15&r)<<18|(63&e[n++])<<12|(63&e[n++])<<6|63&e[n++])-65536,t+=String.fromCharCode(55296|r>>10,56320|1023&r)):t+=1&i?String.fromCharCode((31&r)<<6|63&e[n++]):String.fromCharCode((15&r)<<12|(63&e[n++])<<6|63&e[n++]):t+=String.fromCharCode(r)}};function ce(e,t){if(t){for(var n="",r=0;r<e.length;r+=16384)n+=String.fromCharCode.apply(null,e.subarray(r,r+16384));return n}if(oe)return oe.decode(e);var i=se(e),a=i[0];return i[1].length&&$(8),a}var fe=function(e,t){return t+30+te(e,t+26)+te(e,t+28)},ue=function(e,t,n){var r=te(e,t+28),i=ce(e.subarray(t+46,t+46+r),!(2048&te(e,t+8))),a=t+46+r,o=ne(e,t+20),s=n&&4294967295==o?le(e,a):[o,ne(e,t+24),ne(e,t+42)],c=s[0],f=s[1],u=s[2];return[te(e,t+10),c,f,i,a+te(e,t+30)+te(e,t+32),u]},le=function(e,t){for(;1!=te(e,t);t+=4+te(e,t+2));return[re(e,t+12),re(e,t+4),re(e,t+20)]};var de="function"==typeof queueMicrotask?queueMicrotask:"function"==typeof setTimeout?setTimeout:function(e){e()};var pe=n(325),ve=n(326),he=n(53);function me(e){return function(e){if(Array.isArray(e))return je(e)}(e)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(e)||ke(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function ye(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function ge(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?ye(Object(n),!0).forEach((function(t){be(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):ye(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function be(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function we(e,t){var n;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(n=ke(e))||t&&e&&"number"==typeof e.length){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var a,o=!0,s=!1;return{s:function(){n=e[Symbol.iterator]()},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||null==n.return||n.return()}finally{if(s)throw a}}}}function xe(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if("undefined"==typeof Symbol||!(Symbol.iterator in Object(e)))return;var n=[],r=!0,i=!1,a=void 0;try{for(var o,s=e[Symbol.iterator]();!(r=(o=s.next()).done)&&(n.push(o.value),!t||n.length!==t);r=!0);}catch(e){i=!0,a=e}finally{try{r||null==s.return||s.return()}finally{if(i)throw a}}return n}(e,t)||ke(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function ke(e,t){if(e){if("string"==typeof e)return je(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?je(e,t):void 0}}function je(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function Pe(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function Oe(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function Se(e,t,n){return t&&Oe(e.prototype,t),n&&Oe(e,n),e}for(var Ce=function(){function e(t){Pe(this,e),this.zipfile=t}return Se(e,[{key:"_getFiles",value:function(e){var t=this;return new Promise((function(n,r){!function(e,t,n){n||(n=t,t={}),"function"!=typeof n&&$(7);var r=[],i=function(){for(var e=0;e<r.length;++e)r[e]()},a={},o=function(e,t){de((function(){n(e,t)}))};de((function(){o=n}));for(var s=e.length-22;101010256!=ne(e,s);--s)if(!s||e.length-s>65558)return o($(13,0,1),null),i;var c=te(e,s+8);if(c){var f=c,u=ne(e,s+16),l=4294967295==u;if(l){if(s=ne(e,s-12),101075792!=ne(e,s))return o($(13,0,1),null),i;f=c=ne(e,s+32),u=ne(e,s+48)}for(var d=t&&t.filter,p=function(t){var n=ue(e,u,l),s=n[0],f=n[1],p=n[2],v=n[3],h=n[4],m=n[5],y=fe(e,m);u=h;var b=function(e,t){e?(i(),o(e,null)):(t&&(a[v]=t),--c||o(null,a))};if(!d||d({name:v,size:f,originalSize:p,compression:s}))if(s)if(8==s){var w=e.subarray(y,y+f);if(f<32e4)try{b(null,ae(w,new g(p)))}catch(e){b(e,null)}else r.push(ie(w,{size:p},b))}else b($(14,"unknown compression type "+s,1),null);else b(null,M(e,y,y+f));else b(null,null)},v=0;v<f;++v)p()}else o(null,{})}(t.zipfile,{filter:e},(function(e,t){e&&r(e),n(Object.entries(t).map((function(e){var t=xe(e,2);return{name:t[0],obj:t[1]}})))}))}))}},{key:"file",value:function(e){return this._getFiles((function(t){return t.name===e})).then((function(e){return e[0]}))}},{key:"files",value:function(e){return this._getFiles((function(t){return t.name.startsWith(e)}))}}]),e}(),De={},Ae=0,Ue=["downloaded","copied","accessed-reuse","accessed-embed","accessed-copyright"];Ae<Ue.length;Ae++){var Ee=Ue[Ae];De[he.a[Ee]]=!0}for(var Le=["answered","interacted"],Te={},Ie=0,Fe=["completed","mastered","passed"];Ie<Fe.length;Ie++){var ze=Fe[Ie];Te[he.a[ze]]=!0}function He(e,t){var n="",r=t.split(".").slice(-1)[0];if(r){var i=r.toLowerCase();n=ve[i]}var a=new Blob([e.buffer],{type:n});return URL.createObjectURL(a)}var Je=/(url\(['"]?)([^"')]+)?(['"]?\))/g;function Re(e,t){return t[e].replace(Je,(function(n,r,i,a){try{var o=new URL(i,new URL(e,"http://b.b/")).pathname.substring(1),s=t[o];if(s)return"".concat(r).concat(s).concat(a)}catch(e){console.debug("Error during URL handling",e)}return n}))}var Ne=["title","a11yTitle","authors","changes","source","license","licenseVersion","licenseExtras","authorComments","yearFrom","yearTo","defaultLanguage"],We=function(){function e(t){Pe(this,e),this.shim=t,this.data=t.data,this.scriptLoader=this.scriptLoader.bind(this)}return Se(e,[{key:"init",value:function(e,t,n,r){var i=this;this.dependencies=[],this.jsDependencies={},this.cssDependencies={},this.packageFiles={},this.contentPaths={},this.contentJson="",this.library=null,this.loadedJs={},this.loadedCss={},this.iframe=e,this.iframe.src="../h5p/".concat(pe.a),this.filepath=t,this.zipcontentUrl=new URL("../../zipcontent/".concat(this.filepath.substring(this.filepath.lastIndexOf("/")+1)),window.location).href,this.loaded=n,this.errored=r,this.contentNamespace="1234567890";var a,o=performance.now();(a=this.filepath,new Promise((function(e,t){try{var n=new window.XMLHttpRequest;n.open("GET",a,!0),n.responseType="arraybuffer",n.onreadystatechange=function(){if(4===n.readyState)if(200===n.status||0===n.status)try{e(new Uint8Array(n.response))}catch(e){t(new Error(e))}else t(new Error("Ajax error for "+a+" : "+n.status+" "+n.statusText))},n.send()}catch(e){t(new Error(e),null)}}))).then((function(e){return i.zip=new Ce(e),i.recurseDependencies("h5p.json",!0)})).then((function(){return i.setDependencies(),i.processFiles().then((function(){if(console.debug("H5P file processed in ".concat(performance.now()-o," ms")),i.metadata=c()(i.rootConfig,Ne),i.processCssDependencies(),i.processJsDependencies(),i.iframe.contentDocument&&"complete"===i.iframe.contentDocument.readyState&&i.iframe.contentWindow.H5P)return i.initH5P();i.iframe.addEventListener("load",(function(){return i.initH5P()}))}))}))}},{key:"stateUpdated",value:function(){this.shim.stateUpdated()}},{key:"initH5P",value:function(){var e=this;return this.shimH5P(this.iframe.contentWindow),this.scriptLoader(this.cssURL,!0).then((function(){return e.scriptLoader(e.javascriptURL).then((function(){try{e.iframe.contentWindow.H5P.init(),e.loaded(),setTimeout((function(){var t,n=we(e.iframe.contentWindow.H5P.instances);try{for(n.s();!(t=n.n()).done;){var r=t.value;e.iframe.contentWindow.H5P.trigger(r,"resize")}}catch(e){n.e(e)}finally{n.f()}}),0)}catch(t){e.errored(t)}}))}))}},{key:"shimH5P",value:function(e){var t=e.document.createElement("div");t.classList.add("h5p-content"),t.setAttribute("data-content-id",this.contentNamespace),e.document.body.appendChild(t);var n=e.H5P,r=n.getPath,a=this;n.getPath=function(e,t){return"#tmp"===e.substr(-4,4)&&(e=e.substr(0,e.length-4)),a.contentPaths[e]?a.contentPaths[e]:r(e,t)},n.getContentPath=function(){return a.zipcontentUrl+"/content"},n.getUserData=function(e,t,n){var r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:0,o=i()(a.data,[r,t]);return n(void 0,"RESET"===o?null:o)},n.setUserData=function(e,t,n){var r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:{},i=r.subContentId,s=void 0===i?0:i,c=r.errorCallback,f=void 0===c?null:c;try{n=JSON.stringify(n)}catch(e){return void(o()(f)&&f(e))}u()(a.data,[s,t],n),a.stateUpdated()},n.deleteUserData=function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:0;v()(a.data,[n,t]),a.stateUpdated()};var s=n.ContentType;n.ContentType=function(e){var t=s(e);return t.prototype.getLibraryFilePath=function(e){var t=a.packageFiles[this.libraryInfo.versionedNameNoSpaces+"/"][e];return t||a.zipcontentUrl+"/"+this.libraryInfo.versionedNameNoSpaces+"/"},t},n.XAPIEvent.prototype.setActor=function(){e.xAPI&&e.xAPI.prepareStatement(this.data.statement)};var c,f={},l=we(Le);try{for(l.s();!(c=l.n()).done;){var p=c.value,h=he.a[p];f[h]=d()((function(t){e.xAPI.sendStatement(t,!0).catch((function(e){console.error("Statement: ",t,"gave the following error: ",e)}))}),5e3,{leading:!0,maxWait:3e4})}}catch(e){l.e(e)}finally{l.f()}n.externalDispatcher.on("xAPI",(function(t){if(e.xAPI){var n=t.data.statement;if(n.object&&n.object.id.startsWith(a.H5PContentIdentifier)&&n.object.id!==a.H5PContentIdentifier&&n.verb&&Te[n.verb.id]&&(n.verb.id=he.a.progressed),De[n.verb.id])return;f[n.verb.id]?f[n.verb.id](n):e.xAPI.sendStatement(t.data.statement,!0).catch((function(e){console.error("Statement: ",n,"gave the following error: ",e)}))}}))}},{key:"H5PContentIdentifier",get:function(){return this.rootConfig&&this.rootConfig.source||"http://kolibri.to/content/".concat(this.contentNamespace)}},{key:"shimH5PIntegration",value:function(e){var t=this;this.integrationShim={get contents(){return be({},(e=t.contentNamespace,"cid-".concat(e)),{library:t.library,jsonContent:t.contentJson,fullScreen:!1,displayOptions:{copyright:!1,download:!1,embed:!1,export:!1,frame:!1,icon:!1},contentUserData:t.data,exportUrl:"",embedCode:"",resizeCode:"",mainId:t.contentNamespace,url:t.H5PContentIdentifier,title:t.rootConfig.title,styles:Object.keys(t.loadedCss),scripts:Object.keys(t.loadedJs),metadata:t.metadata});var e},l10n:{H5P:{}},get loadedJs(){return Object.keys(t.loadedJs)},get loadedCss(){return Object.keys(t.loadedCss)},get user(){return{name:t.userData.userFullName,mail:""}},get urlLibraries(){return t.zipcontentUrl}},Object.defineProperty(e,"H5PIntegration",{value:this.integrationShim,configurable:!0})}},{key:"scriptLoader",value:function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],n=this.iframe.contentWindow.document;return new Promise((function(r,i){var a;t?((a=n.createElement("link")).rel="stylesheet",a.type="text/css",a.href=e,r(a)):((a=n.createElement("script")).type="text/javascript",a.src=e,a.async=!0,a.addEventListener("load",(function(){return r(a)})),a.addEventListener("error",i)),n.body.appendChild(a)}))}},{key:"setDependencies",value:function(){var e,t=new m.a,n=we(this.dependencies);try{for(n.s();!(e=n.n()).done;){var r=e.value;this.packageFiles[r.packagePath]={},t.add(r.packagePath,r.dependencies),this.cssDependencies[r.packagePath]=r.preloadedCss,this.jsDependencies[r.packagePath]=r.preloadedJs}}catch(e){n.e(e)}finally{n.f()}this.sortedDependencies=t.sort().reverse()}},{key:"recurseDependencies",value:function(e,t){var n=this,r=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},i=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"";return this.zip.file(e).then((function(e){if(e){var a=JSON.parse(ce(e.obj)),o=a.preloadedDependencies||[];return r=ge({},r),t&&(n.rootConfig=a),Promise.all(o.map((function(e){var i="".concat(e.machineName,"-").concat(e.majorVersion,".").concat(e.minorVersion,"/");return t&&!n.library&&e.machineName===a.mainLibrary&&(n.library="".concat(e.machineName," ").concat(e.majorVersion,".").concat(e.minorVersion)),r[i]?Promise.resolve(i):(r[i]=!0,n.recurseDependencies(i+"library.json",!1,r,i).then((function(){return i})))}))).then((function(e){if(i){var t=(a.preloadedJs||[]).map((function(e){return e.path})),r=(a.preloadedCss||[]).map((function(e){return e.path}));n.dependencies.push({packagePath:i,dependencies:e,preloadedCss:r,preloadedJs:t})}}))}}))}},{key:"processJsDependencies",value:function(){var e=this,t=this.sortedDependencies.reduce((function(t,n){return(e.jsDependencies[n]||[]).reduce((function(t,r){return"".concat(t).concat(e.packageFiles[n][r],"\n\n")}),t)}),"");this.javascriptURL=URL.createObjectURL(new Blob([t],{type:"text/javascript"}))}},{key:"processCssDependencies",value:function(){var e=this,t=this.sortedDependencies.reduce((function(t,n){return(e.cssDependencies[n]||[]).reduce((function(t,r){var i=Re(r,e.packageFiles[n]);return"".concat(t).concat(i,"\n\n")}),t)}),"");this.cssURL=URL.createObjectURL(new Blob([t],{type:"text/css"}))}},{key:"processContent",value:function(e){var t=e.name.replace("content/","");"content.json"===t?this.contentJson=ce(e.obj):this.contentPaths[t]=He(e.obj,t)}},{key:"processPackageFile",value:function(e,t){var n=e.name.replace(t,""),r=this.jsDependencies[t].indexOf(n)>-1;this.cssDependencies[t].indexOf(n)>-1||r?(r?this.loadedJs[e.name]=!0:this.loadedCss[e.name]=!0,this.packageFiles[t][n]=ce(e.obj)):this.packageFiles[t][n]=He(e.obj,n)}},{key:"processFiles",value:function(){var e=this;return Promise.all([this.zip.files("content/").then((function(t){t.map((function(t){return e.processContent(t)}))}))].concat(me(Object.keys(this.packageFiles).map((function(t){return e.zip.files(t).then((function(n){n.map((function(n){return e.processPackageFile(n,t)}))}))})))))}}]),e}()}}]);