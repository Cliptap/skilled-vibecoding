<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const apiBase = 'http://localhost:8000/api/v1'
const token = ref(localStorage.getItem('token'))
const currentUser = ref(null)
const selectedRole = ref(null)
const credentialEmail = ref('')
const password = ref('')
const isLoading = ref(false)
const toast = ref({ show: false, msg: '', type: 'success' })

const activeTab = ref('inicio')
const patients = ref([])
const practitioners = ref([])
const appointments = ref([])
const users = ref([])

const showModal = ref(false)
const modalType = ref('patient')
const searchQuery = ref('')

const newPatient = ref({ identifier: '', name: '' })
const newPractitioner = ref({ identifier: '', name: '', specialty: '', telecom: '' })
const newAppointment = ref({ patient_id: '', practitioner_id: '', start_time: '', end_time: '', status: 'agendada' })
const newUser = ref({ email: '', full_name: '', role: 'secretaria', password: '' })

const roles = [
  { id: 'admin', label: 'Administrador', email: 'admin@clinic.com', pwd: 'admin123', icon: 'admin_panel_settings', color: 'emerald', desc: 'Acceso total al sistema. Gestiona pacientes, profesionales, citas y usuarios.' },
  { id: 'medico', label: 'Médico', email: 'medico@clinic.com', pwd: 'admin123', icon: 'stethoscope', color: 'blue', desc: 'Ve sus citas del día, consulta fichas de pacientes y agenda nuevas consultas.' },
  { id: 'secretaria', label: 'Secretaria', email: 'secretaria@clinic.com', pwd: 'admin123', icon: 'person_add', color: 'violet', desc: 'Registra pacientes, agenda citas y gestiona la agenda diaria del consultorio.' }
]

const roleLabel = computed(() => {
  if (!currentUser.value) return ''
  const map = { admin: 'Administrador', medico: 'Médico', secretaria: 'Secretaria' }
  return map[currentUser.value.role] || ''
})
const canWritePatients = computed(() => currentUser.value?.scopes?.includes('patients:write') || currentUser.value?.scopes?.includes('admin:all'))
const canWriteAppointments = computed(() => currentUser.value?.scopes?.includes('appointments:write') || currentUser.value?.scopes?.includes('admin:all'))
const canWritePractitioners = computed(() => currentUser.value?.scopes?.includes('practitioners:write') || currentUser.value?.scopes?.includes('admin:all'))

const formatRut = (raw) => { const clean = raw.replace(/[^0-9kK]/g, '').toUpperCase(); if (clean.length <= 1) return clean; return clean.slice(0, -1) + '-' + clean.slice(-1) }
const handleRutInput = (e, model, field) => { model[field] = formatRut(e.target.value); const input = e.target; const len = input.value.length; setTimeout(() => input.setSelectionRange(len, len), 0) }
const showToast = (msg, type = 'success') => { toast.value = { show: true, msg, type }; setTimeout(() => toast.value.show = false, 4000) }
const decodeJwt = (t) => { try { return JSON.parse(atob(t.split('.')[1])) } catch { return null } }

const selectRole = (role) => { selectedRole.value = role.id; credentialEmail.value = role.email; password.value = role.pwd }

const login = async () => {
  if (!credentialEmail.value || !password.value) { showToast('Selecciona un rol e ingresa la contraseña', 'error'); return }
  isLoading.value = true
  try {
    const params = new URLSearchParams(); params.append('username', credentialEmail.value); params.append('password', password.value)
    const response = await axios.post('http://localhost:8000/token', params)
    token.value = response.data.access_token; localStorage.setItem('token', token.value)
    const payload = decodeJwt(token.value)
    if (payload) currentUser.value = { email: payload.sub, fullName: payload.full_name || payload.sub, role: payload.role || 'admin', scopes: payload.scopes || [] }
    showToast('Sesión iniciada'); fetchData(); if (payload.role === 'admin') fetchUsers()
  } catch { showToast('Credenciales inválidas', 'error') }
  finally { isLoading.value = false }
}

const logout = () => { token.value = null; currentUser.value = null; selectedRole.value = null; credentialEmail.value = ''; password.value = ''; localStorage.removeItem('token'); activeTab.value = 'inicio' }
const authHeaders = () => ({ headers: { Authorization: `Bearer ${token.value}` } })

