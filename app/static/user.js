console.log("JavaScript file is loaded!");

// Medication data
const medications = [
    'Acetaminophen', 'Ibuprofen', 'Aspirin', 'Amoxicillin', 'Lisinopril',
    'Metformin', 'Atorvastatin', 'Omeprazole', 'Losartan', 'Gabapentin',
    'Sertraline', 'Tramadol', 'Trazodone', 'Fluoxetine', 'Hydrochlorothiazide'
];

// Get DOM elements from your HTML
document.addEventListener('DOMContentLoaded', function() {
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
        
        // Change button text while "processing"
        const originalText = findButton.textContent;
        findButton.textContent = 'Searching...';
        findButton.disabled = true;
        
        // Simulate processing time
        setTimeout(() => {
            findButton.textContent = originalText;
            findButton.disabled = false;
            
            // Show success message - this is where you'd redirect to pharmacy results
            alert(`Searching for ${medication} near ${location}. This would redirect to pharmacy results page.`);
            
            // You can replace the alert above with actual redirection:
            // window.location.href = '/pharmacy-results.html';
            // or call another function to display results
        }, 1500);
    });

    // Optional: Add Enter key support for inputs
    medicationInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            findButton.click();
        }
    });

    locationInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            findButton.click();
        }
    });
});
