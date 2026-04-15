import React, { useState } from 'react';
import { Form, Button, Container, Alert, Card } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';

const CrearPaciente = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        nombre: '',
        apellido: '',
        rut: '',
        telefono: '',
        correo: ''
    });
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(false);
        
        try {
            // Asumiendo que el backend corre en el puerto 8000
            const res = await fetch('http://localhost:8000/pacientes/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!res.ok) {
                const data = await res.json();
                // Extrayendo el mensaje de pydantic o FastAPI
                let errorMsg = 'Error guardando el paciente';
                if (data.detail && typeof data.detail === 'string') {
                    errorMsg = data.detail;
                } else if (data.detail && Array.isArray(data.detail)) {
                    errorMsg = data.detail.map(d => d.msg).join(', ');
                }
                setError(errorMsg);
            } else {
                setSuccess(true);
                setTimeout(() => navigate('/'), 1500); // Redirigir después de 1.5s
            }
        } catch (err) {
            setError('Error de conectividad, el servidor podría estar apagado.');
        }
    };

    return (
        <Container className="pt-5 d-flex justify-content-center">
            <Card style={{ width: '45rem', maxWidth: '100%' }} className="shadow border-0">
                <Card.Header className="bg-success text-white py-3">
                    <h5 className="mb-0 fw-bold px-2">Registro de Nuevo Paciente</h5>
                </Card.Header>
                <Card.Body className="p-4 px-md-5">
                    {/* Alertas requeridas por requerimiento (corta y sencilla debajo del form o arriba) */}
                    {error && <Alert variant="danger" className="text-center fw-bold">{error}</Alert>}
                    {success && <Alert variant="success" className="text-center fw-bold">Paciente creado exitosamente. Redirigiendo...</Alert>}
                    
                    <Form onSubmit={handleSubmit} className="mt-2">
                        <Form.Group className="mb-3">
                            <Form.Label className="fw-bold text-muted small text-uppercase">RUT de Identidad</Form.Label>
                            <Form.Control 
                                type="text" name="rut" placeholder="Ej: 12345678-9" 
                                value={formData.rut} onChange={handleChange} required 
                            />
                        </Form.Group>
                        
                        <div className="row">
                            <Form.Group className="mb-3 col-md-6">
                                <Form.Label className="fw-bold text-muted small text-uppercase">Nombres</Form.Label>
                                <Form.Control 
                                    type="text" name="nombre" placeholder="Nombres del paciente"
                                    value={formData.nombre} onChange={handleChange} required 
                                />
                            </Form.Group>
                            <Form.Group className="mb-3 col-md-6">
                                <Form.Label className="fw-bold text-muted small text-uppercase">Apellidos</Form.Label>
                                <Form.Control 
                                    type="text" name="apellido" placeholder="Apellidos"
                                    value={formData.apellido} onChange={handleChange} required 
                                />
                            </Form.Group>
                        </div>

                        <div className="row">
                            <Form.Group className="mb-3 col-md-6">
                                <Form.Label className="fw-bold text-muted small text-uppercase">Correo Electrónico</Form.Label>
                                <Form.Control 
                                    type="email" name="correo" placeholder="ejemplo@email.com"
                                    value={formData.correo} onChange={handleChange} 
                                />
                            </Form.Group>
                            <Form.Group className="mb-4 col-md-6">
                                <Form.Label className="fw-bold text-muted small text-uppercase">Teléfono</Form.Label>
                                <Form.Control 
                                    type="text" name="telefono" placeholder="+56 9 ..."
                                    value={formData.telefono} onChange={handleChange} 
                                />
                            </Form.Group>
                        </div>
                        
                        <hr className="mb-4 text-muted" />

                        <div className="d-flex justify-content-end gap-3">
                            <Link to="/" className="btn btn-light border px-4 shadow-sm">
                                Cancelar
                            </Link>
                            <Button variant="success" type="submit" className="px-4 shadow-sm fw-bold">
                                Guardar Registro
                            </Button>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default CrearPaciente;