const fetchData = async () => {
  if (!token.value) return; isLoading.value = true
  try {
    const reqs = []
    reqs.push((currentUser.value?.scopes?.includes('patients:read') || currentUser.value?.scopes?.includes('admin:all')) ? axios.get(`${apiBase}/patients/`, authHeaders()) : Promise.resolve({ data: [] }))
    reqs.push((currentUser.value?.scopes?.includes('practitioners:read') || currentUser.value?.scopes?.includes('admin:all')) ? axios.get(`${apiBase}/practitioners/`, authHeaders()) : Promise.resolve({ data: [] }))
    reqs.push((currentUser.value?.scopes?.includes('appointments:read') || currentUser.value?.scopes?.includes('admin:all')) ? axios.get(`${apiBase}/appointments/`, authHeaders()) : Promise.resolve({ data: [] }))
    const [pRes, prRes, aRes] = await Promise.all(reqs)
    patients.value = pRes.data; practitioners.value = prRes.data; appointments.value = aRes.data
  } catch (err) { if (err.response?.status === 401) logout(); else showToast('Error al sincronizar datos', 'error') }
  finally { isLoading.value = false }
}

const fetchUsers = async () => { if (!currentUser.value?.scopes?.includes('admin:all')) return; try { const res = await axios.get(`${apiBase}/users`, authHeaders()); users.value = res.data } catch {} }

const createPatient = async () => {
  if (!newPatient.value.name || !newPatient.value.identifier) { showToast('Nombre e identificador requeridos', 'error'); return }
  isLoading.value = true
  try { await axios.post(`${apiBase}/patients/`, { id: `pat-${Date.now()}`, identifier: newPatient.value.identifier.trim(), name: newPatient.value.name.trim(), birth_date: null }, authHeaders()); showToast('Paciente registrado'); showModal.value = false; newPatient.value = { identifier: '', name: '' }; fetchData() }
  catch (err) { showToast(err.response?.data?.detail || 'Error al registrar paciente', 'error') }
  finally { isLoading.value = false }
}

const createPractitioner = async () => {
  if (!newPractitioner.value.name || !newPractitioner.value.identifier) { showToast('Nombre e identificador requeridos', 'error'); return }
  isLoading.value = true
  try { await axios.post(`${apiBase}/practitioners/`, { id: `prac-${Date.now()}`, identifier: newPractitioner.value.identifier.trim(), name: newPractitioner.value.name.trim(), specialty: newPractitioner.value.specialty || null, telecom: newPractitioner.value.telecom || null }, authHeaders()); showToast('Profesional registrado'); showModal.value = false; newPractitioner.value = { identifier: '', name: '', specialty: '', telecom: '' }; fetchData() }
  catch (err) { showToast(err.response?.data?.detail || 'Error al registrar profesional', 'error') }
  finally { isLoading.value = false }
}

const createAppointment = async () => {
  if (!newAppointment.value.patient_id || !newAppointment.value.practitioner_id || !newAppointment.value.start_time) { showToast('Todos los campos son requeridos', 'error'); return }
  isLoading.value = true
  const start = new Date(newAppointment.value.start_time)
  const end = new Date(start.getTime() + 30 * 60000)
  try { await axios.post(`${apiBase}/appointments/`, { id: `apt-${Date.now()}`, status: newAppointment.value.status, start_time: start.toISOString(), end_time: end.toISOString(), patient_id: newAppointment.value.patient_id, practitioner_id: newAppointment.value.practitioner_id }, authHeaders()); showToast('Cita registrada'); showModal.value = false; newAppointment.value = { patient_id: '', practitioner_id: '', start_time: '', end_time: '', status: 'agendada' }; fetchData() }
  catch (err) { showToast(err.response?.data?.detail || 'Error al registrar cita', 'error') }
  finally { isLoading.value = false }
}

const deleteRecord = async (id, type) => { if (!confirm('¿Eliminar este registro?')) return; try { await axios.delete(`${apiBase}/${type}/${id}/`, authHeaders()); showToast('Registro eliminado'); fetchData() } catch (err) { showToast(err.response?.data?.detail || 'Error al eliminar', 'error') } }

const createUser = async () => {
  if (!newUser.value.email || !newUser.value.full_name || !newUser.value.password) { showToast('Todos los campos son requeridos', 'error'); return }
  isLoading.value = true
  try { await axios.post(`${apiBase}/users`, newUser.value, authHeaders()); showToast('Usuario creado'); showModal.value = false; newUser.value = { email: '', full_name: '', role: 'secretaria', password: '' }; fetchUsers() }
  catch (err) { showToast(err.response?.data?.detail || 'Error al crear usuario', 'error') }
  finally { isLoading.value = false }
}

