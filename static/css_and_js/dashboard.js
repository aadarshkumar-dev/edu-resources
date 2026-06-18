const male = document.querySelector(".male");
const female = document.querySelector(".female");
const come_on_edit = document.querySelectorAll(".come-on-edit");
const go_on_edit = document.querySelectorAll(".go-on-edit");
const edit = document.querySelector(".edit");

function activate(active, inactive) {
    active.style.backgroundColor = "rgb(0, 153, 255)";
    active.style.color = "white";
    inactive.style.backgroundColor = "white";
    inactive.style.color = "rgb(0, 153, 255)";
}

male.addEventListener("click", () => activate(male, female));
female.addEventListener("click", () => activate(female, male));


let editing = false;

edit.addEventListener("click", () => {
    if (!editing) {
        come_on_edit.forEach(el => el.style.display = "flex");
        go_on_edit.forEach(el => el.style.display = "none");
        edit.textContent = "Cancel";
        editing = true;
    } else {
        come_on_edit.forEach(el => el.style.display = "none");
        go_on_edit.forEach(el => el.style.display = "inline-block");
        edit.textContent = "Edit";
        editing = false;
    }
});


