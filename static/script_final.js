window.onload=function(){
    document.getElementById("search-box").click();
  };

function removePage(current_path) {
    start = current_path.indexOf("page=");
    temp_end = current_path.slice(start).indexOf("&");
    end = current_path.length - current_path.slice(start).length + temp_end;
    remove = current_path.slice(start, end + 1);
    current_path = current_path.replace(remove, "");
    return current_path;
}

function removeSearch(current_path, input){
    start = current_path.indexOf("search=");
    temp_end = current_path.slice(start).indexOf("&");
    end = current_path.length - current_path.slice(start).length + temp_end;
    remove = current_path.slice(start, end + 1);
    current_path = current_path.replace(remove, "");
    return current_path;
}

function removeSemester(current_path) {
    start = current_path.indexOf("semester=");
    temp_end = current_path.slice(start).indexOf("&");
    end = current_path.length - current_path.slice(start).length + temp_end;
    remove = current_path.slice(start, end + 1);
    current_path = current_path.replace(remove, "");
    return current_path;
}

function changePage(newpage) {
    var current_path = String(window.location.href);
    if(current_path.includes("page=") == true) {
        var index = current_path.indexOf("page=");
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + 5) + newpage + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + "page=" + newpage + "&";
        } else if(current_path.includes("?")) {
            document.location.href = current_path + "page=" + newpage + "&";
        } else {
            document.location.href = current_path + "?page=" + newpage + "&";
        }
    }
};

function clicked() {
    document.getElementById("search-box").click();
};

function deleteFunction() {
    document.getElementById("search-box").value = "";
    current_path = String(window.location.href).replace("http://127.0.0.1:5000/", "");
    var indexOfFirstQuestionMark = current_path.indexOf("?");
    var indexOfFirstAmpersand = current_path.indexOf("&");
    document.location.href = "/"
};

function perm(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var keyword = "perm="
    if(current_path.includes("perm=") == true) {
        var index = current_path.indexOf("perm=");
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + keyword.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + "perm=" + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?perm=" + choice + "&";
        }
    }
    if(choice == "no" && current_path.includes("perm=no") == true) {
        document.location.href = current_path.replace("perm=no&", "")
    }
    if(choice == "yes" && current_path.includes("perm=yes") == true) {
        document.location.href = current_path.replace("perm=yes&", "")
    }
};

function college0(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var cmc = "college[0]="
    if(current_path.includes("college[0]=") === true) {
        var index = current_path.indexOf("college[0]=");
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + "college[0]=".length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + cmc + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + cmc + choice + "&";
        }
    }
    if(choice == "mckenna" && current_path.includes("college[0]=mckenna") === true) {
        document.location.href = current_path.replace("college[0]=mckenna&", "")
    }
};

function college1(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var hmc = "college[1]="
    if(current_path.includes(hmc) === true) {
        var index = current_path.indexOf(hmc);
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + hmc.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + hmc + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + hmc + choice + "&";
        }
    }
    if(choice == "mudd" && current_path.includes("college[1]=mudd") === true) {
        document.location.href = current_path.replace("college[1]=mudd&", "")
    }
};

function college2(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var pz = "college[2]="
    if(current_path.includes(pz) === true) {
        var index = current_path.indexOf(pz);
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + pz.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + pz + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + pz + choice + "&";
        }
    }
    if(choice == "pitzer" && current_path.includes("college[2]=pitzer") === true) {
        document.location.href = current_path.replace("college[2]=pitzer&", "")
    }
};

function college3(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var po = "college[3]="
    if(current_path.includes(po) === true) {
        var index = current_path.indexOf(po);
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + po.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + po + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + po + choice + "&";
        }
    }
    if(choice == "pomona" && current_path.includes("college[3]=pomona") === true) {
        document.location.href = current_path.replace("college[3]=pomona&", "")
    }
};

function college4(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var sc = "college[4]="
    if(current_path.includes(sc) === true) {
        var index = current_path.indexOf(sc);
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + sc.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + sc + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + sc + choice + "&";
        }
    }
    if(choice == "scripps" && current_path.includes("college[4]=scripps") === true) {
        document.location.href = current_path.replace("college[4]=scripps&", "")
    }
};

function college5(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var ks = "college[5]="
    if(current_path.includes(ks) === true) {
        var index = current_path.indexOf(ks);
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + ks.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + ks + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + ks + choice + "&";
        }
    }
    if(choice == "keck" && current_path.includes("college[5]=keck") === true) {
        document.location.href = current_path.replace("college[5]=keck&", "")
    }
};

function college6(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var none = "college[6]="
    if(current_path.includes(none) === true) {
        var index = current_path.indexOf(none);
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + none.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + none + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + none + choice + "&";
        }
    }
    if(choice == "none" && current_path.includes("college[6]=none") === true) {
        document.location.href = current_path.replace("college[6]=none&", "")
    }
};

