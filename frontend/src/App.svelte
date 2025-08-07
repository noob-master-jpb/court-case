<script>
    
    import { onMount } from 'svelte';
    import Dashboard from "./dashboard.svelte";


  let view_dashboard = false;
  function back() {
    view_dashboard = !view_dashboard;
  }
  let ctype = '';
  let clist = [];
  let isSubmitting = false;
  let lastSubmitTime = 0;
  const SUBMIT_DEBOUNCE_TIME = 1000;
  let case_data = {
    case_type: '',
    case_number: '',
    case_year: '',
    status: '',
    filing_date: '',
    next_date: '',
    last_date: '',
    petitioner: '',
    respondent: '',
    orders: []
  }

  async function load_list() {
    const response = await fetch('/type_list');
    if (response.ok) {
      clist = await response.json();
    } else {
      console.error('Failed to load case types');
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    
    const currentTime = Date.now();
    if (isSubmitting || (currentTime - lastSubmitTime < SUBMIT_DEBOUNCE_TIME)) {
      
      return;
    }
    if (!/^\d+$/.test(case_data.case_number.trim())) {
      alert('Case number must contain only numbers.');
      return;
    }

    const currentYear = new Date().getFullYear();
    const caseYear = parseInt(case_data.case_year.trim());

    if (!/^\d+$/.test(case_data.case_year.trim())) {
      alert('Case year must contain only numbers.');
      return;
    }

    if (isNaN(caseYear) || caseYear > currentYear) {
      alert(`Case year cannot be greater than ${currentYear}.`);
      return;
    }
    if (!case_data.case_type || !case_data.case_number || !case_data.case_year) {
      alert('Please fill in all required fields.');
      return;
    }
    if (case_data.case_type === '0') {
      alert('Please select a valid case type.');must
      return;
    }
    
    isSubmitting = true;
    lastSubmitTime = currentTime;
    
    console.log('Form submitted:', case_data);
    fetch('/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(case_data)
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {        throw new Error('Network response was not ok');
      }
    })
    .then(data => {
      console.log('Success:', data);
      case_data = { ...case_data, ...data };
      view_dashboard = true;
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while submitting the form. Please try again.');
    })
    .finally(() => {
      isSubmitting = false;
    });
  }


onMount(() => {
    load_list();
  });


</script>
{#if view_dashboard}
  <Dashboard {case_data} {view_dashboard} {back}/>
{/if}
<div class="main">
  <div class="top">
  DELHI HIGH COURT
  </div>
  <div class="content">
    <form id="form_data" on:submit={handleSubmit}>
      <div class="case_details">
        <div>

          <label for="case_type">Case Type:</label>
            <select type="text" id="case_type" name="case_type" bind:value={case_data.case_type} required>
              <option value="0" selected="true"> Select</option>
            {#each clist as item}
              <option value={item}>{item}</option>
            {/each}
            </select>
        </div>
                  
        <div>
          <label for="case_number">Case Number:</label>
          <input type="text" id="case_number" name="case_number" bind:value={case_data.case_number} required>
        </div>

        <div>
          <label for="case_year">Case Year:</label>
          <input type="text" id="case_year" name="case_year" bind:value={case_data.case_year} required>
        </div>
      </div>
      <div class=submit>
        <button type="submit" disabled={isSubmitting}>
          {#if isSubmitting}
            Submitting...
          {:else}
            Submit
          {/if}
        </button>
      </div>

    </form>
  </div>
</div>


<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
  --primary-gradient: linear-gradient(135deg, #0f172a 0%, #102342 50%, #000000 100%);
  --secondary-gradient: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  --accent-color: #11f4f4;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --border-light: #374151;
  --border-dark: #4b5563;
  --bg-primary: #1f2937;
  --bg-secondary: #111827;
  --shadow-light: 0 4px 6px rgba(0, 0, 0, 0.3);
  --shadow-medium: 0 10px 25px rgba(0, 0, 0, 0.4);
  --shadow-heavy: 0 20px 40px rgba(0, 0, 0, 0.5);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.main {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--primary-gradient);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  position: relative;
  overflow-x: hidden;
}

.main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(251, 191, 36, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.top {
  flex: 0 0 auto;
  padding: 3rem 2rem;
  font-size: clamp(2.5rem, 6vw, 4rem);
  color: white;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  font-weight: 800;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  letter-spacing: 2px;
  position: relative;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.top::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-color) 0%, #3b82f6 50%, var(--accent-color) 100%);
}

.content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 2rem;
  position: relative;
  z-index: 1;
}
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shimmer {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: -200% 0; }
}

.case_details {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
  align-items: end;
}

.case_details div {
  display: flex;
  flex-direction: column;
  position: relative;
}

.case_details label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.case_details label::before {
  content: '';
  width: 4px;
  height: 4px;
  background: var(--accent-color);
  border-radius: 50%;
  display: inline-block;
}

.case_details input,
.case_details select {
  padding: 1.25rem 1.5rem;
  border: 2px solid var(--border-light);
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 500;
  transition: var(--transition);
  background: var(--bg-primary);
  color: var(--text-primary);
  position: relative;
  box-shadow: var(--shadow-light);
}

.case_details input:focus,
.case_details select:focus {
  outline: none;
  border-color: #3b82f6;
  background: var(--bg-secondary);
  box-shadow: 
    0 0 0 4px rgba(59, 130, 246, 0.2),
    0 8px 25px rgba(59, 130, 246, 0.25);
  transform: translateY(-2px);
}

.case_details input::placeholder {
  color: var(--text-secondary);
  font-weight: 400;
}

.case_details select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23cbd5e1' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 1.5rem center;
  background-repeat: no-repeat;
  background-size: 1.25rem;
  padding-right: 4rem;
}

