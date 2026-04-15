import React, { useState } from 'react';
import { Form, Button, Container, Alert, Card } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';

const AgendarCita = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        paciente_id: '',
        fecha_hora: '',
        motivo: ''
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
            const res = await fetch('http://localhost:8000/citas/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    paciente_id: parseInt(formData.paciente_id),
                    fecha: formData.fecha_hora,
                    razon: formData.motivo
                })
            });

            if (!res.ok) {
                const data = await res.json();
                 let errorMsg = 'Error al agendar la cita';
                if (data.detail && typeof data.detail === 'string') {
                    errorMsg = data.detail;
                } else if (data.detail && Array.isArray(data.detail)) {
                    errorMsg = data.detail.map(d => d.msg).join(', ');
                }
                setError(errorMsg);
            } else {
                setSuccess(true);
                setTimeout(() => navigate('/'), 1500); 
            }
        } catch (err) {
            setError('Error de conectividad con el servidor.');
        }
    };

    return (
        <Container className="pt-5 d-flex justify-content-center">
            <Card style={{ width: '40rem', maxWidth: '100%' }} className="shadow border-0">
                <Card.Header className="bg-primary text-white py-3">
                    <h5 className="mb-0 fw-bold px-2">Agendar Nueva Cita</h5>
                </Card.Header>
                <Card.Body className="p-4 px-md-5">
                    {error && <Alert variant="danger" className="text-center fw-bold">{error}</Alert>}
                    {success && <Alert variant="success" className="text-center fw-bold">Cita agendada exitosamente. Redirigiendo...</Alert>}
                    
                    <Form onSubmit={handleSubmit} className="mt-2">
                        <Form.Group className="mb-4">
                            <Form.Label className="fw-bold text-muted small text-uppercase">ID del Paciente</Form.Label>
                            <Form.Control 
                                type="number" name="paciente_id" placeholder="Ingrese ID interno"
                                value={formData.paciente_id} onChange={handleChange} required 
                            />
                            <Form.Text className="text-muted">
                                (En una versión avanzada aquí iría un buscador por RUT/Nombre en tiempo real).
                            </Form.Text>
                        </Form.Group>
                        
                        <Form.Group className="mb-4">
                            <Form.Label className="fw-bold text-muted small text-uppercase">Fecha y Hora</Form.Label>
                            <Form.Control 
                                type="datetime-local" name="fecha_hora" 
                                value={formData.fecha_hora} onChange={handleChange} required 
                            />
                        </Form.Group>

                        <Form.Group className="mb-4">
                            <Form.Label className="fw-bold text-muted small text-uppercase">Motivo de la Cita</Form.Label>
                            <Form.Control 
                                as="textarea" rows={3} name="motivo" placeholder="Ej: Control general"
                                value={formData.motivo} onChange={handleChange} required 
                            />
                        </Form.Group>
                        
                        <hr className="mb-4 text-muted" />

                        <div className="d-flex justify-content-end gap-3">
                            <Link to="/" className="btn btn-light border px-4 shadow-sm">
                                Volver
                            </Link>
                            <Button variant="primary" type="submit" className="px-4 shadow-sm fw-bold">
                                Confirmar Cita
                            </Button>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default AgendarCita;
