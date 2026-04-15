import React, { useEffect, useState } from 'react';
import { Table, Container, Row, Col, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const [citas, setCitas] = useState([]);
    const [pacientes, setPacientes] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                // Obtenemos pacientes y los dejamos en un mapa { id: paciente }
                const pacRes = await fetch('http://localhost:8000/pacientes/');
                if (pacRes.ok) {
                    const pacData = await pacRes.json();
                    const pacMap = {};
                    pacData.forEach(p => { pacMap[p.id] = p; });
                    setPacientes(pacMap);
                }

                // Obtenemos citas
                const citasRes = await fetch('http://localhost:8000/citas/');
                if (citasRes.ok) {
                    const citasData = await citasRes.json();
                    setCitas(citasData);
                }
            } catch (err) {
                console.error("Error al cargar datos del Dashboard", err);
            }
            setLoading(false);
        };
        fetchData();
    }, []);

    // Formateador de fechas
    const formatDate = (isoString) => {
        const d = new Date(isoString);
        return d.toLocaleDateString('es-CL') + " " + d.toLocaleTimeString('es-CL', {hour: '2-digit', minute:'2-digit'});
    };

    return (
        <Container className="pt-5">
            <Row className="mb-4 align-items-center">
                <Col>
                    <h2 className="text-primary fw-bold mb-0">Consultorio Médico</h2>
                    <p className="text-muted">Gestor de Citas y Pacientes</p>
                </Col>
                <Col className="text-end">
                    <Link to="/nuevo-paciente" className="btn btn-success me-2 px-4 shadow-sm">
                        + Nuevo Paciente
                    </Link>
                    <Link to="/agendar-cita" className="btn btn-primary px-4 shadow-sm">
                        + Agendar Cita
                    </Link>
                </Col>
            </Row>

            <Card className="shadow-sm border-0 rounded-lg">
                <Card.Header className="bg-white py-3">
                    <h5 className="mb-0 text-secondary fw-bold">Citas Registradas</h5>
                </Card.Header>
                <Card.Body className="p-0">
                    <div className="table-responsive">
                        <Table hover className="align-middle mb-0">
                            <thead className="table-light">
                                <tr>
                                    <th className="ps-4">Fecha y Hora</th>
                                    <th>Paciente</th>
                                    <th>RUT</th>
                                    <th>Motivo/Estado</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr>
                                        <td colSpan="4" className="text-center py-5 text-muted">
                                            Cargando citas...
                                        </td>
                                    </tr>
                                ) : citas.length === 0 ? (
                                    <tr>
                                        <td colSpan="4" className="text-center py-5 text-muted">
                                            <i className="bi bi-calendar-x d-block fs-1 mb-2"></i>
                                            No hay citas agendadas hasta el momento.
                                        </td>
                                    </tr>
                                ) : (
                                    citas.map(cita => {
                                        const pac = pacientes[cita.paciente_id] || {};
                                        return (
                                            <tr key={cita.id}>
                                                <td className="ps-4 fw-bold">{formatDate(cita.fecha)}</td>
                                                <td>{pac.nombre} {pac.apellido}</td>
                                                <td>{pac.rut}</td>
                                                <td>{cita.razon}</td>
                                            </tr>
                                        )
                                    })
                                )}
                            </tbody>
                        </Table>
                    </div>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default Dashboard;
