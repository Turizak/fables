document.addEventListener('DOMContentLoaded', function() {
  const nameInput = document.getElementById('name');
  const createBtn = document.getElementById('create-btn');
  
  function toggleButton() {
    createBtn.disabled = nameInput.value.trim() === '';
  }
  
  nameInput.addEventListener('input', toggleButton);
  toggleButton(); // Check initial state
});