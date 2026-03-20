let currentItem = null;

async function openCustomizationModal(itemId) {
    try {
        const response = await fetch(`/api/menu_item/${itemId}`);
        if (!response.ok) throw new Error("Item not found");
        
        const item = await response.json();
        currentItem = item;
        
        document.getElementById('modalItemId').value = item.id;
        document.getElementById('modalItemName').innerText = item.name;
        document.getElementById('modalItemDesc').innerText = item.description;
        document.getElementById('itemQuantity').value = 1;
        
        const container = document.getElementById('customizationsContainer');
        container.innerHTML = '';
        
        item.customizations.forEach(group => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'mb-4';
            
            const groupHeader = document.createElement('h5');
            groupHeader.className = 'fw-bold mb-3 mt-4 text-dark border-bottom pb-2';
            groupHeader.innerHTML = `${group.name} <span class="badge ${group.type === 'multiple' ? 'bg-secondary' : 'bg-primary'} ms-2 rounded-pill fw-medium" style="font-size: 0.7rem;">${group.type === 'multiple' ? 'Choose Multiple' : 'Choose One'}</span>`;
            groupDiv.appendChild(groupHeader);
            
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'row g-3';
            
            group.options.forEach((opt, idx) => {
                const optCol = document.createElement('div');
                optCol.className = 'col-md-6';
                
                const inputType = group.type === 'single' ? 'radio' : 'checkbox';
                const inputName = group.type === 'single' ? `group_${group.id}` : `option_${opt.id}`;
                const inputId = `opt_${opt.id}`;
                const isChecked = group.type === 'single' && idx === 0 ? 'checked' : '';
                
                optCol.innerHTML = `
                    <input type="${inputType}" class="btn-check custom-option-input" name="${inputName}" id="${inputId}" value="${opt.id}" data-price="${opt.price_change}" onchange="updateTotalPrice()" ${isChecked}>
                    <label class="btn btn-outline-light w-100 text-start text-dark shadow-sm custom-option-container p-3 d-flex justify-content-between align-items-center" for="${inputId}">
                        <div>
                            <span class="fs-5 me-2">${opt.icon || ''}</span>
                            <span class="fw-medium">${opt.name}</span>
                        </div>
                        <span class="text-success fw-bold ms-2">${opt.price_change > 0 ? '+₹' + opt.price_change.toFixed(2) : ''}</span>
                    </label>
                `;
                optionsDiv.appendChild(optCol);
            });
            
            groupDiv.appendChild(optionsDiv);
            container.appendChild(groupDiv);
        });
        
        updateTotalPrice();
        
        const modal = new bootstrap.Modal(document.getElementById('customizationModal'));
        modal.show();
        
    } catch (error) {
        console.error('Error fetching item details:', error);
        alert('Could not load customizations. Please try again.');
    }
}

function updateQuantity(change) {
    const input = document.getElementById('itemQuantity');
    let val = parseInt(input.value) || 1;
    val += change;
    if (val < 1) val = 1;
    input.value = val;
    updateTotalPrice();
}

function updateTotalPrice() {
    if (!currentItem) return;
    
    let total = currentItem.base_price;
    const quantity = parseInt(document.getElementById('itemQuantity').value) || 1;
    
    const inputs = document.querySelectorAll('.custom-option-input:checked');
    inputs.forEach(input => {
        total += parseFloat(input.dataset.price);
    });
    
    total = total * quantity;
    document.getElementById('modalTotalPrice').innerText = total.toFixed(2);
}

async function addToCart() {
    if (!currentItem) return;
    
    const quantity = parseInt(document.getElementById('itemQuantity').value) || 1;
    const selectedOptions = [];
    
    document.querySelectorAll('.custom-option-input:checked').forEach(input => {
        selectedOptions.push(input.value);
    });
    
    const data = {
        item_id: currentItem.id,
        quantity: quantity,
        options: selectedOptions
    };
    
    try {
        const response = await fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Update cart badge visually
            const badges = document.querySelectorAll('.cart-count');
            badges.forEach(badge => {
                badge.innerText = result.cart_count;
                badge.style.display = 'inline-block';
                
                // Add pop animation class
                badge.classList.remove('pop');
                void badge.offsetWidth; // trigger reflow
                badge.classList.add('pop');
            });
            
            // Hide modal
            const modalEl = document.getElementById('customizationModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
            
        } else {
            const errResult = await response.json();
            alert(errResult.message || 'Failed to add to cart. Please try again.');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        alert('Could not connect to server.');
    }
}
