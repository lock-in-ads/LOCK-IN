document.addEventListener('DOMContentLoaded', function () {
  var confirmDeleteModal = document.getElementById('confirmDeleteModal');
  confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
      var button = event.relatedTarget;
      var url = button.getAttribute('data-url');  
      var name = button.getAttribute('data-name'); 

      // Change model
      var nameSpan = confirmDeleteModal.querySelector('#name');
      nameSpan.textContent = name;

      // Update url form in modal
      var form = confirmDeleteModal.querySelector('#deleteForm');
      form.action = url;
  });
});