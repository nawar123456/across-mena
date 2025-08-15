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


// document.addEventListener("DOMContentLoaded", function() {
//     function updateFullImportFee() {
//         // Get all rows in the admin list view
//         document.querySelectorAll("tr").forEach(row => {
//             let importFeeInput = row.querySelector("td.field-import_fee input");
//             // let serAllInput = row.querySelector("td.field-ser_all input");
//             let fullImportFeeField = row.querySelector("td.field-full_import_fee input");

//             if (importFeeInput && serAllInput && fullImportFeeField) {
//                 function calculate() {
//                     let importFee = parseFloat(importFeeInput.value) || 0;
//                     let serAll = parseFloat(serAllInput.value) || 0;
//                     let fullImportFee = importFee + serAll;
                    
//                     fullImportFeeField.value = fullImportFee.toFixed(2);  // ✅ Update field dynamically
//                 }

//                 // Call function when values change
//                 importFeeInput.addEventListener("input", calculate);
//                 serAllInput.addEventListener("input", calculate);
                
//                 // Run on page load
//                 calculate();
//             }
//         });
//     }

//     updateFullImportFee();
// });

