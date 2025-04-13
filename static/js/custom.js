const lockerStart = '<a class="locker"><div class="wrapper"><div class="lock"><ul><li></li></ul></div><ul class="air"><li></li><li></li><li></li></ul></div><h2>';
const lockerEnd = '</h2></a>';
const quickAssignment = document.getElementById("quick-assignment");
const lockers = quickAssignment.getElementsByClassName("locker");

function addLockers(amount) {
    for(i=2; i <= amount; i++) {
        let lockerHtml = lockerStart + i + lockerEnd;
        if (i <= 9){
            lockerHtml = lockerStart + "0" + i + lockerEnd;
        }        
        quickAssignment.insertAdjacentHTML('beforeend', lockerHtml);
    }
}

function changeLockers(){
    for (i=0; i <= lockers.length; i++){
        let lockerNumber = i + 1;
        lockers[i].classList.add(lockerNumber);
        if(((lockerNumber%2 == 0) && (lockerNumber%5 == 0)) || (lockerNumber%3 == 0) || (lockerNumber>54 && lockerNumber<61)){
            lockers[i].classList.add("unavailable");           
        }
    }
}

addLockers(80);
changeLockers();