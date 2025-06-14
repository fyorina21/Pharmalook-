// Medication data
const medications = [
    'Acetaminophen', 'Ibuprofen', 'Aspirin', 'Amoxicillin', 'Lisinopril',
    'Metformin', 'Atorvastatin', 'Omeprazole', 'Losartan', 'Gabapentin',
    'Sertraline', 'Tramadol', 'Trazodone', 'Fluoxetine', 'Hydrochlorothiazide'
];

// Mock pharmacy data
const mockPharmacies = [
    {
        name: "HealthPlus Pharmacy",
        address: "123 Main St, Downtown",
        distance: "0.5 km",
        phone: "+1 555-0123",
        hours: "8:00 AM - 10:00 PM"
    },
    {
        name: "MediCare Drugstore",
        address: "456 Oak Ave, City Center", 
        distance: "1.2 km",
        phone: "+1 555-0456",
        hours: "9:00 AM - 9:00 PM"
    },
    {
        name: "QuickMed Pharmacy",
        address: "789 Pine Rd, Uptown",
        distance: "2.1 km", 
        phone: "+1 555-0789",
        hours: "24 Hours"
    }
];

// Get DOM elements from your HTML
const medicationInput = document.querySelector('input[placeholder="search for medicine"]');
const locationInput = document.querySelector('input[placeholder=""]');
const findButton = document.querySelector('button');

// Create autocomplete dropdown for medication search
const suggestionsContainer = document.createElement('div');
suggestionsContainer.className = 'absolute w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-40 overflow-y-auto z-10 hidden';
suggestionsContainer.style.top = '100%';
medicationInput.parentElement.style.position = 'relative';
medicationInput.parentElement.appendChild(suggestionsContainer);

// Medication input functionality
medicationInput.addEventListener('input', function(e) {
    const value = e.target.value.toLowerCase();
    
    if (value.length > 0) {
        const matches = medications.filter(med => 
            med.toLowerCase().includes(value)
        );
        
        if (matches.length > 0) {
            suggestionsContainer.innerHTML = '';
            matches.forEach(medication => {
                const suggestion = document.createElement('div');
                suggestion.className = 'px-4 py-2 hover:bg-green-50 cursor-pointer text-sm';
                suggestion.textContent = medication;
                suggestion.addEventListener('click', () => {
                    medicationInput.value = medication;
                    suggestionsContainer.classList.add('hidden');
                });
                suggestionsContainer.appendChild(suggestion);
            });
            suggestionsContainer.classList.remove('hidden');
        } else {
            suggestionsContainer.classList.add('hidden');
        }
    } else {
        suggestionsContainer.classList.add('hidden');
    }
});

// Hide suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (!medicationInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
        suggestionsContainer.classList.add('hidden');
    }
});

// Find pharmacy button functionality
findButton.addEventListener('click', function() {
    const medication = medicationInput.value.trim();
    const location = locationInput.value.trim();
    
    if (!medication) {
        alert('Please enter a medication name');
        return;
    }
    
    if (!location) {
        alert('Please enter your location');
        return;
    }
    
    // Change button text while "searching"
    const originalText = findButton.textContent;
    findButton.textContent = 'Searching...';
    findButton.disabled = true;
    
    // Simulate search delay
    setTimeout(() => {
        findButton.textContent = originalText;
        findButton.disabled = false;
        displayPharmacyResults();
    }, 1500);
});

// Display pharmacy results
function displayPharmacyResults() {
    // Remove existing results if any
    const existingResults = document.getElementById('pharmacy-results');
    if (existingResults) {
        existingResults.remove();
    }
    
    // Create results section
    const resultsSection = document.createElement('section');
    resultsSection.id = 'pharmacy-results';
    resultsSection.className = 'max-w-4xl mx-auto mt-8 px-4';
    
    const title = document.createElement('h3');
    title.className = 'text-2xl font-bold text-green-800 mb-6 text-center';
    title.textContent = 'Nearby Pharmacies';
    
    const grid = document.createElement('div');
    grid.className = 'grid gap-4 md:grid-cols-2 lg:grid-cols-3';
    
    // Create pharmacy cards
    mockPharmacies.forEach(pharmacy => {
        const card = document.createElement('div');
        card.className = 'bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow';
        
        card.innerHTML = `
            <h4 class="font-semibold text-lg text-green-800 mb-2">${pharmacy.name}</h4>
            <p class="text-gray-600 mb-2">${pharmacy.address}</p>
            <p class="text-green-600 font-medium mb-2">📍 ${pharmacy.distance} away</p>
            <p class="text-gray-600 mb-2">📞 ${pharmacy.phone}</p>
            <p class="text-gray-600 mb-4">🕐 ${pharmacy.hours}</p>
            <div class="flex gap-2">
                <button class="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors" onclick="callPharmacy('${pharmacy.phone}')">
                    Call Now
                </button>
                <button class="flex-1 bg-green-100 text-green-700 py-2 px-4 rounded-md hover:bg-green-200 transition-colors" onclick="getDirections('${pharmacy.address}')">
                    Directions
                </button>
            </div>
        `;
        
        grid.appendChild(card);
    });
    
    resultsSection.appendChild(title);
    resultsSection.appendChild(grid);
    
    // Add results after the main content
    document.querySelector('main').after(resultsSection);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Call pharmacy function
function callPharmacy(phoneNumber) {
    window.location.href = `tel:${phoneNumber}`;
}

// Get directions function
function getDirections(address) {
    const encodedAddress = encodeURIComponent(address);
    window.open(`https://www.google.com/maps/search/${encodedAddress}`, '_blank');
}

// Add location detection functionality
locationInput.addEventListener('focus', function() {
    if (!this.value && navigator.geolocation) {
        const button = document.createElement('button');
        button.textContent = '📍 Use Current Location';
        button.className = 'text-sm text-green-600 hover:text-green-800 mt-1';
        button.onclick = function() {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    locationInput.value = "Current Location (Downtown, Springfield)";
                    button.remove();
                },
                (error) => {
                    alert('Unable to get your location. Please enter manually.');
                    button.remove();
                }
            );
        };
        
        if (!document.querySelector('button[onclick*="geolocation"]')) {
            this.parentElement.appendChild(button);
        }
    }
});