const deleteUser = async (email) => { if (!confirm(`¿Eliminar usuario ${email}?`)) return; try { await axios.delete(`${apiBase}/users/${email}`, authHeaders()); showToast('Usuario eliminado'); fetchUsers() } catch (err) { showToast(err.response?.data?.detail || 'Error al eliminar usuario', 'error') } }

const statusLabel = (s) => { const map = { agendada:'Agendada', confirmada:'Confirmada', en_curso:'En curso', completada:'Completada', cancelada:'Cancelada', no_asiste:'No asiste', booked:'Agendada', pending:'Pendiente', cancelled:'Cancelada' }; return map[s]||s }
const statusColor = (s) => { const map = { agendada:'bg-blue-50 text-blue-700 border-blue-200', booked:'bg-blue-50 text-blue-700 border-blue-200', confirmada:'bg-emerald-50 text-emerald-700 border-emerald-200', en_curso:'bg-amber-50 text-amber-700 border-amber-200', completada:'bg-green-50 text-green-700 border-green-200', cancelada:'bg-red-50 text-red-700 border-red-200', cancelled:'bg-red-50 text-red-700 border-red-200', no_asiste:'bg-gray-50 text-gray-700 border-gray-200', pending:'bg-purple-50 text-purple-700 border-purple-200' }; return map[s]||'bg-gray-50 text-gray-700 border-gray-200' }

const filteredPatients = computed(() => { if (!searchQuery.value) return patients.value; const q = searchQuery.value.toLowerCase(); return patients.value.filter(p => p.name?.toLowerCase().includes(q) || p.identifier?.toLowerCase().includes(q)) })
const filteredPractitioners = computed(() => { if (!searchQuery.value) return practitioners.value; const q = searchQuery.value.toLowerCase(); return practitioners.value.filter(p => p.name?.toLowerCase().includes(q) || p.specialty?.toLowerCase().includes(q)) })
const filteredAppointments = computed(() => { if (!searchQuery.value) return appointments.value; const q = searchQuery.value.toLowerCase(); return appointments.value.filter(a => a.patient_id?.toLowerCase().includes(q) || a.status?.toLowerCase().includes(q)) })
const todayAppointments = computed(() => appointments.value.filter(a => { const d = new Date(a.start_time); const today = new Date(); return d.toDateString() === today.toDateString() }))

const patientName = (id) => { const p = patients.value.find(x => x.id === id); return p ? p.name : id }
const practitionerName = (id) => { const p = practitioners.value.find(x => x.id === id); return p ? p.name : id }

onMounted(() => {
  if (token.value) { const payload = decodeJwt(token.value); if (payload) { currentUser.value = { email: payload.sub, fullName: payload.full_name || payload.sub, role: payload.role || 'admin', scopes: payload.scopes || [] }; fetchData(); if (payload.role === 'admin') fetchUsers() } }
})
</script>

<template>
<div class="min-h-screen bg-gray-50 text-gray-800 flex flex-col font-sans antialiased">

<!-- ===== LOGIN ===== -->
<div v-if="!token" class="flex-1 flex items-center justify-center p-6">
  <div class="w-full max-w-2xl">
    <div class="text-center mb-8">
      <div class="w-14 h-14 bg-emerald-100 rounded-xl flex items-center justify-center mx-auto mb-3 overflow-hidden"><img src="/logo.webp" alt="Logo" class="w-10 h-10 object-contain" /></div>
      <h1 class="text-2xl font-semibold text-gray-900">Consultorio Central</h1>
      <p class="text-sm text-gray-500 mt-1">Sistema de gestión clínica — Demostración de roles</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
      <button v-for="role in roles" :key="role.id" @click="selectRole(role)" class="text-left p-4 rounded-xl border-2 transition-all" :class="selectedRole === role.id ? 'border-emerald-500 bg-emerald-50 shadow-sm' : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-9 h-9 rounded-lg flex items-center justify-center text-white" :class="role.color === 'emerald' ? 'bg-emerald-600' : role.color === 'blue' ? 'bg-blue-600' : 'bg-violet-600'"><span class="material-symbols-outlined text-[20px]">{{ role.icon }}</span></div>
          <div><p class="text-sm font-semibold text-gray-900">{{ role.label }}</p><p class="text-[11px] text-gray-400 font-mono">{{ role.email }}</p></div>
        </div>
        <p class="text-[11px] text-gray-500 leading-relaxed">{{ role.desc }}</p>
      </button>
    </div>
    <div v-if="selectedRole" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-4">
      <div class="flex items-center justify-between"><span class="text-xs font-medium text-gray-400 uppercase tracking-wide">Credenciales</span><span class="text-[11px] text-gray-400 font-mono">contraseña del usuario</span></div>
      <div class="flex gap-3">
        <input v-model="credentialEmail" placeholder="correo@clinica.com" class="flex-1 border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none font-mono" />
        <input v-model="password" type="password" placeholder="Contraseña" class="w-40 border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" />
        <button @click="login" :disabled="isLoading || !password" class="px-6 py-2.5 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors flex items-center gap-2 disabled:opacity-50 shrink-0"><span v-if="isLoading" class="material-symbols-outlined animate-spin text-[18px]">refresh</span><span v-else>Ingresar como {{ roles.find(r => r.id === selectedRole)?.label }}</span></button>
      </div>
    </div>
  </div>
