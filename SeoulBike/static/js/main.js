// static/js/main.js
document.querySelectorAll('input[type=radio][name="gender"]').forEach(radio => {
  radio.addEventListener('change', () => {
    document.querySelectorAll('label[for="inlineRadio1"], label[for="inlineRadio2"]').forEach(label => {
      label.style.fontWeight = 'normal';
    });
    document.querySelector('label[for="' + radio.id + '"]').style.fontWeight = 'bold';
  });
});
