from unittest.mock import MagicMock


def create_appointment(client, monkeypatch, headers):
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_patient_id = MagicMock(return_value=1)
    mock_get_patient_name = MagicMock(return_value='John Doe')
    mock_get_doctor_name = MagicMock(return_value='Dr. Smith')
    monkeypatch.setattr('app.routes.create_appointment.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.create_appointment.get_patient_id', mock_get_patient_id)
    monkeypatch.setattr('app.routes.create_appointment.get_patient_name', mock_get_patient_name)
    monkeypatch.setattr('app.routes.create_appointment.get_doctor_name', mock_get_doctor_name)
    new_appointment = {
        'doctorId': 1,
        'date': '2024-04-01T00:00:00.000Z',
        'time': {'hours': '09', 'minutes': '00'},
    }
    response = client.post('/create-appointment', json=new_appointment, headers=headers)
    return response


def test_create_appointment(client, monkeypatch, headers):
    response = create_appointment(client, monkeypatch, headers)
    assert response.status_code == 201
