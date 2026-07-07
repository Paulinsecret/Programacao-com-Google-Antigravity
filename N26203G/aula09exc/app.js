// Determine backend API URL (supports direct file:// opening and normal http:// running)
let apiOrigin = 'http://localhost:8000';
if (window.location && window.location.origin && window.location.origin.startsWith('http')) {
    apiOrigin = window.location.origin;
}
const API_URL = `${apiOrigin}/pets`;

// Global state
let petsList = [];

// Initialize Page
document.addEventListener("DOMContentLoaded", () => {
    generatePawDecorations();
    loadDashboardData();
    
    // Auto-fetch data on a slow interval for real-time offline updates
    setInterval(loadDashboardData, 8000);
});

/**
 * Helper to retrieve local pets from the browser's LocalStorage.
 */
function getLocalPets() {
    try {
        const data = localStorage.getItem("petfeliz_local_pets");
        return data ? JSON.parse(data) : [];
    } catch (e) {
        console.error("Erro ao ler do localStorage:", e);
        return [];
    }
}

/**
 * Helper to save a new pet to the browser's LocalStorage.
 */
function saveLocalPet(pet) {
    try {
        const pets = getLocalPets();
        // Generate a simple auto-increment ID for client-side sorting
        pet.id = pets.length > 0 ? Math.max(...pets.map(p => p.id)) + 1 : 1;
        pets.unshift(pet); // Add to the beginning of the list
        localStorage.setItem("petfeliz_local_pets", JSON.stringify(pets));
        return pet;
    } catch (e) {
        console.error("Erro ao gravar no localStorage:", e);
        return pet;
    }
}

/**
 * Updates the footer status indicator depending on whether the SQLite DB is online or not.
 */
function updateStatusIndicator(isOnline) {
    const dot  = document.getElementById("statusDot");
    const text = document.getElementById("footerStatusText");

    if (isOnline) {
        if (dot)  { dot.style.background = "var(--color-low)";    dot.style.boxShadow = "0 0 0 2px rgba(16,185,129,0.25)"; }
        if (text) text.textContent = "Sistema Local Conectado (Banco de Dados)";
    } else {
        if (dot)  { dot.style.background = "var(--color-medium)"; dot.style.boxShadow = "0 0 0 2px rgba(245,158,11,0.25)"; }
        if (text) text.textContent = "Modo Offline (Armazenamento do Navegador)";
    }
}

/**
 * Dynamically scatters cute paw prints falling slowly across the background.
 */
function generatePawDecorations() {
    const container = document.getElementById("pawDecorations");
    if (!container) return;
    
    const icons = ["🐾", "🐾", "🐾", "🐾"];
    const totalPaws = 20; // 20 scattered falling paws
    
    for (let i = 0; i < totalPaws; i++) {
        const paw = document.createElement("div");
        paw.className = "falling-paw";
        paw.textContent = icons[Math.floor(Math.random() * icons.length)];
        
        const left = Math.random() * 96; // 0% to 96%
        const size = 16 + Math.random() * 20; // 16px to 36px
        const duration = 18 + Math.random() * 16; // 18s to 34s (very slow falling!)
        const delay = Math.random() * -34; // Negative delay so they start at different phases immediately!
        const rotation = -45 + Math.random() * 90; // Subtle rotation swing
        const opacity = 0.02 + Math.random() * 0.03; // 0.02 to 0.05 transparent
        
        paw.style.left = `${left}%`;
        paw.style.setProperty("--sz", `${size}px`);
        paw.style.setProperty("--dur", `${duration}s`);
        paw.style.setProperty("--delay", `${delay}s`);
        paw.style.setProperty("--rot", `${rotation}deg`);
        paw.style.setProperty("--op", opacity);
        
        container.appendChild(paw);
    }
}

/**
 * Handles toggling active view between Tabs.
 * @param {string} tab - Either 'form' or 'dash'
 */
function switchTab(tab) {
    // Buttons
    const btnForm = document.getElementById("btnTabForm");
    const btnDash = document.getElementById("btnTabDash");
    
    // Content sections
    const tabForm = document.getElementById("tabForm");
    const tabDash = document.getElementById("tabDash");
    
    if (tab === 'form') {
        btnForm.classList.add("active");
        btnDash.classList.remove("active");
        tabForm.classList.add("active");
        tabDash.classList.remove("active");
    } else {
        btnForm.classList.remove("active");
        btnDash.classList.add("active");
        tabForm.classList.remove("active");
        tabDash.classList.add("active");
        // Reload dashboard whenever user switches to it
        loadDashboardData();
    }
}