function prereqs(choice, path) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var keyword = path + choice.toString() + "&";
    if(current_path.includes("&")) {
        document.location.href = current_path + keyword;
    } else {
        document.location.href = current_path.replace("?", "") + "?" + keyword;
    }
    if(choice == "0" && current_path.includes("noprereq0=0") == true) {
        document.location.href = current_path.replace("noprereq0=0&", "")
    }
    if(choice == "1" && current_path.includes("noprereq1=1") == true) {
        document.location.href = current_path.replace("noprereq1=1&", "")
    }
    if(choice == "2" && current_path.includes("noprereq2=2") == true) {
        document.location.href = current_path.replace("noprereq2=2&", "")
    }
};

function majors(obj) {
    var select = document.getElementById("crit-subject");
    var current_path = window.location.href;
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    if(location.href.includes(obj.value.replaceAll(' ', '%20').replaceAll("'", '%27')) == false) {
        var start = current_path.indexOf("major");
        var sub = current_path.slice(start);
        start = sub.indexOf("=")
        var end = sub.indexOf("&");
        document.getElementById("majors").innerHTML = document.getElementById("major").innerHTML;
        if(location.href.includes("?")) {
            document.location.href = location.href + obj.value + "&";
        } else {
            document.location.href = location.href + "?" + obj.value + "&";
        }
    } else {
        document.location.href = current_path;
    }
}

function removemajors(number) {
    var current_path = window.location.href;
    document.getElementById("majors").innerHTML = "Subject";
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    if(current_path.search(number) != -1) {
        var start = current_path.search("major" + number.toString());
        var sub = current_path.slice(start);
        var indexOfFirstAmpersand = sub.indexOf("&");
        var remove = sub.slice(0, indexOfFirstAmpersand + 1);
        var current_path = current_path.replace(remove, "");
        document.location.href = current_path;
    }
};

function gened(obj) {
    var select = document.getElementById("crit-gened");
    var current_path = window.location.href;
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    if(location.href.includes(obj.value.replaceAll(' ', '%20').replaceAll("'", '%27')) == false) {
        // alert(obj.value.replaceAll(' ', '%20').replaceAll("'", '%27'));
        var start = current_path.indexOf("gened");
        var sub = current_path.slice(start);
        start = sub.indexOf("=")
        var end = sub.indexOf("&");
        document.getElementById("geneds").innerHTML = document.getElementById("gened").innerHTML;
        // alert(location.href)
        if(location.href.includes("?")) {
            document.location.href = location.href + obj.value + "&";
        } else {
            document.location.href = location.href + "?" + obj.value + "&";
        }
    } else {
        document.location.href = current_path;
    }
}

function removegeneds(number) {
    var current_path = window.location.href;
    document.getElementById("geneds").innerHTML = "GenEd";
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    if(current_path.search("gened") != -1) {
        // document.getElementById("majors").innerHTML = "All Subjects";
        var start = current_path.search("gened" + number.toString());
        var sub = current_path.slice(start);
        var indexOfFirstAmpersand = sub.indexOf("&");
        var remove = sub.slice(0, indexOfFirstAmpersand + 1);
        var current_path = current_path.replace(remove, "");
        document.location.href = current_path;
    }
};

function removemajors(number) {
    var current_path = window.location.href;
    document.getElementById("majors").innerHTML = "Subject";
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    if(current_path.search(number) != -1) {
        var start = current_path.search("major" + number.toString());
        var sub = current_path.slice(start);
        var indexOfFirstAmpersand = sub.indexOf("&");
        var remove = sub.slice(0, indexOfFirstAmpersand + 1);
        var current_path = current_path.replace(remove, "");
        document.location.href = current_path;
    }
};

function schools(obj) {
    var current_path = window.location.href;
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    if(document.getElementById("schools").value == "all") {
        // document.location.href = current_path.replace("school=all&", "")
        // if (obj.value = "all") {
        var first = current_path.indexOf('school=');
        remove = current_path.slice(first);
        last = remove.indexOf("&");
        remove = remove.slice(0, last + 1);
        new_path = current_path.replace(remove, "");
        document.location.href = new_path;
        // }
    } else {
        var keyword = "school="
        if(current_path.includes("school=") === true) {
            var index = current_path.indexOf("school=");
            var subpath = current_path.slice(index);
            var indexOfFirstAmpersand = subpath.indexOf("&");
            document.location.href = current_path.slice(0, index + keyword.length) + obj.value + subpath.slice(indexOfFirstAmpersand);
        } else {
            if(current_path.includes("&")) {
                document.location.href = current_path + "school=" + obj.value + "&";
            } else {
                document.location.href = current_path.replace("?", "") + "?school=" + obj.value + "&";
            }
        }
    }
};

