window.print = null
print = console.log

class _ {

    static id(id) {
        return document.getElementById(id)
    }

    static cname(class_name, n) {
        // if (!n) {
        //
        // }
        return document.getElementsByClassName(class_name, n)
    }
}

for (let i = 0, Fele = _.cname('caret'), Cele = _.cname('dropdown-menu'); i < Fele.length; i++) {
    let ele_status = 'none'
    if (ele_status === 'none') {
        Fele[i].onclick = function () {
            Cele[i].style.display = 'block'
        }
    }
}
