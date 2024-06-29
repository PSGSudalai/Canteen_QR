// Function to toggle popup visibility
function togglePopup() {
    var popup = document.getElementById("balance-popup");
    popup.classList.toggle("show");
}

// Function to show cart popup for a few seconds
function showCartPopup() {
    var cartPopup = document.getElementById("cart-popup");
    cartPopup.classList.add("show");
    setTimeout(function() {
        cartPopup.classList.remove("show");
    }, 3000); // Adjust the duration (in milliseconds) as needed
}

// Event listener for add to cart form submission
document.addEventListener("DOMContentLoaded", function() {
    var addToCartForms = document.querySelectorAll("form[action='{% url 'add_to_cart' %}']");
    addToCartForms.forEach(function(form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            var formData = new FormData(form);
            var quantity = formData.get("quantity");
            // You can handle the form submission here (e.g., via fetch or XMLHttpRequest)
            // For demonstration, we'll just show the cart popup
            showCartPopup();
        });
    });
});
