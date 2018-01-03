(function(module) {/*
 A JavaScript implementation of the SHA family of hashes, as defined in FIPS
 PUB 180-2 as well as the corresponding HMAC implementation as defined in
 FIPS PUB 198a

 Copyright Brian Turek 2008-2013
 Distributed under the BSD License
 See http://caligatio.github.com/jsSHA/ for more information

 Several functions taken from Paul Johnson
*/
function p(a){throw a;}var r=null;function t(a,b){this.a=a;this.b=b}function v(a,b){var d=[],f,e=[],g=0,j;if("UTF8"==b)for(j=0;j<a.length;j+=1){f=a.charCodeAt(j);e=[];2048<f?(e[0]=224|(f&61440)>>>12,e[1]=128|(f&4032)>>>6,e[2]=128|f&63):128<f?(e[0]=192|(f&1984)>>>6,e[1]=128|f&63):e[0]=f;for(f=0;f<e.length;f+=1)d[g>>>2]|=e[f]<<24-8*(g%4),g+=1}else if("UTF16"==b)for(j=0;j<a.length;j+=1)d[g>>>2]|=a.charCodeAt(j)<<16-8*(g%4),g+=2;return{value:d,binLen:8*g}}
function y(a){var b=[],d=a.length,f,e;0!==d%2&&p("String of HEX type must be in byte increments");for(f=0;f<d;f+=2)e=parseInt(a.substr(f,2),16),isNaN(e)&&p("String of HEX type contains invalid characters"),b[f>>>3]|=e<<24-4*(f%8);return{value:b,binLen:4*d}}
function C(a){var b=[],d=0,f,e,g,j,m;-1===a.search(/^[a-zA-Z0-9=+\/]+$/)&&p("Invalid character in base-64 string");f=a.indexOf("=");a=a.replace(/\=/g,"");-1!==f&&f<a.length&&p("Invalid '=' found in base-64 string");for(e=0;e<a.length;e+=4){m=a.substr(e,4);for(g=j=0;g<m.length;g+=1)f="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".indexOf(m[g]),j|=f<<18-6*g;for(g=0;g<m.length-1;g+=1)b[d>>2]|=(j>>>16-8*g&255)<<24-8*(d%4),d+=1}return{value:b,binLen:8*d}}
function F(a,b){var d="",f=4*a.length,e,g;for(e=0;e<f;e+=1)g=a[e>>>2]>>>8*(3-e%4),d+="0123456789abcdef".charAt(g>>>4&15)+"0123456789abcdef".charAt(g&15);return b.outputUpper?d.toUpperCase():d}
function G(a,b){var d="",f=4*a.length,e,g,j;for(e=0;e<f;e+=3){j=(a[e>>>2]>>>8*(3-e%4)&255)<<16|(a[e+1>>>2]>>>8*(3-(e+1)%4)&255)<<8|a[e+2>>>2]>>>8*(3-(e+2)%4)&255;for(g=0;4>g;g+=1)d=8*e+6*g<=32*a.length?d+"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(j>>>6*(3-g)&63):d+b.b64Pad}return d}
function H(a){var b={outputUpper:!1,b64Pad:"="};try{a.hasOwnProperty("outputUpper")&&(b.outputUpper=a.outputUpper),a.hasOwnProperty("b64Pad")&&(b.b64Pad=a.b64Pad)}catch(d){}"boolean"!==typeof b.outputUpper&&p("Invalid outputUpper formatting option");"string"!==typeof b.b64Pad&&p("Invalid b64Pad formatting option");return b}
function I(a,b){var d=r,d=new t(a.a,a.b);return d=32>=b?new t(d.a>>>b|d.b<<32-b&4294967295,d.b>>>b|d.a<<32-b&4294967295):new t(d.b>>>b-32|d.a<<64-b&4294967295,d.a>>>b-32|d.b<<64-b&4294967295)}function J(a,b){var d=r;return d=32>=b?new t(a.a>>>b,a.b>>>b|a.a<<32-b&4294967295):new t(0,a.a>>>b-32)}function K(a,b,d){return new t(a.a&b.a^~a.a&d.a,a.b&b.b^~a.b&d.b)}function U(a,b,d){return new t(a.a&b.a^a.a&d.a^b.a&d.a,a.b&b.b^a.b&d.b^b.b&d.b)}
function V(a){var b=I(a,28),d=I(a,34);a=I(a,39);return new t(b.a^d.a^a.a,b.b^d.b^a.b)}function W(a){var b=I(a,14),d=I(a,18);a=I(a,41);return new t(b.a^d.a^a.a,b.b^d.b^a.b)}function X(a){var b=I(a,1),d=I(a,8);a=J(a,7);return new t(b.a^d.a^a.a,b.b^d.b^a.b)}function Y(a){var b=I(a,19),d=I(a,61);a=J(a,6);return new t(b.a^d.a^a.a,b.b^d.b^a.b)}
function Z(a,b){var d,f,e;d=(a.b&65535)+(b.b&65535);f=(a.b>>>16)+(b.b>>>16)+(d>>>16);e=(f&65535)<<16|d&65535;d=(a.a&65535)+(b.a&65535)+(f>>>16);f=(a.a>>>16)+(b.a>>>16)+(d>>>16);return new t((f&65535)<<16|d&65535,e)}
function aa(a,b,d,f){var e,g,j;e=(a.b&65535)+(b.b&65535)+(d.b&65535)+(f.b&65535);g=(a.b>>>16)+(b.b>>>16)+(d.b>>>16)+(f.b>>>16)+(e>>>16);j=(g&65535)<<16|e&65535;e=(a.a&65535)+(b.a&65535)+(d.a&65535)+(f.a&65535)+(g>>>16);g=(a.a>>>16)+(b.a>>>16)+(d.a>>>16)+(f.a>>>16)+(e>>>16);return new t((g&65535)<<16|e&65535,j)}
function ba(a,b,d,f,e){var g,j,m;g=(a.b&65535)+(b.b&65535)+(d.b&65535)+(f.b&65535)+(e.b&65535);j=(a.b>>>16)+(b.b>>>16)+(d.b>>>16)+(f.b>>>16)+(e.b>>>16)+(g>>>16);m=(j&65535)<<16|g&65535;g=(a.a&65535)+(b.a&65535)+(d.a&65535)+(f.a&65535)+(e.a&65535)+(j>>>16);j=(a.a>>>16)+(b.a>>>16)+(d.a>>>16)+(f.a>>>16)+(e.a>>>16)+(g>>>16);return new t((j&65535)<<16|g&65535,m)}
function $(a,b,d){var f,e,g,j,m,l,B,D,L,h,M,w,k,n,u,q,z,A,s,N,O,P,Q,R,c,S,x=[],T,E;"SHA-384"===d||"SHA-512"===d?(M=80,f=(b+128>>>10<<5)+31,n=32,u=2,c=t,q=Z,z=aa,A=ba,s=X,N=Y,O=V,P=W,R=U,Q=K,S=[new c(1116352408,3609767458),new c(1899447441,602891725),new c(3049323471,3964484399),new c(3921009573,2173295548),new c(961987163,4081628472),new c(1508970993,3053834265),new c(2453635748,2937671579),new c(2870763221,3664609560),new c(3624381080,2734883394),new c(310598401,1164996542),new c(607225278,1323610764),
new c(1426881987,3590304994),new c(1925078388,4068182383),new c(2162078206,991336113),new c(2614888103,633803317),new c(3248222580,3479774868),new c(3835390401,2666613458),new c(4022224774,944711139),new c(264347078,2341262773),new c(604807628,2007800933),new c(770255983,1495990901),new c(1249150122,1856431235),new c(1555081692,3175218132),new c(1996064986,2198950837),new c(2554220882,3999719339),new c(2821834349,766784016),new c(2952996808,2566594879),new c(3210313671,3203337956),new c(3336571891,
1034457026),new c(3584528711,2466948901),new c(113926993,3758326383),new c(338241895,168717936),new c(666307205,1188179964),new c(773529912,1546045734),new c(1294757372,1522805485),new c(1396182291,2643833823),new c(1695183700,2343527390),new c(1986661051,1014477480),new c(2177026350,1206759142),new c(2456956037,344077627),new c(2730485921,1290863460),new c(2820302411,3158454273),new c(3259730800,3505952657),new c(3345764771,106217008),new c(3516065817,3606008344),new c(3600352804,1432725776),new c(4094571909,
1467031594),new c(275423344,851169720),new c(430227734,3100823752),new c(506948616,1363258195),new c(659060556,3750685593),new c(883997877,3785050280),new c(958139571,3318307427),new c(1322822218,3812723403),new c(1537002063,2003034995),new c(1747873779,3602036899),new c(1955562222,1575990012),new c(2024104815,1125592928),new c(2227730452,2716904306),new c(2361852424,442776044),new c(2428436474,593698344),new c(2756734187,3733110249),new c(3204031479,2999351573),new c(3329325298,3815920427),new c(3391569614,
3928383900),new c(3515267271,566280711),new c(3940187606,3454069534),new c(4118630271,4000239992),new c(116418474,1914138554),new c(174292421,2731055270),new c(289380356,3203993006),new c(460393269,320620315),new c(685471733,587496836),new c(852142971,1086792851),new c(1017036298,365543100),new c(1126000580,2618297676),new c(1288033470,3409855158),new c(1501505948,4234509866),new c(1607167915,987167468),new c(1816402316,1246189591)],h="SHA-384"===d?[new c(3418070365,3238371032),new c(1654270250,914150663),
new c(2438529370,812702999),new c(355462360,4144912697),new c(1731405415,4290775857),new c(41048885895,1750603025),new c(3675008525,1694076839),new c(1203062813,3204075428)]:[new c(1779033703,4089235720),new c(3144134277,2227873595),new c(1013904242,4271175723),new c(2773480762,1595750129),new c(1359893119,2917565137),new c(2600822924,725511199),new c(528734635,4215389547),new c(1541459225,327033209)]):p("Unexpected error in SHA-2 implementation");a[b>>>5]|=128<<24-b%32;a[f]=b;T=a.length;for(w=0;w<
T;w+=n){b=h[0];f=h[1];e=h[2];g=h[3];j=h[4];m=h[5];l=h[6];B=h[7];for(k=0;k<M;k+=1)x[k]=16>k?new c(a[k*u+w],a[k*u+w+1]):z(N(x[k-2]),x[k-7],s(x[k-15]),x[k-16]),D=A(B,P(j),Q(j,m,l),S[k],x[k]),L=q(O(b),R(b,f,e)),B=l,l=m,m=j,j=q(g,D),g=e,e=f,f=b,b=q(D,L);h[0]=q(b,h[0]);h[1]=q(f,h[1]);h[2]=q(e,h[2]);h[3]=q(g,h[3]);h[4]=q(j,h[4]);h[5]=q(m,h[5]);h[6]=q(l,h[6]);h[7]=q(B,h[7])}"SHA-384"===d?E=[h[0].a,h[0].b,h[1].a,h[1].b,h[2].a,h[2].b,h[3].a,h[3].b,h[4].a,h[4].b,h[5].a,h[5].b]:"SHA-512"===d?E=[h[0].a,h[0].b,
h[1].a,h[1].b,h[2].a,h[2].b,h[3].a,h[3].b,h[4].a,h[4].b,h[5].a,h[5].b,h[6].a,h[6].b,h[7].a,h[7].b]:p("Unexpected error in SHA-2 implementation");return E}
module.jsSHA=function(a,b,d){var f=r,e=r,g=0,j=[0],m="",l=r,m="undefined"!==typeof d?d:"UTF8";"UTF8"===m||"UTF16"===m||p("encoding must be UTF8 or UTF16");"HEX"===b?(0!==a.length%2&&p("srcString of HEX type must be in byte increments"),l=y(a),g=l.binLen,j=l.value):"ASCII"===b||"TEXT"===b?(l=v(a,m),g=l.binLen,j=l.value):"B64"===b?(l=C(a),g=l.binLen,j=l.value):p("inputFormat must be HEX, TEXT, ASCII, or B64");this.getHash=function(a,b,d){var h=r,m=j.slice(),l="";switch(b){case "HEX":h=F;break;case "B64":h=
G;break;default:p("format must be HEX or B64")}"SHA-384"===a?(r===f&&(f=$(m,g,a)),l=h(f,H(d))):"SHA-512"===a?(r===e&&(e=$(m,g,a)),l=h(e,H(d))):p("Chosen SHA variant is not supported");return l};this.getHMAC=function(a,b,d,e,f){var l,k,n,u,q,z=[],A=[],s=r;switch(e){case "HEX":l=F;break;case "B64":l=G;break;default:p("outputFormat must be HEX or B64")}"SHA-384"===d?(n=128,q=384):"SHA-512"===d?(n=128,q=512):p("Chosen SHA variant is not supported");"HEX"===b?(s=y(a),u=s.binLen,k=s.value):"ASCII"===b||
"TEXT"===b?(s=v(a,m),u=s.binLen,k=s.value):"B64"===b?(s=C(a),u=s.binLen,k=s.value):p("inputFormat must be HEX, TEXT, ASCII, or B64");a=8*n;b=n/4-1;n<u/8?(k=$(k,u,d),k[b]&=4294967040):n>u/8&&(k[b]&=4294967040);for(n=0;n<=b;n+=1)z[n]=k[n]^909522486,A[n]=k[n]^1549556828;d=$(A.concat($(z.concat(j),a+g,d)),a+q,d);return l(d,H(f))}};})(this);
