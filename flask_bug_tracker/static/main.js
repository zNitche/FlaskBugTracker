function toggleNavbarDropdown() {
    const dropdown = document.getElementById("nav-dropdown");

    dropdown.classList.toggle("displayed");
}


function toggleCollapsible(collapsibleContentID) {
    const collapsibleContent = document.getElementById(collapsibleContentID);

    collapsibleContent.classList.toggle("active-collapsible");
}
