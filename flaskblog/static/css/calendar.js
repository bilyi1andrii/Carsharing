document.getElementById("rentalForm").addEventListener("submit", function(event) {
  event.preventDefault();
  
  var startDate = document.getElementById("startDate").value;
  var endDate = document.getElementById("endDate").value;
  
  // Тут можна виконати додаткову обробку вибраних дат, наприклад, перевірку на правильність чи наявність конкретних дат.
  
  // При необхідності можна виконати подальші дії, наприклад, відправити дані на сервер або відобразити повідомлення про успішне заповнення форми.
  
  console.log("Початок оренди:", startDate);
  console.log("Кінець оренди:", endDate);
});