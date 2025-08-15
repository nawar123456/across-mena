document.addEventListener("DOMContentLoaded", function () {
    function addPopupListeners() {
        document.querySelectorAll("td.field-item").forEach(cell => {
            let hsCodeText = cell.innerText.trim();  // Get the hs_code value
            let row = cell.closest("tr");  // Get the table row
            let editLink = row.querySelector("a.edit-pen");  // Find the edit link in the row

            if (editLink) {
                cell.style.cursor = "pointer";  // Show pointer cursor when hovering
                cell.addEventListener("click", function (event) {
                    event.preventDefault();
                    let popup = window.open(editLink.href, "EditHsCODE", "width=800,height=600,resizable=yes");
                    if (popup) {
                        popup.focus();
                    } else {
                        alert("Popup blocked! Allow popups for this site.");
                    }
                });
            }
        });
    }

    // ✅ Run immediately to add event listeners
    addPopupListeners();

    console.log("✅ Custom admin JS loaded successfully!");
});

// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelectorAll("input[name='import_fee'], input[name='export_fee'], input[name='services_allowance']").forEach(input => {
//         input.addEventListener("input", function () {
//             this.value = this.value.replace(/[^0-9.]/g, "");  // ✅ Allow only numbers and decimal points
//         });
//     });
// });
document.addEventListener("DOMContentLoaded", function () {
    let rows = document.querySelectorAll("tr");

    rows.forEach(row => {
        let checkingColumn = row.querySelector("td.field-checking");
        if (checkingColumn && checkingColumn.innerText.trim() === "True") {
            row.style.backgroundColor = "#D4EDDA";  // ✅ Light green background
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".checking-toggle").forEach(function (el) {
        el.addEventListener("click", function () {
            let itemId = this.getAttribute("data-id");
            let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            fetch(`/admin/custom/toggle-checking/${itemId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let row = el.closest("tr");
                    if (data.new_status) {
                        row.classList.add("row-red");  // ✅ Add red background if True
                    } else {
                        row.classList.remove("row-red");  // ❌ Remove red background if False
                    }
                    el.textContent = data.new_status ? "✅" : "❌"; // Toggle the text
                }
            });
        });
    });
});


