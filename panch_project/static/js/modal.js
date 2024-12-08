// modal.js

// Open modal and set the image source
function openImageModal(imageUrl) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImage");
    var captionText = document.getElementById("caption");
    modal.style.display = "block";
    modalImg.src = imageUrl;
    captionText.innerHTML = imageUrl;
}

// Close the modal
function closeImageModal() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}