/**
 * Submits the Pet Registration Form. Attempts a POST to SQLite, falls back to LocalStorage on block/offline.
 */
async function submitForm(event) {
    event.preventDefault();
    
    const form = document.getElementById("petForm");
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Disable submit button during transaction
    if (submitBtn) submitBtn.disabled = true;
    
    // Gather form values
    const name = document.getElementById("petName").value.trim();
    const species = document.getElementById("petSpecies").value;
    const breed = document.getElementById("petBreed").value.trim();
    const age = document.getElementById("petAge").value.trim();
    const owner = document.getElementById("petOwner").value.trim();
    
    // Extract selected severity radio
    const severityRadio = form.querySelector('input[name="severity"]:checked');
    const severity = severityRadio ? severityRadio.value : "baixa";
    
    // Checkbox hospitalized
    const is_hospitalized = document.getElementById("petHospitalized").checked;
    
    const petData = {
        name,
        species,
        breed,
        age,
        owner,
        severity,
        is_hospitalized
    };
    
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(petData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast("Sucesso!", `Pet '${name}' cadastrado com sucesso!`, "success");
            form.reset();
            await loadDashboardData();
        } else {
            throw new Error(result.error || "Erro retornado do servidor.");
        }
    } catch (error) {
        console.warn("Conexão direta falhou. Salvando no armazenamento local do navegador:", error);
        
        // Save to LocalStorage fallback
        saveLocalPet(petData);
        
        // Show successful toast, noting local storage fallback
        showToast("Sucesso (Local)", `Pet '${name}' cadastrado com sucesso localmente!`, "success");
        form.reset();
        
        // Update view using localStorage content
        petsList = getLocalPets();
        updateStatusIndicator(false);
        updateDashboardUI();
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
}

/**
 * Fetches pet list from SQLite backend, falls back to LocalStorage on connection failure.
 */
async function loadDashboardData() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error("Erro de resposta do servidor: " + response.status);
        }
        
        petsList = await response.json();
        
        // Sync local storage so it has updated copies if they go offline later
        localStorage.setItem("petfeliz_local_pets", JSON.stringify(petsList));
        
        updateStatusIndicator(true);
    } catch (error) {
        console.warn("Servidor SQLite inacessível. Usando armazenamento do navegador:", error.message);
        
        // Load fallback storage
        petsList = getLocalPets();
        updateStatusIndicator(false);
    }
    updateDashboardUI();
}

/**
 * Calculates numbers and updates elements in the DOM.
 */
