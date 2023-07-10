"""Test the devices API endpoints."""

from copy import copy
from datetime import datetime
from unittest.mock import AsyncMock, patch

from bson.objectid import ObjectId
from pymongo import errors
import pytest


@patch("netreports.api.v1.endpoints.devices.create_device", new_callable=AsyncMock)
def test_post_device_201(
    create_device,
    test_client,
):
    """Validate posting a new devices results in 201 and proper return."""
    # Build payload and resp_payload
    payload = {"name": "test-dev01", "model": "9200-48p", "site": "CO", "role": "access"}
    resp_payload = copy(payload)
    resp_payload["_id"] = ObjectId()
    resp_payload["commands"] = {}
    resp_payload["lastupdate"] = datetime.now()
    create_device.return_value = resp_payload

    response = test_client.post("/api/v1/devices", json=payload)

    assert response.status_code == 201
    create_device.assert_awaited_once()

    # Convert to JSON payload
    response = response.json()

    # Assert _id in resp_payload and then pop for comparison
    assert "_id" in response
    response.pop("_id")

    assert "lastupdate" in response
    response.pop("lastupdate")

    assert response == payload


@patch(
    "netreports.api.v1.endpoints.devices.create_device",
    side_effect=errors.DuplicateKeyError("Already exists."),
    new_callable=AsyncMock,
)
def test_post_device_already_exists_409(create_device, test_client):
    """Validate posting a device that already exists results in 409 and proper return."""
    # Build payload
    payload = {"name": "test-dev01", "model": "9200-48p", "site": "CO", "role": "access"}
    # Setup resp_payload
    find_payload = copy(payload)
    find_payload["_id"] = ObjectId()
    find_payload["lastupdate"] = datetime.now()
    create_device.return_value = find_payload

    response = test_client.post("/api/v1/devices", json=payload)

    assert response.status_code == 409
    create_device.assert_awaited_once()


@pytest.mark.parametrize("field", ("name", "model", "site", "role"))
def test_post_invalid_body_422(test_client, field):
    """Validate we get a 422 error back for missing required fields."""
    payload = {"name": "no-role-in-life", "model": "c9200-48p", "site": "CO", "role": "access"}
    payload.pop(field)
    response = test_client.post("/api/v1/devices", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["body", field], "msg": "field required", "type": "value_error.missing"}]
    }


@patch("netreports.api.v1.endpoints.devices.create_device", new_callable=AsyncMock)
@pytest.mark.parametrize("role_choice", ("access", "datacenter"))
def test_post_valid_roles(create_device, test_client, role_choice):
    """Validate only proper choices for role work."""
    payload = {"name": "no-role-in-life", "model": "c9200-48p", "site": "CO", "role": role_choice}
    resp_payload = copy(payload)
    resp_payload["_id"] = ObjectId()
    resp_payload["lastupdate"] = datetime.now().isoformat()
    create_device.return_value = resp_payload
    response = test_client.post("/api/v1/devices", json=payload)

    create_device.assert_awaited_once()
    assert response.status_code == 201
    assert response.json()["role"] == role_choice


@pytest.mark.parametrize("role_choice", ("atm", "edge", "wan"))
def test_post_invalid_roles(test_client, role_choice):
    """Validate only proper choices for role work."""
    payload = {"name": "no-role-in-life", "model": "c9200-48p", "site": "CO", "role": role_choice}
    response = test_client.post("/api/v1/devices", json=payload)

    assert response.status_code == 422


@patch("netreports.api.v1.endpoints.devices.get_documents", new_callable=AsyncMock)
def test_get_all_devices_200(get_documents, test_client, get_all_device_docs):
    """Validate get all devices."""
    get_documents.return_value = get_all_device_docs
    response = test_client.get("/api/v1/devices")

    resp_json = response.json()
    get_documents.assert_called_once()
    assert response.status_code == 200
    assert resp_json["count"] == 4
    assert len(resp_json["results"]) == 4


