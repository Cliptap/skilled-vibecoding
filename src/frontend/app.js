const API_BASE = 'http://127.0.0.1:8000/patients';

// Estado global temporal para el dropdown
let openDropdownId = null;

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    
    // Cerrar cualquier dropdown si se hace clic fuera
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown-container')) {
            closeAllDropdowns();
        }
    });
});

// ========================
// OPERACIONES BACKEND (API)
// ========================

async function loadDashboard() {
    fetchStats();
    fetchPatients();
}

async function fetchStats() {
    try {
        const timeFilter = document.getElementById('filter-time').value;
        const res = await fetch(`${API_BASE}/stats/kpis?time_filter=${timeFilter}`);
        if (!res.ok) throw new Error('Error cargando KPIs');
        const stats = await res.json();
        
        document.getElementById('kpi-total').innerText = stats.total;
        document.getElementById('kpi-fonasa').innerText = stats.fonasa;
        document.getElementById('kpi-isapre').innerText = stats.isapre;
    } catch (e) {
        console.error(e);
    }
}

async function fetchPatients() {
    try {
        const timeFilter = document.getElementById('filter-time').value;
        const sortFilter = document.getElementById('filter-sort').value;
        
        const res = await fetch(`${API_BASE}/?time_filter=${timeFilter}&sort=${sortFilter}`);
        if (!res.ok) throw new Error('Error al cargar tabla');
        const patients = await res.json();
        
        renderPatients(patients);
    } catch (error) {
        const tbody = document.getElementById('patients-table-body');
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                    <i data-lucide="alert-circle" class="w-8 h-8 mx-auto mb-2 text-red-400"></i>
                    <p>Error cargando la lista de pacientes.</p>
                </td>
            </tr>`;
        lucide.createIcons();
    }
}

async function fetchPatientByRut(rut) {
    try {
        const res = await fetch(`${API_BASE}/${rut}`);
        if (!res.ok) throw new Error('Paciente no encontrado');
        const patient = await res.json();
        renderPatients([patient]);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function submitForm() {
    const form = document.getElementById('patient-form');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const mode = document.getElementById('form-mode').value;
    const rut = document.getElementById('rut').value;
    
    const payload = {
        rut: rut,
        nombres: document.getElementById('nombres').value,
        apellidos: document.getElementById('apellidos').value,
        fecha_nacimiento: document.getElementById('fecha_nacimiento').value,
        sexo: document.getElementById('sexo').value,
        prevision: document.getElementById('prevision').value
    };

    const telefono = document.getElementById('telefono').value;
    const correo = document.getElementById('correo').value;
    if (telefono) payload.telefono = telefono;
    if (correo) payload.correo = correo;

    try {
        // Bloquear UI visual
        document.getElementById('btn-submit-text').innerText = 'Guardando...';
        
        const url = mode === 'create' ? `${API_BASE}/` : `${API_BASE}/${rut}`;
        const method = mode === 'create' ? 'POST' : 'PUT';
        
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        
        if (!res.ok) {
            throw new Error(data.detail || 'Error al guardar los datos');
        }

        showToast(`Paciente ${mode === 'create' ? 'registrado' : 'actualizado'} con éxito`, 'success');
        closeModal();
        loadDashboard(); // Refrescamos lista completa y KPIs en lugar de 1 solo
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        document.getElementById('btn-submit-text').innerText = 'Guardar';
    }
}

async function deletePatient(rut) {
    if (!confirm(`¿Está seguro que desea eliminar la ficha del paciente ${rut}? Esta acción no se puede deshacer.`)) {
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/${rut}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('Error al eliminar paciente');
        showToast('Ficha de paciente eliminada correctamente', 'success');
        loadDashboard(); // Recargar default view
    } catch (error) {
        showToast(error.message, 'error');
    }
}


// ========================
// RENDER UI & TABLAS
// ========================

function renderPatients(patients) {
    const tbody = document.getElementById('patients-table-body');
    tbody.innerHTML = '';

    if (patients.length === 0) {
        tbody.innerHTML = `
        <tr>
            <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                <i data-lucide="users" class="w-8 h-8 mx-auto mb-2 text-gray-400"></i>
                <p>No se encontraron registros para los filtros seleccionados.</p>
            </td>
        </tr>`;
        lucide.createIcons();
        return;
    }

    patients.forEach(p => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-gray-50 transition";
        tr.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${p.rut}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                ${p.nombres} ${p.apellidos}<br>
                <span class="text-xs text-gray-500">${p.fecha_nacimiento} · Sexo: ${p.sexo}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${p.prevision === 'fonasa' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}">
                    ${p.prevision.toUpperCase()}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                ${p.telefono || '-'}<br>
                <span class="text-xs text-gray-500">${p.correo || '-'}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium relative dropdown-container">
                <!-- Botón Tres Puntos -->
                <button onclick="toggleDropdown('${p.rut}')" class="text-gray-400 hover:text-gray-600 focus:outline-none p-1 rounded-md hover:bg-gray-200 transition">
                    <i data-lucide="more-vertical" class="w-5 h-5"></i>
                </button>
                
                <!-- Menú Desplegable -->
                <div id="dropdown-${p.rut}" class="hidden absolute right-8 top-8 w-32 bg-white border border-gray-200 rounded-md shadow-lg z-10 overflow-hidden">
                    <button onclick="editPatient('${encodeURIComponent(JSON.stringify(p))}')" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2">
                        <i data-lucide="pencil" class="w-4 h-4"></i>
                        <span>Editar</span>
                    </button>
                    <button onclick="deletePatient('${p.rut}')" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2">
                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                        <span>Borrar</span>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
    lucide.createIcons();
}

// ========================
// CONTROLADORES DE ESTADO UI
// ========================

function toggleDropdown(rut) {
    const dropdown = document.getElementById(`dropdown-${rut}`);
    
    // Si hay uno abierto y es distinto a este, lo cerramos
    if (openDropdownId && openDropdownId !== rut) {
        document.getElementById(`dropdown-${openDropdownId}`).classList.add('hidden');
    }

    if (dropdown.classList.contains('hidden')) {
        dropdown.classList.remove('hidden');
        openDropdownId = rut;
    } else {
        dropdown.classList.add('hidden');
        openDropdownId = null;
    }
}

function closeAllDropdowns() {
    if (openDropdownId) {
        const dropdown = document.getElementById(`dropdown-${openDropdownId}`);
        if(dropdown) dropdown.classList.add('hidden');
        openDropdownId = null;
    }
}

function openModal(mode = 'create', data = null) {
    closeAllDropdowns();
    document.getElementById('patient-modal').classList.remove('hidden');
    document.getElementById('form-mode').value = mode;
    
    const rutInput = document.getElementById('rut');

    if (mode === 'create') {
        document.getElementById('modal-title').innerText = 'Registrar Paciente';
        document.getElementById('patient-form').reset();
        rutInput.readOnly = false;
        rutInput.classList.remove('bg-gray-100');
    } else if (data) {
        document.getElementById('modal-title').innerText = 'Editar Paciente';
        rutInput.value = data.rut;
        rutInput.readOnly = true; // El RUT es identificador único, no debe editarse según la logica básica
        rutInput.classList.add('bg-gray-100');
        
        document.getElementById('nombres').value = data.nombres;
        document.getElementById('apellidos').value = data.apellidos;
        document.getElementById('fecha_nacimiento').value = data.fecha_nacimiento;
        document.getElementById('sexo').value = data.sexo;
        document.getElementById('prevision').value = data.prevision;
        document.getElementById('telefono').value = data.telefono || '';
        document.getElementById('correo').value = data.correo || '';
    }
}

function closeModal() {
    document.getElementById('patient-modal').classList.add('hidden');
}

function editPatient(patientJsonBase64) {
    const patient = JSON.parse(decodeURIComponent(patientJsonBase64));
    openModal('update', patient);
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    const bgColor = type === 'success' ? 'bg-green-50 border-green-200 text-green-800' : 'bg-red-50 border-red-200 text-red-800';
    const icon = type === 'success' ? '<i data-lucide="check-circle" class="w-5 h-5 text-green-500"></i>' : '<i data-lucide="alert-circle" class="w-5 h-5 text-red-500"></i>';

    toast.className = `flex items-center space-x-3 p-4 border rounded-md shadow-sm transform transition-all duration-300 translate-y-0 opacity-100 ${bgColor}`;
    toast.innerHTML = `
        ${icon}
        <span class="text-sm font-medium">${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-auto text-gray-400 hover:text-gray-600 focus:outline-none">
            <i data-lucide="x" class="w-4 h-4"></i>
        </button>
    `;

    container.appendChild(toast);
    lucide.createIcons();

    // Auto eliminar luego de 5 segundos
    setTimeout(() => {
        toast.classList.replace('opacity-100', 'opacity-0');
        toast.classList.replace('translate-y-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}
