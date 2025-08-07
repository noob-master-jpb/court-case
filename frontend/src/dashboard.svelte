<script>
  import { onMount } from 'svelte';
  

    export let case_data = {};
    export let view_dashboard;
    export let back;
let loading = false;
let pdfLoading = false;

    async function downloadPDF() {
        pdfLoading = true;
        try {
            const response = await fetch('/download_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: case_data ? JSON.stringify(case_data) : '{}',
            });

            if (!response.ok) {
                throw new Error('Failed to generate PDF');
            }

            // Get the filename from the response headers or generate one
            const contentDisposition = response.headers.get('content-disposition');
            let filename = 'case_report.pdf';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="(.+)"/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }

            // Create blob and download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            
            console.log('PDF downloaded successfully');
        } catch (error) {
            console.error('Error downloading PDF:', error);
            alert('Failed to download PDF. Please try again.');
        } finally {
            pdfLoading = false;
        }
    }


</script>

<div class="dashboard">
    <div class="dashboard-header">
        <h1>Case Dashboard</h1>
        <div class="header-actions">
            <button class="btn-secondary" on:click={back}>← Back to Search</button>
            <button class="btn-primary" on:click={downloadPDF} disabled={pdfLoading}>
                {pdfLoading ? 'Generating...' : 'Export PDF'}
            </button>
        </div>
    </div>

    <div id="case_info">
        <div id="case_details" class="info-card">
            <div class="card-header">
                <h3>Case Information</h3>
                <div class="status-badge status-pending">Pending</div>
            </div>
            <div class="details-grid">
                <div class="detail-item">
                    <span class="label">Case Number:</span>
                    <span class="value">{case_data.case_number}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Case Type:</span>
                    <span class="value">{case_data.case_type}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Year:</span>
                    <span class="value">{case_data.case_year}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Status:</span>
                    <span class="value status-text">{case_data.status}</span>
                </div>
            </div>
        </div>

        <div id="case_parties" class="info-card">
            <div class="card-header">
                <h3>Parties</h3>
            </div>
            <div class="parties-container">
                <div class="party">
                    <div class="party-label">Petitioner</div>
                    <div class="party-name">{case_data.petitioner}</div>
                </div>
                <div class="vs-divider">VS.</div>
                <div class="party">
                    <div class="party-label">Respondent</div>
                    <div class="party-name">{case_data.respondent}</div>
                </div>
            </div>
        </div>

        <div id="case_dates" class="info-card">
            <div class="card-header">
                <h3>Important Dates</h3>
            </div>
            <div class="dates-container">
                <div class="date-item">
                    <div class="date-icon">📅</div>
                    <div class="date-content">
                        <span class="date-label">Filing Date</span>
                        <span class="date-value">{case_data.filing_date}</span>
                    </div>
                </div>
                <div class="date-item next-hearing">
                    <div class="date-icon">⏰</div>
                    <div class="date-content">
                        <span class="date-label">Next Hearing</span>
                        <span class="date-value">
                            {#if case_data.next_date === null}
                                <span class="date-placeholder">No next hearing scheduled</span>
                            {:else}
                                {case_data.next_date}
                            {/if}
                        </span>
                    </div>
                </div>
                <div class="date-item">
                    <div class="date-icon">📋</div>
                    <div class="date-content">
                        <span class="date-label">Last Hearing</span>
                        <span class="date-value">{case_data.last_date}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="case_orders" class="info-card orders-section">
        <div class="card-header">
            <h3>Orders & Documents</h3>
        </div>
        <div class="orders-container">
            {#each (case_data.orders || []) as order, index}
                <div class="order-item">
                    <div class="order-number">#{index + 1}</div>
                    <div class="order-info">
                        <div class="order-date">
                            <b>{order.date}</b>
                        </div>
                    </div>
                    <div class="order-actions">
                        <button class="download-btn" on:click={async () => {
                            try {
                                const response = await fetch(order.link);
                                const blob = await response.blob();
                                const url = window.URL.createObjectURL(blob);
                                const link = document.createElement('a');
                                link.href = url;
                                link.download = `Court_Order_${index + 1}_${order.date}.pdf`;
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                                window.URL.revokeObjectURL(url);
                            } catch (error) {
                                console.error('Download failed:', error);
                                // Fallback to opening in new tab
                                window.open(order.link, '_blank');
                            }
                        }}>
                            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                            </svg>
                            Download
                        </button>
                    </div>
                </div>
            {/each}
        </div>
    </div>
    <div id="footer">
        <p>Under MIT License</p>
    </div>
</div>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  :root {
    --primary-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    --secondary-gradient: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
    --accent-color: #fbbf24;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #94a3b8;
    --border-light: #374151;
    --border-dark: #4b5563;
    --bg-primary: #1f2937;
    --bg-secondary: #111827;
    --bg-card: rgba(31, 41, 55, 0.9);
    --shadow-light: 0 4px 6px rgba(0, 0, 0, 0.3);
    --shadow-medium: 0 10px 25px rgba(0, 0, 0, 0.4);
    --shadow-heavy: 0 20px 40px rgba(0, 0, 0, 0.5);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .dashboard {
    scroll-behavior: smooth;
    min-height: 95vh;
    padding: 2rem;
    background: var(--primary-gradient);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    position: relative;
    overflow-x: hidden;
    
  }

  .dashboard::before {
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

  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    position: relative;
    z-index: 1;
  }

  .dashboard-header h1 {
    font-size: 3rem;
    font-weight: 800;
    color: var(--text-primary);
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    margin: 0;
  }

  .header-actions {
    display: flex;
    gap: 1rem;
  }

  .btn-primary, .btn-secondary {
    padding: 0.75rem 1.5rem;
    border-radius: 12px;
    font-weight: 600;
    transition: var(--transition);
    border: none;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .btn-primary {
    background: var(--secondary-gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
  }

  .btn-secondary {
    background: var(--bg-primary);
    color: var(--text-primary);
    border: 1px solid var(--border-light);
  }

  .btn-secondary:hover {
    background: var(--bg-secondary);
    border-color: var(--border-dark);
  }

  #case_info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
    position: relative;
    z-index: 1;
  }

  .info-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: var(--shadow-medium);
    transition: var(--transition);
  }
  .parties-container {

    display: flex;
    flex-direction: column;
  }
  .parties-container div{
    width: 100%;
    text-align: center;
  }
  .info-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-heavy);
    border-color: var(--border-dark);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-light);
  }

  .card-header h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
  }

  .status-badge {
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .status-pending {
    background: var(--warning-color);
    color: var(--bg-primary);
  }

  .details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .detail-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
  }

  .value {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .status-text {
    color: var(--warning-color);
  }

  /* Parties Section */
  .parties-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }

  .party {
    flex: 1;
    text-align: center;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-light);
  }

  .party-label {

    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  .party-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .vs-divider {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--accent-color);
    padding: 0.5rem;
  }

  /* Dates Section */
  .dates-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .date-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-light);
    transition: var(--transition);
  }

  .date-item:hover {
    border-color: var(--border-dark);
    background: var(--bg-primary);
  }

  .date-item.next-hearing {
    border-color: var(--accent-color);
    box-shadow: 0 0 20px rgba(251, 191, 36, 0.2);
  }

  .date-icon {
    font-size: 1.5rem;
    width: 2rem;
    text-align: center;
  }

  .date-content {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .date-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
  }

  .date-value {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .date-placeholder {
    color: var(--text-muted);
    font-style: italic;
  }

  /* Orders Section */
  .orders-section {
    grid-column: 1 / -1;
  }

  .orders-count {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
  }



  .orders-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .order-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--bg-secondary);
    border-radius: 16px;
    border: 1px solid var(--border-light);
    transition: var(--transition);
  }

  .order-item:hover {
    border-color: var(--border-dark);
    background: var(--bg-primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
  }

  .order-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    background: var(--secondary-gradient);
    color: white;
    font-weight: 700;
    border-radius: 50%;
    font-size: 0.9rem;
  }

  .order-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }


  .order-date {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }

  .order-actions {
    display: flex;
    gap: 0.75rem;
  }

  .download-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.85rem;
    transition: var(--transition);
    text-decoration: none;
    border: none;
    cursor: pointer;
    background: var(--secondary-gradient);
    color: white;
    box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
  }

  .download-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .dashboard {
      padding: 1rem;
    }

    .dashboard-header {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .dashboard-header h1 {
      font-size: 2rem;
    }

    #case_info {
      grid-template-columns: 1fr;
    }

    .parties-container {
      flex-direction: column;
    }

    .vs-divider {
      transform: rotate(90deg);
      margin: 0.5rem 0;
    }

    .order-item {
      flex-direction: column;
      gap: 1rem;
    }

    .order-actions {
      width: 100%;
      justify-content: center;
    }

    .download-btn {
      flex: 1;
      justify-content: center;
    }

    
    #footer {
      width: 100%;
      text-align: center;
      font-size: 1rem;
      padding: 1rem;
      margin-top: 2rem;
    }
  }

  #footer {
    width: 100%;
    text-align: center;
    font-size: 1rem;
    padding: 1rem;
    margin-top: 2rem;
    color: var(--text-secondary);
  }

  #footer p {
    margin: 0;
  }
</style>
