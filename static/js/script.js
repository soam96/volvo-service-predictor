document.addEventListener('DOMContentLoaded', function() {
    console.log('Volvo Service Predictor loaded');
    
    // Initialize all components
    initializeTaskSelection();
    initializeFormSubmission();
    prefillSampleData();
});

function initializeTaskSelection() {
    const taskCheckboxes = document.querySelectorAll('input[name="tasks"]');
    const selectedTasksSummary = document.getElementById('selectedTasksSummary');
    const tasksList = document.getElementById('tasksList');
    const selectedTasksCount = document.getElementById('selectedTasksCount');
    const totalTime = document.getElementById('totalTime');

    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedTasks);
    });

    function updateSelectedTasks() {
        const selectedTasks = Array.from(taskCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => ({
                value: checkbox.value,
                name: checkbox.parentElement.querySelector('strong').textContent,
                time: parseFloat(checkbox.dataset.time)
            }));

        // Update summary display
        if (selectedTasks.length > 0) {
            selectedTasksSummary.style.display = 'block';
            selectedTasksCount.textContent = `${selectedTasks.length} task${selectedTasks.length > 1 ? 's' : ''}`;
            
            // Update tasks list
            tasksList.innerHTML = '';
            let totalHours = 0;
            
            selectedTasks.forEach(task => {
                totalHours += task.time;
                const taskItem = document.createElement('div');
                taskItem.className = 'task-item';
                taskItem.innerHTML = `
                    <span class="task-name">${task.name}</span>
                    <span class="task-duration">${task.time}h</span>
                `;
                tasksList.appendChild(taskItem);
            });

            // Update total time
            totalTime.textContent = `Estimated time: ${totalHours.toFixed(1)} hours`;
        } else {
            selectedTasksSummary.style.display = 'none';
        }
    }

    // Pre-select some common tasks for demo
    setTimeout(() => {
        document.querySelector('input[value="oil_change"]').checked = true;
        document.querySelector('input[value="air_filter"]').checked = true;
        updateSelectedTasks();
    }, 500);
}

