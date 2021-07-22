document.onkeydown = function(e) {
    if(event.keyCode == 123) {
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

function changePage(newpage) {
    const current_path = String(window.location.href);
    if(current_path.includes("page=") == true) {
        const index = current_path.indexOf("page=");
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + 5) + newpage + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
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
    const indexOfFirstQuestionMark = current_path.indexOf("?");
    const indexOfFirstAmpersand = current_path.indexOf("&");
    document.location.href = "/"
};

function perm(choice) {
    const current_path = String(window.location.href);
    var keyword = "perm="
    if(current_path.includes("perm=") == true) {
        const index = current_path.indexOf("perm=");
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
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
    const current_path = String(window.location.href);
    const cmc = "college[0]="
    if(current_path.includes("college[0]=") == true) {
        const index = current_path.indexOf("college[0]=");
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + "college[0]=".length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + cmc + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + cmc + choice + "&";
        }
    }
    if(choice == "mckenna" && current_path.includes("college[0]=mckenna") == true) {
        document.location.href = current_path.replace("college[0]=mckenna&", "")
    }
};

function college1(choice) {
    const current_path = String(window.location.href);
    const hmc = "college[1]="
    if(current_path.includes(hmc) == true) {
        const index = current_path.indexOf(hmc);
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + hmc.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + hmc + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + hmc + choice + "&";
        }
    }
    if(choice == "mudd" && current_path.includes("college[1]=mudd") == true) {
        document.location.href = current_path.replace("college[1]=mudd&", "")
    }
};

function college2(choice) {
    const current_path = String(window.location.href);
    const pz = "college[2]="
    if(current_path.includes(pz) == true) {
        const index = current_path.indexOf(pz);
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + pz.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + pz + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + pz + choice + "&";
        }
    }
    if(choice == "pitzer" && current_path.includes("college[2]=pitzer") == true) {
        document.location.href = current_path.replace("college[2]=pitzer&", "")
    }
};

function college3(choice) {
    const current_path = String(window.location.href);
    const po = "college[3]="
    if(current_path.includes(po) == true) {
        const index = current_path.indexOf(po);
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + po.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + po + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + po + choice + "&";
        }
    }
    if(choice == "pomona" && current_path.includes("college[3]=pomona") == true) {
        document.location.href = current_path.replace("college[3]=pomona&", "")
    }
};

function college4(choice) {
    const current_path = String(window.location.href);
    const sc = "college[4]="
    if(current_path.includes(sc) == true) {
        const index = current_path.indexOf(sc);
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + sc.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + sc + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + sc + choice + "&";
        }
    }
    if(choice == "scripps" && current_path.includes("college[4]=scripps") == true) {
        document.location.href = current_path.replace("college[4]=scripps&", "")
    }
};

function college5(choice) {
    const current_path = String(window.location.href);
    const ks = "college[5]="
    if(current_path.includes(ks) == true) {
        const index = current_path.indexOf(ks);
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + ks.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + ks + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?" + ks + choice + "&";
        }
    }
    if(choice == "keck" && current_path.includes("college[5]=keck") == true) {
        document.location.href = current_path.replace("college[5]=keck&", "")
    }
};

function prereqs(choice, path) {
    const current_path = String(window.location.href);
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

function removemajors() {
    var current_path = window.location.href;
    document.getElementById("majors").innerHTML = "Subject";
    if(current_path.includes("major") == true) {
        // document.getElementById("majors").innerHTML = "All Subjects";
        var start = current_path.indexOf("major");
        var sub = current_path.slice(start);
        var indexOfFirstAmpersand = sub.indexOf("&");
        var end = current_path.slice(0, start).length + indexOfFirstAmpersand;
        var remove = current_path.slice(start, end + 1);
        var new_path = current_path.replace(remove, "");
        document.location.href = new_path;
    }
};

function majors(obj) {
    var select = document.getElementById("crit-subject");
    const current_path = window.location.href;
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
}

function schools(obj) {
    const current_path = String(window.location.href);
    var keyword = "school="
        //document.getElementById("schools").innerHTML = document.getElementById("school").innerHTML
    if(current_path.includes("school=") == true) {
        const index = current_path.indexOf("school=");
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + keyword.length) + obj.value + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + "school=" + obj.value + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?school=" + obj.value + "&";
        }
    }
};

