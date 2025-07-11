document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector(".search-bar");
  const pharmacyList = document.getElementById("pharmacy-list");
  const noResults = document.getElementById("no-results");

  function fetchPharmacies(query = "") {
    fetch(`/api/pharmacies?search=${query}`)
      .then(response => response.json())
      .then(data => {
        pharmacyList.innerHTML = "";

        if (data.length === 0) {
          noResults.style.display = "block";
          return;
        } else {
          noResults.style.display = "none";
        }

        data.forEach(pharmacy => {
          const card = document.createElement("div");
          card.className = "pharmacy-card";
          card.innerHTML = `
            <div class="pharmacy-header">
              <div>
                <h2>${pharmacy.name}</h2>
                <p>${pharmacy.location}</p>
              </div>
              <button class="toggle-btn">View details ▼</button>
            </div>
            <div class="medicine-box">
              ${pharmacy.medicines.map(med => `
                <h3>${med.name}</h3>
                <p><strong>Price:</strong> ${med.price} birr</p>
                <p><strong>Dosage:</strong> ${med.dosage}</p>
                <p><strong>Medicine descriptions:</strong><br/>${med.description}</p>
                <hr>
              `).join('')}
            </div>
          `;
          pharmacyList.appendChild(card);
        });

        // Re-add toggle button functionality
        document.querySelectorAll(".toggle-btn").forEach(button => {
          button.addEventListener("click", () => {
            const medicineBox = button.closest(".pharmacy-card").querySelector(".medicine-box");
            if (medicineBox.style.display === "none" || medicineBox.style.display === "") {
              medicineBox.style.display = "block";
              button.textContent = "Hide details ▲";
            } else {
              medicineBox.style.display = "none";
              button.textContent = "View details ▼";
            }
          });
        });
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }

  // Initial load
  fetchPharmacies();

  // On search input
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim();
    fetchPharmacies(query);
  });
});
