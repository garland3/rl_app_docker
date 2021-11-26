function clickableGrid(rows, cols, callback_clicked) {
    var i = 0;
    var grid = document.createElement('table');
    grid.className = 'grid';
    for (var r = 0; r < rows; ++r) {
        var tr = grid.appendChild(document.createElement('tr'));
        for (var c = 0; c < cols; ++c) {
            var cell = tr.appendChild(document.createElement('td'));
            cell.id = "c" + i;
            cell.innerHTML = ++i;

            // register the call back if the user clicks on the item. 
            cell.addEventListener('click', (function (el, r, c, i) {
                return function () {
                    callback_clicked(el, r, c, i);
                }
            })(cell, r, c, i), false);
        }
    }
    return grid;
}

var lastClicked;
function grid_item_click(el, row, col, i) {
    // console.log("You clicked on element:",el);
    // console.log("You clicked on row:",row);
    // console.log("You clicked on col:",col);
    // console.log("You clicked on item #:",i);
    if (el.className == 'fixed_bc') { el.className = ''; } // clear a click
    else { el.className = 'fixed_bc'; }
    // if (lastClicked) lastClicked.className='';
    lastClicked = el; // record the clast clicked in case we want to change to a loading condition
}

function grid_item_keydown(event) {

    // console.log("a key down event was logged. ");
    // console.log(event.key);
    if (event.key == "ArrowRight") {
        // console.log("right");
        event.preventDefault();
        lastClicked.className = 'right';
    }
    if (event.key == "ArrowLeft") {
        // console.log("left");
        event.preventDefault();
        lastClicked.className = 'left';
    }
    if (event.key == "ArrowUp") {
        // console.log("up");
        event.preventDefault();
        lastClicked.className = 'up';
    }
    if (event.key == "ArrowDown") {
        // console.log("down");
        event.preventDefault();
        lastClicked.className = 'down';
    }
}


function geneate_config_object() {
    // console.log("submit clicked. ");
    var fixed_bcs = document.getElementsByClassName('fixed_bc');
    var rights = document.getElementsByClassName('right');
    var lefts = document.getElementsByClassName('left');
    var ups = document.getElementsByClassName('up');
    var downs = document.getElementsByClassName('down');
    var volfract = document.getElementById("percentage")

    var names = ['bcs', 'rights', 'lefts', 'ups', 'downs'];
    var collections = [fixed_bcs, rights, lefts, ups, downs];

    // Collect everything into a json object. 
    var json = {};
    var i = 0;
    names.forEach(name => {
        var collection = collections[i];
        var item_numbers = [];
        Array.from(collection).forEach(element => {
            item_numbers.push(element.innerHTML); // add to the array
        });
        json[name] = item_numbers;
        i++;
    });
    // add the vol fraction
    json['volfraction'] = volfract.value;
    console.log(json);
    return json;
}

var myresults = "";
function apply_results(json) {
    myresults = json;
    // console.log(json);
    mytop = json.Topology[0];
    // console.log("topology array is " + mytop);
    mytop.forEach(update_cell);
}

function update_cell(value, index, array) {
    value = parseInt(value);
    var no_change = value == 0;
    var cellid = "c" + index;
    var cell = document.getElementById(cellid);
    // console.log("calling value "+value+no_change+index);
    if (no_change) { cell.className = "not_material"; }
    else { cell.className = "material"; }
}

///
/// global var for the interval timer. 
///
var INTERVAL_TIMER_ID = 0;
var INTERVAL_COUNTER = 0;
var MAX_INTERVAL_COUNTER = 1000;
var FASTER_INTERVAL_TIME_TILL_RECHECK_MILLI = 500;
var USING_FAST_INTERVAL = false;
var INTERVAL_TIME_TILL_CHECK_IF_STARTED = 1500;
var RESPONSE_OJB = null;
var REPONSE_OBJ_PRE_JSON = null;
var SUBMIT_BUTTON = document.getElementById('submit');


var job_id = 1;


function check_interval_counter(){
    if (INTERVAL_COUNTER > 2 * MAX_INTERVAL_COUNTER) {
        window.clearInterval(INTERVAL_TIMER_ID);
        SUBMIT_BUTTON.removeAttribute("disabled");
        SUBMIT_BUTTON.classList.replace("btn-success", "btn-primary");
        SUBMIT_BUTTON.innerText = "Timed out. Something failed. Submit for Design";
    }

}

