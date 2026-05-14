<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const apiBase = 'http://localhost:8000/api/v1'
const token = ref(localStorage.getItem('token'))
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const toast = ref({ show: false, msg: '', type: 'success' })

const activeTab = ref('dashboard')
const patients = ref([])
const practitioners = ref([])
const appointments = ref([])

// Modals
const showModal = ref(false)
const modalType = ref('patient') // 'patient' | 'practitioner' | 'appointment'

const newPatient = ref({ identifier: '', name: '' })
const newPractitioner = ref({ identifier: '', name: '', specialty: '', telecom: '' })
const newAppointment = ref({ patient_id: '', practitioner_id: '', start_time: '', end_time: '', status: 'booked' })

// RUT formatting: auto-inserts hyphen before last char, allows only digits + K
const formatRut = (raw) => {
  // Strip everything except digits and K
  const clean = raw.replace(/[^0-9kK]/g, '').toUpperCase()
  if (clean.length <= 1) return clean
  return clean.slice(0, -1) + '-' + clean.slice(-1)
}
const handleRutInput = (e, model, field) => {
  model[field] = formatRut(e.target.value)
  // Keep cursor at end
  const input = e.target
  const len = input.value.length
  setTimeout(() => input.setSelectionRange(len, len), 0)
}

const showToast = (msg, type = 'success') => {
  toast.value = { show: true, msg, type }
  setTimeout(() => toast.value.show = false, 4000)
}

const openModal = (type) => {
  modalType.value = type
  showModal.value = true
}

// Auth
const login = async () => {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    params.append('username', username.value)
    params.append('password', password.value)
    const response = await axios.post('http://localhost:8000/token', params)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    showToast('Sesión iniciada correctamente')
    fetchData()
  } catch {
    showToast('Credenciales inválidas', 'error')
  } finally {
    isLoading.value = false
  }
}

const logout = () => {
  token.value = null
  localStorage.removeItem('token')
}

const authHeaders = () => ({ headers: { Authorization: `Bearer ${token.value}` } })

// Fetch all data
const fetchData = async () => {
  if (!token.value) return
  isLoading.value = true
  try {
    const [pRes, prRes, aRes] = await Promise.all([
      axios.get(`${apiBase}/patients/`, authHeaders()),
      axios.get(`${apiBase}/practitioners/`, authHeaders()),
      axios.get(`${apiBase}/appointments/`, authHeaders())
    ])
    patients.value = pRes.data
    practitioners.value = prRes.data
    appointments.value = aRes.data
  } catch (err) {
    if (err.response?.status === 401) logout()
    else showToast('Error sincronizando datos', 'error')
  } finally {
    isLoading.value = false
  }
}

// Create patient
const createPatient = async () => {
  if (!newPatient.value.name || !newPatient.value.identifier) {
    showToast('Nombre e Identificador requeridos', 'error'); return
  }
  isLoading.value = true
  try {
    await axios.post(`${apiBase}/patients/`, {
      id: `pat-${Date.now()}`,
      identifier: newPatient.value.identifier.trim(),
      name: newPatient.value.name.trim(),
      birth_date: null
    }, authHeaders())
    showToast('Paciente registrado')
    showModal.value = false
    newPatient.value = { identifier: '', name: '' }
    fetchData()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Error al registrar paciente', 'error')
  } finally { isLoading.value = false }
}

// Create practitioner
const createPractitioner = async () => {
  if (!newPractitioner.value.name || !newPractitioner.value.identifier) {
    showToast('Nombre e Identificador requeridos', 'error'); return
  }
  isLoading.value = true
  try {
    await axios.post(`${apiBase}/practitioners/`, {
      id: `prac-${Date.now()}`,
      identifier: newPractitioner.value.identifier.trim(),
      name: newPractitioner.value.name.trim(),
      specialty: newPractitioner.value.specialty || null,
      telecom: newPractitioner.value.telecom || null
    }, authHeaders())
    showToast('Profesional registrado')
    showModal.value = false
    newPractitioner.value = { identifier: '', name: '', specialty: '', telecom: '' }
    fetchData()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Error al registrar profesional', 'error')
  } finally { isLoading.value = false }
}

