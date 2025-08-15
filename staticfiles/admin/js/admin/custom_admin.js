document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("td.field-hs_code a").forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();  // Prevent default link behavior
            window.open(this.href, "EditHsCode", "width=800,height=600,resizable=yes");
        });
    });
});