function concurrent(choice) {
    const current_path = String(window.location.href);
    var keyword = "concurrent="
    if(current_path.includes("concurrent=") == true) {
        const index = current_path.indexOf("concurrent=");
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + keyword.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + "concurrent=" + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?concurrent=" + choice + "&";
        }
    }
    if(choice == "no" && current_path.includes("concurrent=no") == true) {
        document.location.href = current_path.replace("concurrent=no&", "")
    }
    if(choice == "yes" && current_path.includes("concurrent=yes") == true) {
        document.location.href = current_path.replace("concurrent=yes&", "")
    }
};

function searchFunction(event) {
    var input;
    input = document.getElementById("search-box").value.toLowerCase();
    current_path = window.location.href;
    if(event.code === "Enter") {
        setTimeout(function() {
            if(current_path.includes("page=")) {
                start = current_path.indexOf("page=");
                temp_end = current_path.slice(start).indexOf("&");
                end = current_path.length - current_path.slice(start).length + temp_end;
                remove = current_path.slice(start, end + 1);
                current_path = current_path.replace(remove, "");
                i = current_path.indexOf("?");
                new_path = current_path.slice(0, i + 1) + "search=" + input + "&" + current_path.slice(i + 1);
                document.location.href = new_path;
            } else {
                if(input != "") {
                    const indexOfFirstQuestionMark = current_path.indexOf("?");
                    const indexOfFirstAmpersand = current_path.indexOf("&");
                    const indexOfFirstEqual = current_path.indexOf("=")
                    tailpath = current_path.slice(indexOfFirstQuestionMark + 1);
                    if(current_path.includes("search=") == false) {
                        if(current_path.includes("&") == true) {
                            document.location.href = current_path.slice(0, indexOfFirstQuestionMark + 1) + "search=" + input + "&" + tailpath;
                        } else {
                            current_path = current_path.replace(window.location.href, "");
                            document.location.href = window.location.href.replace("?", "") + "?search=" + input + "&";
                        }
                    } else {
                        document.location.href = current_path.slice(0, indexOfFirstEqual + 1) + input + current_path.slice(indexOfFirstAmpersand)
                    }
                } else {
                    const indexOfFirstQuestionMark = current_path.indexOf("?");
                    const indexOfFirstAmpersand = current_path.indexOf("&");
                    remove = current_path.slice(indexOfFirstQuestionMark + 1, indexOfFirstAmpersand + 1)
                    if(current_path.includes("&") == true) {
                        document.location.href = current_path.replace(remove, "")
                    }
                }
            }
        }, 500)
    }
};

function corequisites(choice) {
    const current_path = String(window.location.href);
    var keyword = "corequisite="
    if(current_path.includes("corequisite=") == true) {
        const index = current_path.indexOf("corequisite=");
        const subpath = current_path.slice(index);
        const indexOfFirstAmpersand = subpath.indexOf("&");
        document.location.href = current_path.slice(0, index + keyword.length) + choice + subpath.slice(indexOfFirstAmpersand);
    } else {
        if(current_path.includes("&")) {
            document.location.href = current_path + "corequisite=" + choice + "&";
        } else {
            document.location.href = current_path.replace("?", "") + "?corequisite=" + choice + "&";
        }
    }
    if(choice == "no" && current_path.includes("corequisite=no") == true) {
        document.location.href = current_path.replace("corequisite=no&", "")
    }
    if(choice == "yes" && current_path.includes("corequisite=yes") == true) {
        document.location.href = current_path.replace("corequisite=yes&", "")
    }
};

function year(sem) {
    current_path = window.location.href;
    if(current_path.includes("&") == false) {
        document.location.href = current_path + "?" + "semester=" + sem + "&";
    } else {
        document.location.href = current_path + "semester=" + sem + "&";
    }
};

function clearAll() {
    document.location.href = '/'
}

function year(sem) {
    current_path = window.location.href;
    if(current_path.includes("&") == false) {
        document.location.href = current_path + "?" + "semester=" + sem + "&";
    } else {
        document.location.href = current_path + "semester=" + sem + "&";
    }
};
                    
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

  function displayReport() {
    var x = document.getElementById("report_form");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }	
  
  function addtoPlanner(code) {
    var planner = getCookie(code);
    var element = document.getElementById('planner');
    if(planner == ''){
        document.cookie = code + "=on";
        element.innerHTML = "<strong> Remove from My Courses </strong>";
    }
    else{
        document.cookie = code + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; url=http://127.0.0.1:5000/";
        element.innerHTML = "<strong> Add to My Courses </strong>";
    }						  
    }					  				  