</div>

<!-- ===== APP SHELL ===== -->
<div v-else class="flex flex-1 overflow-hidden">

  <!-- SIDEBAR -->
  <aside class="w-60 bg-white border-r border-gray-200 flex flex-col shrink-0">
    <div class="p-5 border-b border-gray-100">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center overflow-hidden"><img src="/logo.webp" alt="Logo" class="w-6 h-6 object-contain" /></div>
        <h1 class="text-sm font-semibold text-gray-900 leading-tight">Consultorio</h1>
      </div>
    </div>
    <nav class="flex-1 p-3 space-y-0.5">
      <a @click.prevent="activeTab = 'inicio'" href="#" class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors" :class="activeTab === 'inicio' ? 'bg-emerald-50 text-emerald-700 font-medium' : 'text-gray-600 hover:bg-gray-50'"><span class="material-symbols-outlined text-[20px]">dashboard</span>Inicio</a>
      <a v-if="currentUser?.scopes?.includes('patients:read') || currentUser?.scopes?.includes('admin:all')" @click.prevent="activeTab = 'patients'" href="#" class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors" :class="activeTab === 'patients' ? 'bg-emerald-50 text-emerald-700 font-medium' : 'text-gray-600 hover:bg-gray-50'"><span class="material-symbols-outlined text-[20px]">person</span>Pacientes</a>
      <a v-if="currentUser?.scopes?.includes('appointments:read') || currentUser?.scopes?.includes('admin:all')" @click.prevent="activeTab = 'appointments'" href="#" class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors" :class="activeTab === 'appointments' ? 'bg-emerald-50 text-emerald-700 font-medium' : 'text-gray-600 hover:bg-gray-50'"><span class="material-symbols-outlined text-[20px]">calendar_today</span>Citas</a>
      <a v-if="currentUser?.scopes?.includes('practitioners:read') || currentUser?.scopes?.includes('admin:all')" @click.prevent="activeTab = 'practitioners'" href="#" class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors" :class="activeTab === 'practitioners' ? 'bg-emerald-50 text-emerald-700 font-medium' : 'text-gray-600 hover:bg-gray-50'"><span class="material-symbols-outlined text-[20px]">stethoscope</span>Personal médico</a>
      <div v-if="currentUser?.role === 'admin'" class="pt-2 mt-2 border-t border-gray-100"></div>
      <a v-if="currentUser?.role === 'admin'" @click.prevent="activeTab = 'users'; fetchUsers()" href="#" class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors" :class="activeTab === 'users' ? 'bg-emerald-50 text-emerald-700 font-medium' : 'text-gray-600 hover:bg-gray-50'"><span class="material-symbols-outlined text-[20px]">manage_accounts</span>Gestión de usuarios</a>
    </nav>
    <div class="p-3 border-t border-gray-100">
      <div class="flex items-center gap-3 px-3 py-2 mb-2">
        <div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-xs font-bold text-emerald-700">{{ currentUser?.fullName?.charAt(0) || 'U' }}</div>
        <div class="min-w-0"><p class="text-sm font-medium text-gray-900 truncate">{{ currentUser?.fullName }}</p><p class="text-[11px] text-gray-400">{{ roleLabel }}</p></div>
      </div>
      <a @click.prevent="logout" class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-red-600 hover:bg-red-50 cursor-pointer transition-colors"><span class="material-symbols-outlined text-[20px]">logout</span>Cerrar sesión</a>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="flex-1 flex flex-col min-w-0 bg-gray-50 overflow-hidden">
    <header class="flex justify-between items-center h-14 px-6 bg-white border-b border-gray-200 shrink-0">
      <h2 class="text-base font-semibold text-gray-800">{{ activeTab === 'inicio' ? 'Panel principal' : activeTab === 'patients' ? 'Pacientes' : activeTab === 'appointments' ? 'Citas' : activeTab === 'practitioners' ? 'Personal médico' : 'Gestión de usuarios' }}</h2>
      <button @click="fetchData" class="p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors" title="Actualizar"><span class="material-symbols-outlined text-[20px]" :class="{ 'animate-spin': isLoading }">sync</span></button>
    </header>

    <div class="flex-1 overflow-y-auto p-6 space-y-6">

      <!-- INICIO -->
      <template v-if="activeTab === 'inicio'">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-white rounded-xl border border-gray-200 p-5"><div class="flex items-center justify-between mb-3"><span class="text-xs font-medium text-gray-400 uppercase tracking-wide">Pacientes</span><span class="material-symbols-outlined text-emerald-500 text-[20px]">person</span></div><p class="text-2xl font-semibold text-gray-900">{{ patients.length }}</p><p class="text-xs text-gray-400 mt-1">Total registrados</p></div>
          <div class="bg-white rounded-xl border border-gray-200 p-5"><div class="flex items-center justify-between mb-3"><span class="text-xs font-medium text-gray-400 uppercase tracking-wide">Citas hoy</span><span class="material-symbols-outlined text-emerald-500 text-[20px]">today</span></div><p class="text-2xl font-semibold text-gray-900">{{ todayAppointments.length }}</p><p class="text-xs text-gray-400 mt-1">{{ new Date().toLocaleDateString('es-CL', { weekday:'long', day:'numeric', month:'long' }) }}</p></div>
          <div class="bg-white rounded-xl border border-gray-200 p-5"><div class="flex items-center justify-between mb-3"><span class="text-xs font-medium text-gray-400 uppercase tracking-wide">Personal</span><span class="material-symbols-outlined text-emerald-500 text-[20px]">stethoscope</span></div><p class="text-2xl font-semibold text-gray-900">{{ practitioners.length }}</p><p class="text-xs text-gray-400 mt-1">Médicos y especialistas</p></div>
        </div>
        <div v-if="canWriteAppointments || currentUser?.role === 'medico'" class="bg-white rounded-xl border border-gray-200 p-5">
          <h3 class="text-sm font-semibold text-gray-800 mb-4">Citas del día</h3>
          <div v-if="todayAppointments.length === 0" class="text-center py-8 text-sm text-gray-400"><span class="material-symbols-outlined text-[40px] mb-2 block text-gray-300">event_busy</span>No hay citas programadas para hoy</div>
          <table v-else class="w-full text-sm"><thead><tr class="text-left text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100"><th class="pb-2 font-medium">Hora</th><th class="pb-2 font-medium">Paciente</th><th class="pb-2 font-medium">Profesional</th><th class="pb-2 font-medium">Estado</th></tr></thead><tbody><tr v-for="a in todayAppointments" :key="a.id" class="border-b border-gray-50"><td class="py-2.5 text-gray-700">{{ new Date(a.start_time).toLocaleTimeString('es-CL', { hour:'2-digit', minute:'2-digit' }) }}</td><td class="py-2.5 text-gray-700 font-medium">{{ patientName(a.patient_id) }}</td><td class="py-2.5 text-gray-500">{{ practitionerName(a.practitioner_id) }}</td><td class="py-2.5"><span class="inline-flex px-2 py-0.5 rounded-full text-[11px] font-medium border" :class="statusColor(a.status)">{{ statusLabel(a.status) }}</span></td></tr></tbody></table>
        </div>
      </template>

      <!-- PACIENTES -->
      <template v-if="activeTab === 'patients'">
        <div class="flex items-center justify-between">
          <div class="relative"><span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-gray-400 text-[18px]">search</span><input v-model="searchQuery" placeholder="Buscar paciente..." class="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none w-64" /></div>
          <button v-if="canWritePatients" @click="modalType = 'patient'; showModal = true" class="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors"><span class="material-symbols-outlined text-[18px]">add</span>Nuevo paciente</button>
        </div>
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table class="w-full text-sm"><thead><tr class="text-left text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 bg-gray-50/50"><th class="px-5 py-3 font-medium">Paciente</th><th class="px-5 py-3 font-medium">Identificador</th><th class="px-5 py-3 font-medium text-right w-20">Acciones</th></tr></thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="p in filteredPatients" :key="p.id" class="hover:bg-gray-50/50 transition-colors"><td class="px-5 py-3"><div class="flex items-center gap-3"><div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-xs font-semibold text-emerald-700">{{ p.name?.charAt(0) || '?' }}</div><span class="font-medium text-gray-800">{{ p.name }}</span></div></td><td class="px-5 py-3 text-gray-500 font-mono text-xs">{{ p.identifier }}</td><td class="px-5 py-3 text-right"><button v-if="canWritePatients" @click="deleteRecord(p.id, 'patients')" class="p-1.5 rounded hover:bg-red-50 text-gray-400 hover:text-red-500 transition-colors" title="Eliminar"><span class="material-symbols-outlined text-[18px]">delete</span></button></td></tr>
              <tr v-if="filteredPatients.length === 0 && !isLoading"><td colspan="3" class="px-5 py-12 text-center text-sm text-gray-400"><span class="material-symbols-outlined text-[40px] mb-2 block text-gray-300">folder_open</span>No hay pacientes {{ searchQuery ? 'para esta búsqueda' : 'registrados' }}</td></tr>
            </tbody>
          </table>
        </div>
      </template>

      <!-- CITAS -->
      <template v-if="activeTab === 'appointments'">
        <div class="flex items-center justify-between">
          <div class="relative"><span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-gray-400 text-[18px]">search</span><input v-model="searchQuery" placeholder="Buscar cita..." class="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none w-64" /></div>
          <button v-if="canWriteAppointments" @click="modalType = 'appointment'; showModal = true" class="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors"><span class="material-symbols-outlined text-[18px]">add</span>Nueva cita</button>
        </div>
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table class="w-full text-sm"><thead><tr class="text-left text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 bg-gray-50/50"><th class="px-5 py-3 font-medium">Fecha / Hora</th><th class="px-5 py-3 font-medium">Paciente</th><th class="px-5 py-3 font-medium">Profesional</th><th class="px-5 py-3 font-medium">Estado</th><th class="px-5 py-3 font-medium text-right w-20">Acciones</th></tr></thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="a in filteredAppointments" :key="a.id" class="hover:bg-gray-50/50 transition-colors"><td class="px-5 py-3 text-gray-700">{{ new Date(a.start_time).toLocaleString('es-CL', { day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit' }) }}</td><td class="px-5 py-3 text-gray-700 font-medium">{{ patientName(a.patient_id) }}</td><td class="px-5 py-3 text-gray-500">{{ practitionerName(a.practitioner_id) }}</td><td class="px-5 py-3"><span class="inline-flex px-2 py-0.5 rounded-full text-[11px] font-medium border" :class="statusColor(a.status)">{{ statusLabel(a.status) }}</span></td><td class="px-5 py-3 text-right"><button v-if="canWriteAppointments" @click="deleteRecord(a.id, 'appointments')" class="p-1.5 rounded hover:bg-red-50 text-gray-400 hover:text-red-500 transition-colors" title="Eliminar"><span class="material-symbols-outlined text-[18px]">delete</span></button></td></tr>
              <tr v-if="filteredAppointments.length === 0 && !isLoading"><td colspan="5" class="px-5 py-12 text-center text-sm text-gray-400"><span class="material-symbols-outlined text-[40px] mb-2 block text-gray-300">event_busy</span>No hay citas {{ searchQuery ? 'para esta búsqueda' : 'registradas' }}</td></tr>
            </tbody>
          </table>
        </div>
      </template>

      <!-- PERSONAL MÉDICO -->
      <template v-if="activeTab === 'practitioners'">
        <div class="flex items-center justify-between">
          <div class="relative"><span class="absolute left-3 top-1/2 -translate-y-1/2 material-symbols-outlined text-gray-400 text-[18px]">search</span><input v-model="searchQuery" placeholder="Buscar profesional..." class="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none w-64" /></div>
          <button v-if="canWritePractitioners" @click="modalType = 'practitioner'; showModal = true" class="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors"><span class="material-symbols-outlined text-[18px]">add</span>Nuevo profesional</button>
        </div>
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table class="w-full text-sm"><thead><tr class="text-left text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 bg-gray-50/50"><th class="px-5 py-3 font-medium">Profesional</th><th class="px-5 py-3 font-medium">Especialidad</th><th class="px-5 py-3 font-medium">Contacto</th><th class="px-5 py-3 font-medium text-right w-20">Acciones</th></tr></thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="pr in filteredPractitioners" :key="pr.id" class="hover:bg-gray-50/50 transition-colors"><td class="px-5 py-3"><div class="flex items-center gap-3"><div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-xs font-semibold text-blue-700">{{ pr.name?.charAt(0) || '?' }}</div><span class="font-medium text-gray-800">{{ pr.name }}</span></div></td><td class="px-5 py-3 text-gray-500">{{ pr.specialty || 'Medicina general' }}</td><td class="px-5 py-3 text-gray-500 text-xs font-mono">{{ pr.telecom || '—' }}</td><td class="px-5 py-3 text-right"><button v-if="canWritePractitioners" @click="deleteRecord(pr.id, 'practitioners')" class="p-1.5 rounded hover:bg-red-50 text-gray-400 hover:text-red-500 transition-colors" title="Eliminar"><span class="material-symbols-outlined text-[18px]">delete</span></button></td></tr>
              <tr v-if="filteredPractitioners.length === 0 && !isLoading"><td colspan="4" class="px-5 py-12 text-center text-sm text-gray-400"><span class="material-symbols-outlined text-[40px] mb-2 block text-gray-300">folder_open</span>No hay profesionales registrados</td></tr>
            </tbody>
          </table>
        </div>
      </template>

      <!-- GESTIÓN DE USUARIOS -->
      <template v-if="activeTab === 'users'">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-gray-700">Usuarios del sistema</h3>
          <button @click="modalType = 'user'; showModal = true" class="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors"><span class="material-symbols-outlined text-[18px]">person_add</span>Nuevo usuario</button>
        </div>
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table class="w-full text-sm"><thead><tr class="text-left text-xs text-gray-400 uppercase tracking-wide border-b border-gray-100 bg-gray-50/50"><th class="px-5 py-3 font-medium">Usuario</th><th class="px-5 py-3 font-medium">Rol</th><th class="px-5 py-3 font-medium">Permisos</th><th class="px-5 py-3 font-medium text-right w-20">Acciones</th></tr></thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="u in users" :key="u.email" class="hover:bg-gray-50/50 transition-colors">
                <td class="px-5 py-3"><div class="flex items-center gap-3"><div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-xs font-semibold text-emerald-700">{{ u.full_name?.charAt(0) || '?' }}</div><div><p class="font-medium text-gray-800">{{ u.full_name }}</p><p class="text-[11px] text-gray-400 font-mono">{{ u.email }}</p></div></div></td>
                <td class="px-5 py-3"><span class="inline-flex px-2 py-0.5 rounded-full text-[11px] font-medium border" :class="u.role === 'admin' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : u.role === 'medico' ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-violet-50 text-violet-700 border-violet-200'">{{ u.role === 'admin' ? 'Administrador' : u.role === 'medico' ? 'Médico' : 'Secretaria' }}</span></td>
                <td class="px-5 py-3 text-[11px] text-gray-400">{{ u.scopes?.length || 0 }} scopes</td>
                <td class="px-5 py-3 text-right"><button @click="deleteUser(u.email)" :disabled="u.email === currentUser?.email" class="p-1.5 rounded hover:bg-red-50 text-gray-400 hover:text-red-500 transition-colors disabled:opacity-30 disabled:cursor-not-allowed" :title="u.email === currentUser?.email ? 'No puedes eliminarte a ti mismo' : 'Eliminar'"><span class="material-symbols-outlined text-[18px]">delete</span></button></td>
              </tr>
              <tr v-if="users.length === 0 && !isLoading"><td colspan="4" class="px-5 py-12 text-center text-sm text-gray-400"><span class="material-symbols-outlined text-[40px] mb-2 block text-gray-300">group_off</span>No hay usuarios registrados</td></tr>
            </tbody>
          </table>
        </div>
      </template>

    </div>
  </main>

</div>

<!-- ===== MODAL ===== -->
<div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/20 backdrop-blur-sm">
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 w-full max-w-md overflow-hidden">
    <div class="px-5 py-4 border-b border-gray-100 flex justify-between items-center">
      <h3 class="text-base font-semibold text-gray-800">{{ modalType === 'practitioner' ? 'Nuevo profesional' : modalType === 'appointment' ? 'Nueva cita' : modalType === 'user' ? 'Nuevo usuario' : 'Nuevo paciente' }}</h3>
      <button @click="showModal = false" class="text-gray-400 hover:text-gray-600 transition-colors material-symbols-outlined">close</button>
    </div>

    <!-- Patient form -->
    <div v-if="modalType === 'patient'" class="p-5 space-y-4">
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Nombre completo</label><input v-model="newPatient.name" placeholder="Ej: Juan Pérez" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Identificador (RUT)</label><input :value="newPatient.identifier" @input="handleRutInput($event, newPatient, 'identifier')" placeholder="12345678-9" maxlength="11" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm font-mono focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
    </div>

    <!-- Practitioner form -->
    <div v-if="modalType === 'practitioner'" class="p-5 space-y-4">
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Nombre completo</label><input v-model="newPractitioner.name" placeholder="Ej: Dra. María González" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Identificador (RUT)</label><input :value="newPractitioner.identifier" @input="handleRutInput($event, newPractitioner, 'identifier')" placeholder="12345678-9" maxlength="11" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm font-mono focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Especialidad</label><input v-model="newPractitioner.specialty" placeholder="Medicina general" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Contacto</label><input v-model="newPractitioner.telecom" placeholder="+56 9 1234 5678" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
    </div>

    <!-- Appointment form -->
    <div v-if="modalType === 'appointment'" class="p-5 space-y-4">
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Paciente</label><select v-model="newAppointment.patient_id" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm bg-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"><option value="" disabled>Seleccionar paciente...</option><option v-for="p in patients" :key="p.id" :value="p.id">{{ p.name }} ({{ p.identifier }})</option></select></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Profesional</label><select v-model="newAppointment.practitioner_id" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm bg-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"><option value="" disabled>Seleccionar profesional...</option><option v-for="pr in practitioners" :key="pr.id" :value="pr.id">{{ pr.name }} – {{ pr.specialty || 'Medicina general' }}</option></select></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Fecha y hora</label><input v-model="newAppointment.start_time" type="datetime-local" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Estado</label><select v-model="newAppointment.status" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm bg-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"><option value="agendada">Agendada</option><option value="confirmada">Confirmada</option><option value="cancelada">Cancelada</option></select></div>
    </div>

    <!-- User form -->
    <div v-if="modalType === 'user'" class="p-5 space-y-4">
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Nombre completo</label><input v-model="newUser.full_name" placeholder="Ej: Dra. María González" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Correo electrónico</label><input v-model="newUser.email" type="email" placeholder="usuario@clinica.com" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none font-mono" /></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Rol</label><select v-model="newUser.role" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm bg-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"><option value="medico">Médico</option><option value="secretaria">Secretaria</option><option value="admin">Administrador</option></select></div>
      <div><label class="block text-xs font-medium text-gray-500 mb-1">Contraseña</label><input v-model="newUser.password" type="text" placeholder="Mínimo 6 caracteres" class="w-full border border-gray-200 p-2.5 rounded-lg text-sm focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none" /></div>
    </div>

    <div class="px-5 py-4 border-t border-gray-100 bg-gray-50 flex gap-3 justify-end">
      <button @click="showModal = false" class="px-4 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors">Cancelar</button>
      <button @click="modalType === 'practitioner' ? createPractitioner() : modalType === 'appointment' ? createAppointment() : modalType === 'user' ? createUser() : createPatient()" :disabled="isLoading" class="px-4 py-2 bg-emerald-600 rounded-lg text-sm font-medium text-white hover:bg-emerald-700 transition-colors flex items-center gap-2 disabled:opacity-50"><span v-if="isLoading" class="material-symbols-outlined animate-spin text-[18px]">refresh</span><span v-else>Guardar</span></button>
    </div>
  </div>
</div>

<!-- ===== TOAST ===== -->
<Transition name="toast">
  <div v-if="toast.show" class="fixed bottom-6 right-6 flex items-center gap-2.5 px-4 py-3 rounded-lg shadow-lg border z-50 text-sm font-medium" :class="toast.type === 'error' ? 'bg-red-50 border-red-200 text-red-700' : 'bg-white border-gray-200 text-gray-800'">
    <span class="material-symbols-outlined text-[18px]">{{ toast.type === 'error' ? 'error' : 'check_circle' }}</span>{{ toast.msg }}
  </div>
</Transition>

</div>
</template>

<style>
.toast-enter-active, .toast-leave-active { transition: all 0.25s ease; }
.toast-enter-from { opacity: 0; transform: translateY(0.5rem); }
.toast-leave-to { opacity: 0; transform: translateY(0.5rem); }
</style>
