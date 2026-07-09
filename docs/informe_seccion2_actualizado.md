## 2. Requerimientos del Sistema

### 2.1 Requerimientos Funcionales (RF)

#### Harness

**RF01** — El harness debe proveer skills que guíen al modelo de IA por un pipeline de desarrollo, forzando que el modelo pregunte antes de generar código.

**RF02** — El harness debe cargar automáticamente reglas de comportamiento en cada sesión que impidan al modelo decidir tecnologías, agregar features no pedidas o inventar dependencias.

**RF03** — El harness debe instalarse en cualquier proyecto con un comando, sin dependencias externas.

**RF04** — El harness debe preservar el estado del desarrollo entre sesiones de IA.

#### Producto

**RF05** — El sistema debe definir su nivel de gobernanza (bajo, medio o alto) antes del desarrollo.

**RF06** — El sistema debe permitir crear, leer, modificar y eliminar pacientes, médicos y citas.

**RF07** — El sistema debe impedir agendar citas en el pasado, para pacientes o médicos inexistentes, o con horarios solapados.

**RF08** — El sistema debe registrar quién creó, modificó o eliminó cada dato, qué cambió y cuándo.

**RF09** — El acceso a funcionalidades debe restringirse según el rol del usuario. Un médico solo modifica sus propias citas. Solo el admin ve la auditoría y gestiona usuarios.

**RF10** — El admin debe poder crear, listar y eliminar usuarios, y regenerar sus credenciales.

**RF11** — El admin debe poder consultar el historial de cambios filtrable por entidad, operación y usuario.

**RF12** — Todo módulo generado debe incluir tests que verifiquen su correcto funcionamiento.

### 2.2 Requerimientos No Funcionales (RNF)

#### Harness

**RNF01** — Cada decisión de diseño debe documentarse con su justificación y ser trazable a una respuesta del desarrollador.

#### Producto

**RNF02** — El código debe organizarse en módulos independientes con funciones de máximo 50 líneas.

**RNF03** — El estilo de código y nomenclatura debe ser uniforme en todo el proyecto.

**RNF04** — Las contraseñas deben almacenarse hasheadas. Datos sensibles no deben aparecer en logs. La configuración debe usar variables de entorno, sin valores hardcodeados.