.case_details select:hover {
  border-color: #3b82f6;
  box-shadow: var(--shadow-medium);
}

.submit {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  gap: 1rem;
}

.submit button {
  padding: 1.25rem 3.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  background: var(--secondary-gradient);
  color: white;
  border: none;
  border-radius: 50px;
  transition: var(--transition);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  box-shadow: 
    0 12px 24px rgba(102, 126, 234, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.submit button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.submit button:hover::before {
  left: 100%;
}

.submit button:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 20px 40px rgba(59, 130, 246, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
}

.submit button:active {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 16px rgba(59, 130, 246, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.submit button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  background: #6b7280;
}

.submit button:disabled:hover {
  transform: none;
  box-shadow: 
    0 12px 24px rgba(102, 126, 234, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Enhanced Responsive Design */
@media (max-width: 1024px) {
  #form {
    padding: 3rem 2.5rem;
  }
  
  .case_details {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

@media (max-width: 768px) {
  .top {
    padding: 2rem 1.5rem;
  }
  
  .content {
    padding: 2rem 1rem;
  }
  
  #form {
    margin: 0;
    padding: 2.5rem 1.5rem;
    border-radius: 24px;
  }
  
  .case_details {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .submit button {
    padding: 1rem 2.5rem;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .top {
    padding: 1.5rem 1rem;
  }
  
  #form {
    padding: 2rem 1rem;
    border-radius: 20px;
  }
  
  .case_details input,
  .case_details select {
    padding: 1rem;
    font-size: 0.95rem;
  }
  
  .submit button {
    padding: 1rem 2rem;
    width: 100%;
    max-width: 300px;
  }
}

/* Loading states and interactions */
.case_details select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--bg-secondary);
}

.case_details select option {
  padding: 0.75rem;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-weight: 500;
}

.case_details select option:hover {
  background: var(--bg-secondary);
}

/* Form validation styles */
.case_details input:invalid:not(:placeholder-shown) {
  border-color: #003c3f;
  box-shadow: 0 0 0 3px rgba(0, 48, 76, 0.2);
}

.case_details input:valid:not(:placeholder-shown) {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

/* Enhanced accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  .submit button::before {
    display: none;
  }
}

/* Focus styles for accessibility */
.case_details input:focus-visible,
.case_details select:focus-visible,
.submit button:focus-visible {
  outline: 2px solid var(--accent-color);
  outline-offset: 2px;
}

/* Print styles */
@media print {
  .main {
    background: white !important;
  }

  .top {
    background: #333 !important;
    color: white !important;
  }
  
  #form {
    box-shadow: none !important;
    border: 2px solid #333 !important;
  }
}

</style>