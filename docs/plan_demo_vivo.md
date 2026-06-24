# Demo en Vivo — 5 Minutos

> Estrategia: 2 min de interacción live + 3 min de evidencia pre-preparada.

---

## Minuto 0:00 — Apertura (15 seg)

**Qué decir:** "El harness VibeCoding fuerza a la IA a preguntar en vez de asumir. En 5 minutos les muestro cómo."

**Qué mostrar:** Abrir OpenCode. Señalar en la terminal:
```
Instructions from: AGENTS.md
Instructions from: .opencode/rules/vibecoding/01_ask_dont_assume.md
...
```
**Impacto:** Las 4 reglas always-on se cargan solas. Sin configuración manual.

---

## Minuto 0:15 — Interacción Live: PRD Express (1:45 min)

**Prompt:** *"Quiero agregar notificaciones al sistema de consultorio. Cargá la skill de PRD."*

El modelo debe responder con el patrón pregunta-respuesta:

| Pregunta del modelo | Respuesta rápida | Duración |
|---------------------|-----------------|----------|
| ¿Qué tipo de proyecto? | web_app | 10s |
| ¿Problema y propósito? | "Notificar pacientes cuando se agenda/cancela su cita" | 15s |
| ¿Usuarios? | "Los 3 roles existentes. Paciente recibe notificación, admin las gestiona" | 15s |
| ¿Gobernanza? | "Alta, consistente con el sistema actual" | 5s |

**Momento clave:** Señalar que el modelo NO generó código — solo preguntó. Sin harness, habría inventado un stack, creado endpoints, y agregado Docker sin preguntar.

**PRD generado.** Mostrar que cada sección es trazable a una respuesta. → Siguiente.

---

## Minuto 2:00 — Evidencia: Trazabilidad (45 seg)

**Abrir `docs/changelog_impacto_roadmap.md`.** Señalar:

- **4 iteraciones** documentadas, cada decisión trazable
- **70+ preguntas** hechas por el harness en el ciclo de vida del proyecto
- **0 alucinaciones, 0 goldplating, 0 decisiones asumidas** en Iteración 4

---

## Minuto 2:45 — Evidencia: Auditoría en Vivo (45 seg)

**Abrir `localhost:8080`, loguearse como admin.**

- Sidebar → **Auditoría**: 34 eventos agrupados tipo changelog
- Señalar un evento: "recepcionista creó paciente pat-01 a las 08:30"
- Filtros funcionando: entidad, operación, usuario

---

## Minuto 3:30 — Evidencia: Subagentes (45 seg)

**Mostrar `docs/plan_demo_vivo.md` sección 3** o abrir un reporte de code_reviewer:

```
code_reviewer.md: Revisa código contra 4 reglas
planner.md: Descompone features en tareas
security_reviewer.md: Audita OWASP Top 10
```

**Si hay tiempo:** Delegar code_reviewer en vivo: *"Revisá el último PRD generado"*.

---

## Minuto 4:15 — Evidencia: Métricas (30 seg)

**Mostrar tabla resumen:**

| Métrica | Sin Harness | Con Harness |
|---------|:-----------:|:-----------:|
| Alucinaciones | ~10% | **0%** |
| Goldplating | ~25% | **0%** |
| Decisiones no consultadas | ~8 | **0** |
| Tests (11/11) | 0 | **11** |

---

## Minuto 4:45 — Cierre (15 seg)

**Qué decir:** "En 5 minutos vimos: reglas que se cargan solas, skills que preguntan en vez de asumir, trazabilidad total de decisiones, y 0 alucinaciones. El harness no es magia — es estructura."

---

## Requisitos Técnicos para la Demo

- [ ] Docker corriendo (consultorio con seed data)
- [ ] OpenCode abierto con AGENTS.md cargado
- [ ] `docs/changelog_impacto_roadmap.md` abierto en otra pestaña
- [ ] `localhost:8080` abierto con sesión de admin iniciada
- [ ] Conexión a internet (por si se delega un subagente)
- [ ] Tener las respuestas del PRD preparadas (para responder rápido)

## Plan B

| Si falla... | Hacer esto... |
|-------------|--------------|
| El modelo no carga AGENTS.md | Decir "Cargá las reglas de AGENTS.md" manualmente |
| El modelo no activa la skill | Decir "Cargá la skill 01_prd de .opencode/skills/" |
| El modelo alucina o asume | Señalarlo: "Esto es exactamente lo que el harness previene. Sin él, pasaría en cada sesión." |
| Docker no responde | Mostrar screenshots del sistema (tomar antes de la demo) |
| Se acaba el tiempo antes | Saltar a métricas (minuto 4:15) directamente |

## Screenshots a Preparar (backup)

1. AGENTS.md cargándose al inicio de sesión
2. Modelo preguntando "¿Qué tipo de proyecto?" (sin generar código)
3. Vista de Auditoría con 34 eventos
4. Tabla de métricas del changelog
5. Reporte de code_reviewer o security_reviewer