function updateDashboardUI() {
    const totalCount = petsList.length;
    const hospitalizedList = petsList.filter(pet => pet.is_hospitalized);
    const hospitalizedCount = hospitalizedList.length;
    
    // 1. Update Numeric Highlights
    document.getElementById("statTotalCount").textContent = totalCount;
    document.getElementById("statHospitalizedCount").textContent = hospitalizedCount;
    
    const rate = totalCount > 0 ? Math.round((hospitalizedCount / totalCount) * 100) : 0;
    document.getElementById("statHospitalizationRate").textContent = `${rate}%`;
    
    // 2. Severity Progress Bars
    let lowCount = 0;
    let medCount = 0;
    let highCount = 0;
    
    petsList.forEach(pet => {
        if (!pet.severity) return;
        const s = pet.severity.toLowerCase();
        if (s === "baixa") lowCount++;
        else if (s === "média" || s === "media" || s === "médio" || s === "medio") medCount++;
        else if (s === "alta" || s === "crítica" || s === "critica") highCount++;
    });
    
    const lowPct = totalCount > 0 ? Math.round((lowCount / totalCount) * 100) : 0;
    const medPct = totalCount > 0 ? Math.round((medCount / totalCount) * 100) : 0;
    const highPct = totalCount > 0 ? Math.round((highCount / totalCount) * 100) : 0;
    
    // Update Text Labels
    document.getElementById("severityLowText").textContent = `${lowCount} pets (${lowPct}%)`;
    document.getElementById("severityMediumText").textContent = `${medCount} pets (${medPct}%)`;
    document.getElementById("severityHighText").textContent = `${highCount} pets (${highPct}%)`;
    
    // Update Progress Widths
    document.getElementById("severityLowBar").style.width = `${lowPct}%`;
    document.getElementById("severityMediumBar").style.width = `${medPct}%`;
    document.getElementById("severityHighBar").style.width = `${highPct}%`;
    
    // 3. Top Breeds Frequency List
    const breedFrequencies = {};
    petsList.forEach(pet => {
        if (!pet.breed) return;
        const breed = pet.breed.trim();
        if (breed) {
            breedFrequencies[breed] = (breedFrequencies[breed] || 0) + 1;
        }
    });
    
    const topBreeds = Object.entries(breedFrequencies)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
        
    const breedListEl = document.getElementById("topBreedsList");
    if (topBreeds.length === 0) {
        breedListEl.innerHTML = `<li class="empty-list-msg">Nenhuma raça registrada.</li>`;
    } else {
        breedListEl.innerHTML = topBreeds.map(([breed, count]) => {
            return `<li><span>🐩 ${breed}</span> <span class="list-count">${count}</span></li>`;
        }).join("");
    }
    
    // 4. Species Counts
    const speciesEmojis = {
        "cães": "🐶 Cães",
        "gatos": "🐱 Gatos",
        "aves": "🐦 Aves",
        "roedores": "🐹 Roedores",
        "répteis": "🦎 Répteis",
        "outros": "🐾 Outros"
    };
    
    const speciesFrequencies = {};
    petsList.forEach(pet => {
        if (!pet.species) return;
        const sp = pet.species.toLowerCase();
        speciesFrequencies[sp] = (speciesFrequencies[sp] || 0) + 1;
    });
    
    const speciesListEl = document.getElementById("speciesCountList");
    const speciesEntries = Object.entries(speciesFrequencies).sort((a,b) => b[1] - a[1]);
    
    if (speciesEntries.length === 0) {
        speciesListEl.innerHTML = `<li class="empty-list-msg">Nenhuma espécie registrada.</li>`;
    } else {
        speciesListEl.innerHTML = speciesEntries.map(([species, count]) => {
            const displayName = speciesEmojis[species] || `🐾 ${species.toUpperCase()}`;
            return `<li><span>${displayName}</span> <span class="list-count">${count}</span></li>`;
        }).join("");
    }
    
    // 5. Render Pets Data Table
    const tableBody = document.getElementById("petsTableBody");
    if (petsList.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="7" class="empty-table-msg">Ainda não há pets cadastrados.</td></tr>`;
    } else {
        tableBody.innerHTML = petsList.map(pet => {
            const speciesText = speciesEmojis[pet.species] ? speciesEmojis[pet.species].split(" ")[0] : "🐾";
            
            // Format state severity badges
            let badgeClass = "badge-low";
            let severityLabel = pet.severity || "Baixa";
            if (pet.severity) {
                const s = pet.severity.toLowerCase();
                if (s === "média" || s === "media") {
                    badgeClass = "badge-medium";
                    severityLabel = "Média";
                } else if (s === "alta") {
                    badgeClass = "badge-high";
                    severityLabel = "Alta";
                }
            }
            
            // Hospitalization Badge
            const hospBadge = pet.is_hospitalized 
                ? '<span class="badge badge-hosp">Sim 🏥</span>' 
                : '<span class="badge badge-home">Não 🏠</span>';
                
            return `
                <tr>
                    <td><strong>${escapeHtml(pet.name)}</strong></td>
                    <td>${speciesText} ${escapeHtml(pet.species)}</td>
                    <td>${escapeHtml(pet.breed)}</td>
                    <td>${escapeHtml(pet.age)}</td>
                    <td>${escapeHtml(pet.owner)}</td>
                    <td><span class="badge ${badgeClass}">${severityLabel}</span></td>
                    <td>${hospBadge}</td>
                </tr>
            `;
        }).join("");
    }
}

/**
 * Escapes user-inputted strings to prevent XSS issues in browser table output.
 */
function escapeHtml(str) {
    if (!str) return "";
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * Creates and displays toast messages to the user.
 */
function showToast(title, message, type = "success") {
    const container = document.getElementById("toastContainer");
    if (!container) return;
    
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    
    const icon = type === "success" ? "✓" : "⚠";
    
    toast.innerHTML = `
        <div class="toast-icon">${icon}</div>
        <div class="toast-content">
            <strong class="toast-title" style="display:block; font-size:13px; font-weight:700;">${title}</strong>
            <span class="toast-body">${message}</span>
        </div>
    `;
    
    container.appendChild(toast);
    
    // Trigger transition Reflow
    setTimeout(() => {
        toast.classList.add("show");
    }, 10);
    
    // Auto-remove toast after 4.5 seconds
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4500);
}