function initializeFormSubmission() {
    const form = document.getElementById('serviceForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultCard = document.getElementById('resultCard');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const lastServiceDateInput = document.getElementById('last_service_date');
    const calculatedDaysDiv = document.getElementById('calculatedDays');
    const daysSinceLastServiceSpan = document.getElementById('daysSinceLastService');

    // Set max date to today for last service date
    const today = new Date().toISOString().split('T')[0];
    lastServiceDateInput.max = today;

    // Calculate days since last service
    function calculateDaysSinceLastService() {
        const lastServiceDate = lastServiceDateInput.value;
        
        if (!lastServiceDate) {
            calculatedDaysDiv.style.display = 'none';
            return null;
        }

        const lastService = new Date(lastServiceDate);
        const today = new Date();
        const timeDiff = today.getTime() - lastService.getTime();
        const daysDiff = Math.floor(timeDiff / (1000 * 3600 * 24));

        // Update the display
        daysSinceLastServiceSpan.textContent = daysDiff;
        calculatedDaysDiv.style.display = 'block';
        calculatedDaysDiv.classList.add('show');
        
        // Add warning classes based on days
        calculatedDaysDiv.className = 'calculated-days show';
        if (daysDiff > 365) {
            calculatedDaysDiv.classList.add('alert');
        } else if (daysDiff > 180) {
            calculatedDaysDiv.classList.add('warning');
        }

        return daysDiff;
    }

    // Event listener for last service date changes
    lastServiceDateInput.addEventListener('change', calculateDaysSinceLastService);
    lastServiceDateInput.addEventListener('input', calculateDaysSinceLastService);

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Form submitted');
        
        // Validate form
        if (!validateForm()) {
            return;
        }

        // Calculate days since last service
        const daysSinceLastService = calculateDaysSinceLastService();
        if (daysSinceLastService === null) {
            showError('Please select the last service date');
            return;
        }

        // Show loading state
        showLoading(true);

        try {
            const formData = getFormData();
            // Add calculated days to form data
            formData.last_service_days = daysSinceLastService;

            console.log('Sending data to server:', formData);

            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Received response from server:', data);

            if (data.success) {
                // Add delay to show loading animation
                setTimeout(() => {
                    displayResults(data);
                    showLoading(false);
                }, 1500);
            } else {
                showError(data.error || 'Prediction failed');
                showLoading(false);
            }
        } catch (error) {
            console.error('Network error:', error);
            showError('Network error: Unable to connect to server. Please check if the server is running.');
            showLoading(false);
        }
    });

    function getFormData() {
        const selectedTasks = Array.from(document.querySelectorAll('input[name="tasks"]:checked'))
            .map(checkbox => checkbox.value);
        
        const formData = {
            car_number_plate: document.getElementById('car_number_plate').value.trim().toUpperCase(),
            car_model: document.getElementById('car_model').value,
            manufacture_year: parseInt(document.getElementById('manufacture_year').value),
            fuel_type: document.getElementById('fuel_type').value,
            service_type: document.getElementById('service_type').value,
            total_kilometers: parseInt(document.getElementById('total_kilometers').value),
            km_since_last_service: parseInt(document.getElementById('km_since_last_service').value),
            selected_tasks: selectedTasks,
            number_of_tasks: selectedTasks.length
        };
        
        console.log('Form data prepared:', formData);
        return formData;
    }

    function validateForm() {
        const numberPlate = document.getElementById('car_number_plate').value;
        const numberPlatePattern = /^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{1,4}$/i;
        
        if (!numberPlatePattern.test(numberPlate)) {
            showError('Invalid car number plate format. Please use format like MH12AB1234');
            return false;
        }

        // Check last service date is provided
        if (!lastServiceDateInput.value) {
            showError('Please select the last service date');
            lastServiceDateInput.focus();
            return false;
        }

        // Check all required fields are filled
        const requiredFields = form.querySelectorAll('[required]');
        for (let field of requiredFields) {
            if (!field.value.trim()) {
                showError(`Please fill in all required fields`);
                field.focus();
                return false;
            }
        }

        // Validate at least one task is selected
        const selectedTasks = document.querySelectorAll('input[name="tasks"]:checked');
        if (selectedTasks.length === 0) {
            showError('Please select at least one service task');
            return false;
        }

        // Validate numeric ranges
        const manufactureYear = parseInt(document.getElementById('manufacture_year').value);
        if (manufactureYear < 2000 || manufactureYear > 2024) {
            showError('Manufacture year must be between 2000 and 2024');
            return false;
        }

        const totalKms = parseInt(document.getElementById('total_kilometers').value);
        if (totalKms < 0) {
            showError('Total kilometers cannot be negative');
            return false;
        }

        const kmSinceService = parseInt(document.getElementById('km_since_last_service').value);
        if (kmSinceService < 0) {
            showError('KM since last service cannot be negative');
            return false;
        }

        return true;
    }

    function displayResults(data) {
        console.log('Displaying results:', data);
        
        const workloadClass = `workload-${data.workload_level.toLowerCase()}`;
        const partsStatus = data.parts_availability;
        
        let partsClass = 'parts-out-of-stock';
        let partsIcon = '<i class="fas fa-times-circle"></i>';
        let partsText = 'Not Available';
        let partsDetails = partsStatus;

        if (partsStatus.includes('All parts available') && partsStatus.includes('low stock')) {
            partsClass = 'parts-limited';
            partsIcon = '<i class="fas fa-exclamation-circle"></i>';
            partsText = 'Limited Stock';
        } else if (partsStatus === 'All parts available') {
            partsClass = 'parts-available';
            partsIcon = '<i class="fas fa-check-circle"></i>';
            partsText = 'Available';
        } else if (partsStatus.includes('Some parts out of stock')) {
            partsClass = 'parts-out-of-stock';
            partsIcon = '<i class="fas fa-exclamation-triangle"></i>';
            partsText = 'Partial Stock';
        } else if (partsStatus.includes('All parts out of stock')) {
            partsClass = 'parts-out-of-stock';
            partsIcon = '<i class="fas fa-times-circle"></i>';
            partsText = 'Out of Stock';
        } else if (partsStatus === 'Model not found') {
            partsClass = 'parts-out-of-stock';
            partsIcon = '<i class="fas fa-question-circle"></i>';
            partsText = 'Model Not Found';
        }

        resultCard.innerHTML = `
            <div class="fade-in" style="width: 100%;">
                <div class="service-info">
                    <h3><i class="fas fa-car"></i> ${data.car_model}</h3>
                    <div class="service-id">Service ID: ${data.service_id}</div>
                    <div class="service-id">Number Plate: ${data.car_number_plate}</div>
                    <div class="service-id">Days Since Last Service: ${data.last_service_days} days</div>
                </div>
                <div class="metrics-grid">
                    <div class="metric service-time">
                        <div class="metric-label">
                            <i class="fas fa-clock"></i> Predicted Service Time
                        </div>
                        <div class="metric-value" id="serviceTimeValue">0.0</div>
                        <div class="metric-details">Estimated completion time</div>
                    </div>
                    <div class="metric workload">
                        <div class="metric-label">
                            <i class="fas fa-chart-bar"></i> Workload Level
                        </div>
                        <div class="metric-value ${workloadClass}" id="workloadValue">${data.workload_level}</div>
                        <div class="metric-details">${data.workload_percentage}% capacity</div>
                    </div>
                    <div class="metric queue">
                        <div class="metric-label">
                            <i class="fas fa-list-ol"></i> Queue Position
                        </div>
                        <div class="metric-value" id="queueValue">0</div>
                        <div class="metric-details">Cars ahead in queue</div>
                    </div>
                    <div class="metric parts">
                        <div class="metric-label">
                            <i class="fas fa-cogs"></i> Parts Availability
                        </div>
                        <div class="metric-value ${partsClass}" id="partsValue">
                            ${partsIcon} ${partsText}
                        </div>
                        <div class="metric-details">
                            ${partsDetails}
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Animate the numbers
        animateValue('serviceTimeValue', 0, data.predicted_service_time, 2000);
        animateValue('queueValue', 0, data.queue_position, 1500);

        // Show results section with animation
        resultsSection.style.display = 'block';
        resultsSection.classList.add('fade-in');
        
        // Add scroll animation to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    function animateValue(id, start, end, duration) {
        const obj = document.getElementById(id);
        if (!obj) {
            console.error(`Element with id ${id} not found`);
            return;
        }
        
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = progress * (end - start) + start;
            
            if (id === 'serviceTimeValue') {
                obj.textContent = value.toFixed(1);
            } else {
                obj.textContent = Math.floor(value);
            }
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    function showError(message) {
        // Remove existing errors
        const existingError = document.querySelector('.error-section');
        if (existingError) {
            existingError.remove();
        }

        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-section';
        errorDiv.innerHTML = `
            <div class="error-card">
                <i class="fas fa-exclamation-triangle"></i>
                ${message}
            </div>
        `;
        
        // Insert before form section
        form.parentNode.parentNode.insertBefore(errorDiv, form.parentNode);
        
        // Remove error after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    function showLoading(show) {
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        
        if (show) {
            btnText.style.display = 'none';
            btnLoader.style.display = 'flex';
            loadingOverlay.style.display = 'flex';
            submitBtn.disabled = true;
        } else {
            btnText.style.display = 'block';
            btnLoader.style.display = 'none';
            loadingOverlay.style.display = 'none';
            submitBtn.disabled = false;
        }
    }

    // Add input validation styling
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.style.borderColor = '#4caf50';
            } else {
                this.style.borderColor = '#ddd';
            }
        });
        
        // Special handling for number plate
        if (input.id === 'car_number_plate') {
            input.addEventListener('input', function(e) {
                this.value = this.value.toUpperCase();
            });
        }
    });
}

function prefillSampleData() {
    console.log('Prefilling sample data...');
    
    document.getElementById('car_number_plate').value = 'MH12AB1234';
    document.getElementById('car_model').value = 'XC60';
    document.getElementById('manufacture_year').value = '2020';
    document.getElementById('fuel_type').value = 'petrol';
    document.getElementById('service_type').value = 'general';
    
    // Set last service date to 100 days ago
    const hundredDaysAgo = new Date();
    hundredDaysAgo.setDate(hundredDaysAgo.getDate() - 100);
    const formattedDate = hundredDaysAgo.toISOString().split('T')[0];
    document.getElementById('last_service_date').value = formattedDate;
    
    document.getElementById('total_kilometers').value = '35000';
    document.getElementById('km_since_last_service').value = '5000';
    
    // Calculate days since last service
    const lastServiceDateInput = document.getElementById('last_service_date');
    const event = new Event('change');
    lastServiceDateInput.dispatchEvent(event);
}

console.log('Application initialized successfully');