function concurrent(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var keyword = "concurrent="
    if(current_path.includes("concurrent=") === true) {
        var index = current_path.indexOf("concurrent=");
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + keyword.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + "concurrent=" + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?concurrent=" + choice + "&";
        }
    }
    if(choice == "no" && current_path.includes("concurrent=no") === true) {
        document.location.href = current_path.replace("concurrent=no&", "")
    }
    if(choice == "yes" && current_path.includes("concurrent=yes") === true) {
        document.location.href = current_path.replace("concurrent=yes&", "")
    }
};

function searchFunction() {
    var input;
    input = document.getElementById("search-box").value;
    current_path = window.location.href;
    if(current_path.includes("page=")) {
        current_path = removePage(current_path)
    }
    if(input != "") {
        var indexOfFirstQuestionMark = current_path.indexOf("?");
        var indexOfFirstAmpersand = current_path.indexOf("&");
        var indexOfFirstEqual = current_path.indexOf("=")
        tailpath = current_path.slice(indexOfFirstQuestionMark + 1);
        if(current_path.includes("search=") === false) {
            if(current_path.includes("&") === true) {
                document.location.href = current_path.slice(0, indexOfFirstQuestionMark + 1) + "search=" + input + "&" + tailpath;
            } else {
                current_path = current_path.replace(window.location.href, "");
                document.location.href = current_path.replace("?", "") + "?search=" + input + "&";
            }
        } else {
            document.location.href = current_path.slice(0, indexOfFirstEqual + 1) + input + current_path.slice(indexOfFirstAmpersand)
        }
    } else {
        var indexOfFirstQuestionMark = current_path.indexOf("?");
        var indexOfFirstAmpersand = current_path.indexOf("&");
        remove = current_path.slice(indexOfFirstQuestionMark + 1, indexOfFirstAmpersand + 1)
        if(current_path.includes("&") === true) {
            alert(current_path)
            document.location.href = current_path.replace(remove, "")
        }
    }
};


function corequisites(choice) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var keyword = "corequisite="
    if(current_path.includes("corequisite=") === true) {
        var index = current_path.indexOf("corequisite=");
        var subpath = current_path.slice(index);
        var indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + keyword.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + "corequisite=" + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?corequisite=" + choice + "&";
        }
    }
    if(choice == "no" && current_path.includes("corequisite=no") === true) {
        document.location.href = current_path.replace("corequisite=no&", "")
    }
    if(choice == "yes" && current_path.includes("corequisite=yes") === true) {
        document.location.href = current_path.replace("corequisite=yes&", "")
    }
};
window.onload = function() {
    document.getElementById('search-box').click();
};

function year(choice, path) {
    var current_path = String(window.location.href);
    if(current_path.search("page=") != -1) {
        current_path = removePage(current_path);
    }
    var keyword = path + choice.toString() + "&";
    if(current_path.includes("&")) {
        document.location.href = current_path + keyword;
    } else {
        document.location.href = current_path.replace("?", "") + "?" + keyword;
    }
    if(current_path.includes("semester=" + choice + "&") == true) {
        document.location.href = current_path.replace("semester=" + choice + "&", "")
    }
};

function clearAll() {
    current_path = window.location.href;
    firstIndex = current_path.search("search=")
    if(firstIndex == -1) {
        document.location.href = '/'
    } else {
        sub = current_path.slice(firstIndex);
        lastIndex = sub.search("&");
        sub = sub.slice(0, lastIndex + 1);
        document.location.href = '/?' + sub;
    }
}

function report() {
    window.open("https://forms.gle/QWgGpB2sjYF6RQBN7")
};

function upload(folder) {
    current_path = window.location.href;
    if(current_path.includes("&") === false) {
        document.location.href = current_path + "?" + "upload=" + folder + "&";
    } else {
        document.location.href = current_path + "upload=" + folder + "&";
    }
};

function upload(id) {
    document.getElementById(id).addEventListener('click', openDialog);
}

function openDialog(courseid) {
    document.getElementById(courseid).click();
}
document.onkeydown = function(e) {
    if(e.code == "F12") {
        return false;
    }
    if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) {
        return false;
    }
    if(e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) {
        return false;
    }
    if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) {
        return false;
    }
    if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) {
        return false;
    }
}

function buttontoggle() {
    var n = document.querySelector(".scrolling_filtering_system");
    n.classList.toggle("xuKXj22n");
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }


function darkmode() {
    var darkmode = getCookie("darkmode");
    var element = document.body;
    element.classList.toggle("mode-dark");
    if(darkmode == ''){
        document.cookie = "darkmode=on";
    }
    else{
        document.cookie = "darkmode=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }
  }