function check_design_finished() {
    var json = { 'job_id': job_id };

    const options = {
        method: 'POST',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    }

    fetch(check_if_done_url, options)
        .then(res => res.json())
        .then(function (res) {
            // response_pre_json = res;
            var t = typeof (res);
            console.log("type of is " + t);
            if (t == 'object') { console.log(res) }
            else { res = JSON.parse(res); }
            RESPONSE_OJB = res;
            console.log("check if done response is " + res);
            if ("intermediate_results" in res && res['intermediate_results']== true) {
                if (USING_FAST_INTERVAL == false){
                    // basically, pick up the pass on checking for updates. 
                    USING_FAST_INTERVAL = true;
                    window.clearInterval(INTERVAL_TIMER_ID);
                    INTERVAL_TIMER_ID = window.setInterval(check_design_finished, FASTER_INTERVAL_TIME_TILL_RECHECK_MILLI);
                }

                console.log("Some intermediate results to apply. ")
                apply_results(res.result);
                var message = "Applying initial results: " + INTERVAL_COUNTER + " of " + MAX_INTERVAL_COUNTER;
                console.log(message);
                SUBMIT_BUTTON.innerText = message;
                INTERVAL_COUNTER += 1;
                check_interval_counter();
            }
            else {
                if ("final_result" in res && res['final_result']== true) {
                    console.log("Applying results");
                    apply_results(res.result);
                    SUBMIT_BUTTON.removeAttribute("disabled");
                    SUBMIT_BUTTON.classList.replace("btn-success", "btn-primary");
                    SUBMIT_BUTTON.innerText = "Submit for Design";
                    window.clearInterval(INTERVAL_TIMER_ID);
                    USING_FAST_INTERVAL = false;
                } else {
                    var position = res['position'];
                    if (position == 0) {
                        var message = "Working on your design " + INTERVAL_COUNTER + " of " + MAX_INTERVAL_COUNTER;
                        console.log(message);
                        SUBMIT_BUTTON.innerText = message;
                        INTERVAL_COUNTER += 1;
                        check_interval_counter();
                    } else {
                        // switch the 1st char back and forth to make it look like it's doing something
                        var firstchar = SUBMIT_BUTTON.innerText[0];
                        if (firstchar=="."){
                            firstchar = "__";
                        } else{
                            firstchar=".."
                        }
                        var message = firstchar+"In the design queue. Your position is " + position;
                        console.log(message);
                        SUBMIT_BUTTON.innerText = message;
                    }

                }
            }


        })
        .catch(function (err) {
            console.log("Failed in check_design_finiished " + err);
            SUBMIT_BUTTON.removeAttribute("disabled");
            SUBMIT_BUTTON.classList.replace("btn-success", "btn-primary");
            SUBMIT_BUTTON.innerText = "Failed. Try again. Submit for Design";
            window.clearInterval(INTERVAL_TIMER_ID);
        });

}





function submit_clicked(event, target_url) {

    var att = document.createAttribute("disabled")
    SUBMIT_BUTTON.setAttributeNode(att);
    SUBMIT_BUTTON.classList.replace("btn-primary", "btn-success");
    SUBMIT_BUTTON.innerText = "Working! This might take a few moments. ";

    var json = geneate_config_object();
    // console.log(target_url, json);
    const options = {
        method: 'POST',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    console.log("submitting config for design");
    // send post request
    // send post request
    fetch(target_url, options)
        .then(res => res.json())
        .then(function (res) {
            console.log("Got response" + res);
            if ('id' in res) {
                job_id = res['id'];
                console.log("saving job_id " + job_id);
            }
            // 888888888888
            //        SET UP a  timer to check the server. if 
            //8888888888888
            INTERVAL_COUNTER = 0;
            INTERVAL_TIMER_ID = window.setInterval(check_design_finished, INTERVAL_TIME_TILL_CHECK_IF_STARTED);
            USING_FAST_INTERVAL = false;
        })
        .catch(function (err) {
            SUBMIT_BUTTON.removeAttribute("disabled");
            SUBMIT_BUTTON.classList.replace("btn-success", "btn-primary");
            SUBMIT_BUTTON.innerText = "Failed. Try again. Submit for Design";
            console.log(err);
        });
}

function downloadObjectAsJson(exportObj, exportName) {
    // https://stackoverflow.com/a/30800715/1319433
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

function download_config_clicked(event) {
    var json = geneate_config_object();
    downloadObjectAsJson(json, "config");
}

var n = 24;
var grid = clickableGrid(n, n, grid_item_click);
document.getElementById("grid_here").appendChild(grid);
//listen for key downs to place the loading conditions. 
document.addEventListener('keydown', grid_item_keydown);
document.getElementById('submit').addEventListener('click', function (event) { submit_clicked(event, submit_job_clicked_url) });


document.getElementById('download_config').addEventListener('click', function (event) { download_config_clicked(event) });