@patch("netreports.api.v1.endpoints.devices.get_documents", new_callable=AsyncMock)
def test_get_all_devices_filter_site_200(get_documents, test_client, get_all_device_docs):
    """Validate get all devices."""
    dc1_devices = [device for device in get_all_device_docs[1] if device["site"] == "datacenter1"]
    get_documents.return_value = len(dc1_devices), dc1_devices
    response = test_client.get("/api/v1/devices?site=datacenter1")

    resp_json = response.json()
    get_documents.assert_called_once()
    assert response.status_code == 200
    assert resp_json["count"] == 2
    assert len(resp_json["results"]) == 2


@patch("netreports.api.v1.endpoints.devices.get_documents", new_callable=AsyncMock)
def test_get_all_devices_filter_model_200(get_documents, test_client, get_all_device_docs):
    """Validate get all devices."""
    model_devices = [device for device in get_all_device_docs[1] if device["model"] == "7280QR2"]
    get_documents.return_value = len(model_devices), model_devices
    response = test_client.get("/api/v1/devices?model=7280QR2")

    resp_json = response.json()
    get_documents.assert_called_once()
    assert response.status_code == 200
    assert resp_json["count"] == 2
    assert len(resp_json["results"]) == 2


@patch("netreports.api.v1.endpoints.devices.get_documents", new_callable=AsyncMock)
def test_get_all_devices_filter_role_200(get_documents, test_client, get_all_device_docs):
    """Validate get all devices."""
    access_devices = [device for device in get_all_device_docs[1] if device["role"] == "access"]
    get_documents.return_value = len(access_devices), access_devices
    response = test_client.get("/api/v1/devices?role=access")

    resp_json = response.json()
    get_documents.assert_called_once()
    assert response.status_code == 200
    assert resp_json["count"] == 2
    assert len(resp_json["results"]) == 2


@patch("netreports.api.v1.endpoints.devices.get_one_device", new_callable=AsyncMock)
def test_get_single_device_200(get_one_device, test_client):
    """Validate single device exists and returns 200."""
    find_one_return = {
        "_id": "639e3d2843f2ab668befab9e",
        "name": "test-device02",
        "model": "c9200-48p",
        "site": "AZ",
        "role": "access",
        "lastupdate": datetime.now().isoformat(),
    }
    get_one_device.return_value = find_one_return
    response = test_client.get("/api/v1/devices/test-device02")

    get_one_device.assert_awaited_once()

    assert response.status_code == 200
    assert response.json() == find_one_return


@patch("netreports.api.v1.endpoints.devices.get_one_device", return_value=None, new_callable=AsyncMock)
def test_get_single_device_404(get_one_device, test_client):
    """Validate single device is not present and 404 returned."""
    response = test_client.get("/api/v1/devices/no-device02")

    get_one_device.assert_awaited_once()
    assert response.status_code == 404


@patch(
    "netreports.api.v1.endpoints.devices.delete_all_commands_for_device",
    return_value=None,
    new_callable=AsyncMock,
)
@patch("netreports.api.v1.endpoints.devices.get_one_device_raw", new_callable=AsyncMock)
@patch("netreports.api.v1.endpoints.devices.delete_device", new_callable=AsyncMock)
def test_delete_single_device_204(delete_device, get_one_device, background_task, test_client):
    """Validate you can delete device and 204 returned."""
    find_one_return = {
        "_id": "639e3d2843f2ab668befab9e",
        "name": "test-device02",
        "model": "c9200-48p",
        "site": "AZ",
        "role": "access",
        "lastupdate": datetime.now().isoformat(),
    }
    get_one_device.return_value = find_one_return
    response = test_client.delete("/api/v1/devices/device01")

    delete_device.assert_awaited_once()
    background_task.assert_called_once()
    assert response.status_code == 204


@patch("netreports.api.v1.endpoints.devices.get_one_device_raw", return_value=None, new_callable=AsyncMock)
def test_delete_single_device_404(get_one_device, test_client):
    """Validate single device is not present and 404 returned."""
    response = test_client.delete("/api/v1/devices/no-device01")

    get_one_device.assert_awaited_once()
    assert response.status_code == 404
    assert response.json()["detail"] == "Device 'no-device01' does not exist in devices collection."