// Create appointment
const createAppointment = async () => {
  if (!newAppointment.value.patient_id || !newAppointment.value.practitioner_id || !newAppointment.value.start_time || !newAppointment.value.end_time) {
    showToast('Todos los campos son requeridos', 'error'); return
  }
  isLoading.value = true
  try {
    await axios.post(`${apiBase}/appointments/`, {
      id: `apt-${Date.now()}`,
      status: newAppointment.value.status,
      start_time: new Date(newAppointment.value.start_time).toISOString(),
      end_time: new Date(newAppointment.value.end_time).toISOString(),
      patient_id: newAppointment.value.patient_id,
      practitioner_id: newAppointment.value.practitioner_id
    }, authHeaders())
    showToast('Cita registrada')
    showModal.value = false
    newAppointment.value = { patient_id: '', practitioner_id: '', start_time: '', end_time: '', status: 'booked' }
    fetchData()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Error al registrar cita', 'error')
  } finally { isLoading.value = false }
}

// Delete patient (soft)
const deleteRecord = async (id) => {
  if (!confirm('¿Eliminar registro?')) return
  const endpoint = activeTab.value === 'patients' ? 'patients' : activeTab.value === 'practitioners' ? 'practitioners' : 'appointments'
  try {
    await axios.delete(`${apiBase}/${endpoint}/${id}/`, authHeaders())
    showToast('Registro eliminado')
    fetchData()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Error al eliminar', 'error')
  }
}

onMounted(() => { if (token.value) fetchData() })
</script>

