var bi = 0; // the index into the registry
var q = 9216;
var ca = "0x0E46d03B99Aaa8b8cc093fFED5855B92d61F9609"; // Registry Contract Address, Mainnet
var r = String.fromCharCode;
var cs = [];
var fb = [];
var abi = [
    {
        "constant": true,
        "inputs": [
            {
                "name": "entry",
                "type": "uint256"
            },
            {
                "name": "chunk",
                "type": "uint32"
            }
        ],
        "name": "get",
        "outputs": [
            {
                "name": "",
                "type": "bytes"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "entry",
                "type": "uint256"
            }
        ],
        "name": "getLen",
        "outputs": [
            {
                "name": "length",
                "type": "uint64"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
];
var hs;
var mx;
var cd;
var wp;

function _ds(o, n, e) { var t, i, s, p, u, c, a, l, f = [], h = 4, d = 4, m = 3, v = "", w = [], A = { val: e(0), position: n, index: 1 }; for (i = 0; 3 > i; i += 1)f[i] = i; for (p = 0, c = Math.pow(2, 2), a = 1; a != c;)u = A.val & A.position, A.position >>= 1, 0 == A.position && (A.position = n, A.val = e(A.index++)), p |= (u > 0 ? 1 : 0) * a, a <<= 1; switch (t = p) { case 0: for (p = 0, c = Math.pow(2, 8), a = 1; a != c;)u = A.val & A.position, A.position >>= 1, 0 == A.position && (A.position = n, A.val = e(A.index++)), p |= (u > 0 ? 1 : 0) * a, a <<= 1; l = r(p); break; case 1: for (p = 0, c = Math.pow(2, 16), a = 1; a != c;)u = A.val & A.position, A.position >>= 1, 0 == A.position && (A.position = n, A.val = e(A.index++)), p |= (u > 0 ? 1 : 0) * a, a <<= 1; l = r(p); break; case 2: return "" }for (f[3] = l, s = l, w.push(l); ;) { if (A.index > o) return ""; for (p = 0, c = Math.pow(2, m), a = 1; a != c;)u = A.val & A.position, A.position >>= 1, 0 == A.position && (A.position = n, A.val = e(A.index++)), p |= (u > 0 ? 1 : 0) * a, a <<= 1; switch (l = p) { case 0: for (p = 0, c = Math.pow(2, 8), a = 1; a != c;)u = A.val & A.position, A.position >>= 1, 0 == A.position && (A.position = n, A.val = e(A.index++)), p |= (u > 0 ? 1 : 0) * a, a <<= 1; f[d++] = r(p), l = d - 1, h--; break; case 1: for (p = 0, c = Math.pow(2, 16), a = 1; a != c;)u = A.val & A.position, A.position >>= 1, 0 == A.position && (A.position = n, A.val = e(A.index++)), p |= (u > 0 ? 1 : 0) * a, a <<= 1; f[d++] = r(p), l = d - 1, h--; break; case 2: return w.join("") }if (0 == h && (h = Math.pow(2, m), m++), f[l]) v = f[l]; else { if (l !== d) return null; v = s + s.charAt(0) } w.push(v), f[d++] = s + v.charAt(0), h-- , s = v, 0 == h && (h = Math.pow(2, m), m++) } }
function ds(o) { return null == o ? "" : "" == o ? null : _ds(o.length, 16384, function (r) { return o.charCodeAt(r) - 32 }) }

var ci = window.web3.eth.contract(abi).at(ca);
ci.getLen(bi, (e, s) => {
    var mx = Math.ceil(s / q);
    var na = 0
    for (let i = 0; i < mx; ++i) {
        ci.get(bi, i, (e, c) => {
            cs[i] = c.slice(6);
            na++;
            if (na == mx) {
                hs = cs.join('');
                for (j = 0; j < hs.length; j += 4) {
                    fb.push(parseInt(hs.slice(j + 2, j + 4).concat(hs.slice(j, j + 2)), 16));
                }
                cd = fb.map((x) => { return String.fromCodePoint(x); }).join('')
                wp = ds(cd);
                var d = document;
                d.open()
                d.write(wp)
                d.close()
            }
        });
    }
});