<template>
  <div class="min-h-screen bg-background text-on-background font-body-md overflow-hidden selection:bg-surface-variant selection:text-on-surface flex flex-col">
    
    <!-- Login Screen -->
    <div v-if="!token" class="flex-1 flex items-center justify-center p-6 bg-surface-container-lowest">
      <div class="w-full max-w-[400px] glass-card p-8 rounded-xl shadow-sm">
        <div class="flex flex-col items-center mb-8">
          <div class="w-12 h-12 bg-primary-container rounded-lg flex items-center justify-center mb-4 text-on-primary">
            <span class="material-symbols-outlined text-[28px]">clinical_notes</span>
          </div>
          <h1 class="font-headline-lg text-headline-lg text-on-surface">Clinical Central</h1>
          <p class="font-label-caps text-label-caps text-on-surface-variant mt-2">Health Systems v2.4</p>
        </div>
          
        <div class="space-y-4">
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Correo electrónico</label>
            <input v-model="username" placeholder="admin@clinic.com" class="w-full bg-surface-container-lowest border border-outline-variant p-3 rounded-lg focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all placeholder:text-outline text-body-md" />
          </div>
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Contraseña</label>
            <input v-model="password" type="password" placeholder="••••••••" class="w-full bg-surface-container-lowest border border-outline-variant p-3 rounded-lg focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all placeholder:text-outline text-body-md" />
          </div>
          <button @click="login" :disabled="isLoading" class="w-full bg-primary text-on-primary hover:opacity-90 p-3 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 mt-2 shadow-md disabled:opacity-70 text-body-md">
            <span v-if="isLoading" class="material-symbols-outlined animate-spin text-[20px]">refresh</span>
            <span v-else>Iniciar Sesión</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Dashboard Shell -->
    <div v-else class="flex flex-1 overflow-hidden">
      <!-- SideNavBar Shell -->
      <aside class="w-[280px] bg-surface-container-lowest border-r border-outline-variant/50 shadow-sm flex flex-col py-8 px-4 z-50 shrink-0">
        <div class="mb-10 px-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-primary-container flex items-center justify-center text-on-primary">
              <span class="material-symbols-outlined text-[24px]">clinical_notes</span>
            </div>
            <div>
              <h1 class="font-headline-md text-[20px] font-bold text-on-surface leading-tight">Clinical Central</h1>
              <p class="font-label-caps text-[10px] text-on-surface-variant/70 tracking-widest">Health Systems v2.4</p>
            </div>
          </div>
        </div>
        
        <nav class="flex-1 space-y-1">
          <a @click.prevent="activeTab = 'dashboard'" href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors duration-200" :class="activeTab === 'dashboard' ? 'text-primary font-semibold border-r-4 border-primary bg-surface-container-low' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'">
            <span class="material-symbols-outlined">dashboard</span>
            <span class="font-label-caps text-label-caps">Panel General</span>
          </a>
          <a @click.prevent="activeTab = 'patients'" href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors duration-200" :class="activeTab === 'patients' ? 'text-primary font-semibold border-r-4 border-primary bg-surface-container-low' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'">
            <span class="material-symbols-outlined">patient_list</span>
            <span class="font-label-caps text-label-caps">Registros de Pacientes</span>
          </a>
          <a @click.prevent="activeTab = 'practitioners'" href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors duration-200" :class="activeTab === 'practitioners' ? 'text-primary font-semibold border-r-4 border-primary bg-surface-container-low' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'">
            <span class="material-symbols-outlined">stethoscope</span>
            <span class="font-label-caps text-label-caps">Personal Médico</span>
          </a>
          <a @click.prevent="activeTab = 'appointments'" href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors duration-200" :class="activeTab === 'appointments' ? 'text-primary font-semibold border-r-4 border-primary bg-surface-container-low' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'">
            <span class="material-symbols-outlined">calendar_today</span>
            <span class="font-label-caps text-label-caps">Citas Clínicas</span>
          </a>
          <a @click.prevent="activeTab = 'compliance'" href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors duration-200" :class="activeTab === 'compliance' ? 'text-primary font-semibold border-r-4 border-primary bg-surface-container-low' : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-high'">
            <span class="material-symbols-outlined">gavel</span>
            <span class="font-label-caps text-label-caps">Compliance & Audits</span>
          </a>
        </nav>
        
        <div class="mt-auto space-y-6">
          <button @click="openModal(activeTab === 'practitioners' ? 'practitioner' : activeTab === 'appointments' ? 'appointment' : 'patient')" class="w-full py-3 bg-primary text-on-primary rounded-lg font-semibold flex items-center justify-center gap-2 shadow-lg shadow-primary/10 hover:opacity-90 transition-opacity">
            <span class="material-symbols-outlined">add</span>
            <span class="font-label-caps text-label-caps">Nuevo Registro</span>
          </button>
          
          <div class="pt-6 border-t border-outline-variant/30 space-y-1">
            <a class="flex items-center gap-3 px-4 py-2 rounded-lg text-error hover:bg-error-container/50 transition-colors cursor-pointer" @click.prevent="logout">
              <span class="material-symbols-outlined">logout</span>
              <span class="font-label-caps text-label-caps">Cerrar Sesión</span>
            </a>
          </div>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="flex-1 flex flex-col min-w-0 bg-background overflow-hidden relative">
        <!-- TopAppBar Shell -->
        <header class="flex justify-between items-center h-16 px-gutter w-full bg-surface-container-lowest/80 backdrop-blur-xl border-b border-outline-variant/30 sticky top-0 z-40 shrink-0">
          <div class="flex items-center gap-6">
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-on-surface-variant">search</span>
              <input class="bg-surface-container-low border-none rounded-full py-2 pl-10 pr-4 w-80 text-body-md focus:ring-2 focus:ring-primary outline-none transition-shadow" placeholder="Buscar pacientes o sistemas..." type="text"/>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <button @click="fetchData" class="w-10 h-10 rounded-full hover:bg-surface-variant/50 flex items-center justify-center text-on-surface transition-all" title="Actualizar datos">
              <span class="material-symbols-outlined" :class="{ 'animate-spin': isLoading }">sync</span>
            </button>
            <button class="w-10 h-10 rounded-full hover:bg-surface-variant/50 flex items-center justify-center text-on-surface transition-all">
              <span class="material-symbols-outlined">notifications</span>
            </button>
            <div class="h-8 w-[1px] bg-outline-variant/30"></div>
            <div class="flex items-center gap-3">
              <div class="text-right hidden lg:block">
                <p class="text-body-sm font-semibold leading-tight">Admin System</p>
                <p class="text-[10px] text-on-tertiary-container uppercase tracking-widest">Director Médico</p>
              </div>
              <div class="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center font-bold text-on-surface border border-outline-variant">A</div>
            </div>
          </div>
        </header>

        <!-- Dynamic Content Canvas -->
        <div class="p-gutter flex-1 overflow-y-auto space-y-gutter">
          
          <div class="flex justify-between items-end mb-6">
            <div>
              <h2 class="font-headline-lg text-[28px] text-on-surface font-bold">
                {{ activeTab === 'dashboard' ? 'Panel de Gobernanza' : activeTab === 'patients' ? 'Registros de Pacientes' : activeTab === 'practitioners' ? 'Personal Médico' : activeTab === 'appointments' ? 'Citas Clínicas' : 'Cumplimiento y Auditorías' }}
              </h2>
              <p class="text-on-surface-variant font-body-md mt-1">Monitoreo del sistema y registro de accesos.</p>
            </div>
            <div class="flex gap-3">
              <button @click="fetchData" class="flex items-center gap-2 px-4 py-2 border border-outline rounded-lg text-body-sm font-semibold hover:bg-surface-container-high transition-colors">
                <span class="material-symbols-outlined text-[18px]">download</span>
                Exportar Datos
              </button>
            </div>
          </div>

          <!-- Dashboard specific widgets (Only shown when activeTab === dashboard) -->
          <div v-if="activeTab === 'dashboard' || activeTab === 'compliance'" class="grid grid-cols-1 md:grid-cols-3 gap-gutter mb-6">
            <!-- Active Sessions -->
            <div class="glass-card p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start mb-4">
                <div class="w-12 h-12 rounded-xl bg-primary-fixed flex items-center justify-center text-primary">
                  <span class="material-symbols-outlined">person_pin</span>
                </div>
                <span class="flex items-center text-[12px] font-bold text-secondary">
                  <span class="material-symbols-outlined text-[16px] mr-1">trending_up</span> +2
                </span>
              </div>
              <p class="text-on-tertiary-container font-label-caps text-label-caps">Sesiones Activas</p>
              <h3 class="font-headline-lg text-headline-lg mt-1">14</h3>
            </div>
            
            <!-- FHIR Sync Status -->
            <div class="glass-card p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start mb-4">
                <div class="w-12 h-12 rounded-xl bg-secondary-fixed flex items-center justify-center text-secondary">
                  <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">sync_alt</span>
                </div>
                <div class="px-2 py-1 bg-secondary-fixed/30 rounded text-[10px] font-bold text-secondary border border-secondary-fixed">HEALTHY</div>
              </div>
              <p class="text-on-tertiary-container font-label-caps text-label-caps">FHIR Sync Status</p>
              <div class="flex items-baseline gap-2 mt-1">
                <h3 class="font-headline-lg text-headline-lg">Stable</h3>
                <span class="text-body-md text-secondary font-semibold">/ 99.9%</span>
              </div>
              <div class="mt-4 h-1.5 w-full bg-surface-container rounded-full overflow-hidden">
                <div class="h-full bg-secondary-container w-[99.9%]"></div>
              </div>
            </div>

            <!-- Recent Access Logs -->
            <div class="glass-card p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start mb-4">
                <div class="w-12 h-12 rounded-xl bg-surface-container flex items-center justify-center text-on-surface">
                  <span class="material-symbols-outlined">security_update_good</span>
                </div>
                <button class="material-symbols-outlined text-on-surface-variant">more_horiz</button>
              </div>
              <p class="text-on-tertiary-container font-label-caps text-label-caps">Registros de Acceso Recientes</p>
              <h3 class="font-headline-lg text-headline-lg mt-1">1,240 <span class="text-body-md font-normal text-on-tertiary-container">hoy</span></h3>
            </div>
          </div>

          <!-- Data Table Section -->
          <section v-if="activeTab !== 'dashboard' && activeTab !== 'compliance'" class="bg-surface-container-lowest rounded-xl border border-outline-variant/30 overflow-hidden shadow-sm">
            <div class="px-6 py-5 border-b border-outline-variant/30 flex justify-between items-center">
              <div>
                <h4 class="font-headline-sm text-headline-sm text-on-surface">Registros del Sistema</h4>
                <p class="text-body-sm text-on-surface-variant">Historial de interacción con registros electrónicos de salud en tiempo real.</p>
              </div>
              <div class="flex gap-2">
                <div class="flex items-center bg-surface-container-low border border-outline-variant/50 rounded-lg px-3 py-1.5">
                  <span class="material-symbols-outlined text-[18px] mr-2 text-on-surface-variant">filter_list</span>
                  <span class="text-body-sm font-medium">Filtrar</span>
                </div>
              </div>
            </div>
            
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-surface-container-low/50 border-b border-outline-variant/30">
                    <th v-if="activeTab === 'patients'" class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider">ID Paciente</th>
                    <th v-if="activeTab === 'patients'" class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider">Nombre Completo</th>
                    <th v-if="activeTab === 'patients'" class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider">Identificador (RUT)</th>
                    
                    <th v-if="activeTab === 'practitioners'" class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider">Profesional</th>
                    <th v-if="activeTab === 'practitioners'" class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider">Especialidad</th>
                    
                    <th v-if="activeTab === 'appointments'" class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider">Referencia Paciente</th>
                    <th v-if="activeTab === 'appointments'" class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider">Estado</th>
                    
                    <th class="px-6 py-4 font-label-caps text-[11px] font-bold text-on-tertiary-container uppercase tracking-wider text-right">Acción</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-outline-variant/30">
                  <tr v-for="item in (activeTab === 'patients' ? patients : activeTab === 'practitioners' ? practitioners : appointments)" :key="item.id" class="hover:bg-surface-container-low transition-colors group">
                    
                    <!-- Patients -->
                    <td v-if="activeTab === 'patients'" class="px-6 py-4">
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded bg-surface-container-high flex items-center justify-center text-on-surface-variant">
                          <span class="material-symbols-outlined text-[16px]">fingerprint</span>
                        </div>
                        <span class="font-data-mono text-[13px] font-medium">{{ item.id }}</span>
                      </div>
                    </td>
                    <td v-if="activeTab === 'patients'" class="px-6 py-4">
                      <div class="flex items-center gap-2">
                        <div class="w-6 h-6 rounded-full bg-secondary-fixed flex items-center justify-center text-[10px] font-bold">{{ item.name ? item.name.charAt(0) : '?' }}</div>
                        <span class="text-body-md font-medium text-on-surface">{{ item.name }}</span>
                      </div>
                    </td>
                    <td v-if="activeTab === 'patients'" class="px-6 py-4 text-body-sm text-on-surface-variant font-data-mono">{{ item.identifier }}</td>
                    
                    <!-- Practitioners -->
                    <td v-if="activeTab === 'practitioners'" class="px-6 py-4">
                      <div class="flex items-center gap-2">
                        <div class="w-6 h-6 rounded-full bg-primary-fixed flex items-center justify-center text-[10px] font-bold">{{ item.name ? item.name.charAt(0) : '?' }}</div>
                        <span class="text-body-md font-medium text-on-surface">{{ item.name }}</span>
                      </div>
                    </td>
                    <td v-if="activeTab === 'practitioners'" class="px-6 py-4 text-body-sm text-on-surface-variant">{{ item.specialty || 'General' }}</td>
                    
                    <!-- Appointments -->
                    <td v-if="activeTab === 'appointments'" class="px-6 py-4 font-data-mono text-[13px] font-medium">{{ item.patient_id }}</td>
                    <td v-if="activeTab === 'appointments'" class="px-6 py-4">
                      <span v-if="item.status === 'booked'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-surface-variant text-on-surface border border-outline-variant/30 uppercase tracking-wider">Booked</span>
                      <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-secondary-fixed/20 text-secondary border border-secondary-fixed/30 uppercase tracking-wider">{{ item.status }}</span>
                    </td>

                    <!-- Actions -->
                    <td class="px-6 py-4 text-right">
                      <div class="flex items-center justify-end">
                        <button @click="deleteRecord(item.id)" class="material-symbols-outlined text-on-tertiary-container hover:text-error transition-colors text-[20px]" title="Eliminar">delete</button>
                      </div>
                    </td>
                  </tr>
                  
                  <tr v-if="!isLoading && ((activeTab === 'patients' && patients.length === 0) || (activeTab === 'practitioners' && practitioners.length === 0) || (activeTab === 'appointments' && appointments.length === 0))">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <span class="material-symbols-outlined text-[48px] text-outline-variant mb-4">folder_open</span>
                        <h3 class="text-[16px] font-medium text-on-surface">Sin registros encontrados</h3>
                        <p class="text-sm text-on-surface-variant mt-1">No hay datos en esta sección aún.</p>
                        <button @click="openModal(activeTab === 'practitioners' ? 'practitioner' : activeTab === 'appointments' ? 'appointment' : 'patient')" class="mt-4 text-sm text-secondary font-semibold hover:underline">Crear primer registro</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="px-6 py-4 border-t border-outline-variant/30 flex justify-between items-center bg-surface-container-low/30">
              <span class="text-body-sm text-on-surface-variant">Mostrando registros</span>
              <div class="flex gap-2">
                <button class="p-1.5 rounded border border-outline-variant bg-surface-container-lowest hover:bg-surface-container-low disabled:opacity-30" disabled>
                  <span class="material-symbols-outlined text-[18px]">chevron_left</span>
                </button>
                <button class="p-1.5 rounded border border-outline-variant bg-surface-container-lowest hover:bg-surface-container-low">
                  <span class="material-symbols-outlined text-[18px]">chevron_right</span>
                </button>
              </div>
            </div>
          </section>

          <!-- Governance specific detail grid -->
          <div v-if="activeTab === 'dashboard' || activeTab === 'compliance'" class="grid grid-cols-1 lg:grid-cols-2 gap-gutter mt-6">
            <div class="bg-surface-container-lowest p-6 rounded-xl border border-outline-variant/30">
              <div class="flex justify-between items-center mb-6">
                <h4 class="font-headline-sm text-headline-sm text-on-surface">Integridad de Datos</h4>
                <span class="material-symbols-outlined text-on-tertiary-container">info</span>
              </div>
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <span class="text-body-md">Estado de Validación</span>
                  <span class="text-body-md font-bold text-secondary">Verificado</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-body-md">Cumplimiento de Esquema</span>
                  <span class="text-body-md font-bold text-secondary">100% (HL7 FHIR v4)</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-body-md">Nivel de Cifrado</span>
                  <span class="text-body-md font-bold">AES-256-GCM</span>
                </div>
              </div>
            </div>
            <div class="bg-primary-container p-6 rounded-xl border border-outline-variant/30 text-on-primary">
              <div class="flex items-center gap-3 mb-6">
                <span class="material-symbols-outlined text-primary-fixed">admin_panel_settings</span>
                <h4 class="font-headline-sm text-headline-sm">Aviso de Seguridad</h4>
              </div>
              <p class="text-on-primary-container text-body-md mb-6 leading-relaxed">
                  Revisión periódica de gobernanza programada para mañana a las 09:00 AM. Asegúrese de que todos los registros de acceso marcados estén anotados y archivados antes del cierre del ciclo actual.
              </p>
              <button @click="activeTab = 'patients'" class="mt-6 w-full py-2 bg-primary-fixed text-primary font-bold rounded-lg hover:bg-white transition-colors">
                  Ver Registros de Pacientes
              </button>
            </div>
          </div>

        </div>
      </main>
    </div>

    <!-- Modals -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-primary-container/40 backdrop-blur-sm">
      <div class="bg-surface-container-lowest rounded-xl shadow-xl border border-outline-variant/30 w-full max-w-md overflow-hidden">
        <div class="px-6 py-5 border-b border-outline-variant/30 flex justify-between items-center bg-surface-container-low">
          <h3 class="text-[18px] font-semibold text-on-surface">
            {{ modalType === 'practitioner' ? 'Nuevo Profesional' : modalType === 'appointment' ? 'Nueva Cita' : 'Nuevo Paciente' }}
          </h3>
          <button @click="showModal = false" class="text-on-surface-variant hover:text-on-surface transition-colors material-symbols-outlined">close</button>
        </div>

        <!-- Patient form -->
        <div v-if="modalType === 'patient'" class="p-6 space-y-4">
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Nombre Completo</label>
            <input v-model="newPatient.name" placeholder="Ej: Juan Pérez" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary focus:ring-1 focus:ring-primary outline-none text-body-md" />
          </div>
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Identificador (RUT)</label>
            <input
              :value="newPatient.identifier"
              @input="handleRutInput($event, newPatient, 'identifier')"
              placeholder="12345678-9"
              maxlength="10"
              class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary focus:ring-1 focus:ring-primary outline-none text-body-md font-mono" />
            <p v-if="newPatient.identifier && newPatient.identifier.length < 9" class="text-[11px] text-error mt-1">RUT incompleto (mínimo 7 dígitos + dígito verificador)</p>
          </div>
        </div>

        <!-- Practitioner form -->
        <div v-if="modalType === 'practitioner'" class="p-6 space-y-4">
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Nombre Completo</label>
            <input v-model="newPractitioner.name" placeholder="Ej: Dra. María González" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md" />
          </div>
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Identificador (RUT)</label>
            <input
              :value="newPractitioner.identifier"
              @input="handleRutInput($event, newPractitioner, 'identifier')"
              placeholder="12345678-9"
              maxlength="10"
              class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md font-mono" />
            <p v-if="newPractitioner.identifier && newPractitioner.identifier.length < 9" class="text-[11px] text-error mt-1">RUT incompleto (mínimo 7 dígitos + dígito verificador)</p>
          </div>
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Especialidad</label>
            <input v-model="newPractitioner.specialty" placeholder="Medicina General" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md" />
          </div>
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Contacto (telecom)</label>
            <input v-model="newPractitioner.telecom" placeholder="+56 9 1234 5678" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md" />
          </div>
        </div>

        <!-- Appointment form -->
        <div v-if="modalType === 'appointment'" class="p-6 space-y-4">
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">ID Paciente</label>
            <select v-model="newAppointment.patient_id" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md">
              <option value="" disabled>Seleccionar paciente...</option>
              <option v-for="p in patients" :key="p.id" :value="p.id">{{ p.name }} ({{ p.identifier }})</option>
            </select>
          </div>
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">ID Profesional</label>
            <select v-model="newAppointment.practitioner_id" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md">
              <option value="" disabled>Seleccionar profesional...</option>
              <option v-for="pr in practitioners" :key="pr.id" :value="pr.id">{{ pr.name }} – {{ pr.specialty || 'General' }}</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Inicio</label>
              <input v-model="newAppointment.start_time" type="datetime-local" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md" />
            </div>
            <div>
              <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Fin</label>
              <input v-model="newAppointment.end_time" type="datetime-local" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md" />
            </div>
          </div>
          <div>
            <label class="block font-label-caps text-label-caps text-on-surface-variant mb-1">Estado</label>
            <select v-model="newAppointment.status" class="w-full bg-surface border border-outline-variant p-3 rounded-lg focus:border-primary outline-none text-body-md">
              <option value="booked">Booked</option>
              <option value="pending">Pending</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-outline-variant/30 bg-surface-container-low flex gap-3 justify-end">
          <button @click="showModal = false" class="px-4 py-2 bg-surface-container-lowest border border-outline-variant rounded-lg text-body-sm font-semibold text-on-surface-variant hover:bg-surface transition-colors">Cancelar</button>
          <button
            @click="modalType === 'practitioner' ? createPractitioner() : modalType === 'appointment' ? createAppointment() : createPatient()"
            :disabled="isLoading"
            class="px-4 py-2 bg-primary rounded-lg text-body-sm font-semibold text-on-primary hover:opacity-90 transition-opacity flex items-center gap-2 shadow-sm disabled:opacity-70">
            <span v-if="isLoading" class="material-symbols-outlined animate-spin text-[18px]">refresh</span>
            <span v-else>Guardar Registro</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast.show" class="fixed bottom-6 right-6 flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg border border-outline-variant/30 z-50" :class="toast.type === 'error' ? 'bg-error-container text-error' : 'bg-surface-container-highest text-on-surface'">
        <span class="material-symbols-outlined text-[20px]">{{ toast.type === 'error' ? 'error' : 'check_circle' }}</span>
        <span class="text-body-sm font-semibold">{{ toast.msg }}</span>
      </div>
    </Transition>

  </div>
</template>

<style>
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateY(1rem); }
.toast-leave-to { opacity: 0; transform: translateY(1rem); }
</style>
