"""Test device API endpoints."""


class TestDevices:
    """Test all devices API endpoints."""

    def test_create_device_success_201(self, test_client):
        """Validate we get a 201 and can create a device."""
        payload = {"name": "test-dev01", "model": "9200-48p", "site": "CO", "role": "access"}
        response = test_client.post("/api/v1/devices/", json=payload)

        assert response.status_code == 201

    def test_create_device_duplicate_409(self, test_client):
        """Validate we get a 409 and cannot create a duplicate device."""
        payload = {"name": "test-dev01", "model": "9200-48p", "site": "CO", "role": "access"}
        response = test_client.post("/api/v1/devices/", json=payload)

        assert response.status_code == 409

    def test_get_all_devices_200(self, test_client):
        """Validate we get a 200 and return two devices."""
        payload = {"name": "test-dev02", "model": "9300-48p", "site": "AZ", "role": "datacenter"}
        test_client.post("/api/v1/devices/", json=payload)

        response = test_client.get("/api/v1/devices/")

        assert response.status_code == 200
        assert response.json()["count"] == 3

    def test_get_single_device_200(self, test_client):
        """Validate we get a 200 and can retrieve a single device."""
        self.devices_collection_name = "devices"

        response = test_client.get("/api/v1/devices/test-dev01")

        resp_data = response.json()
        assert response.status_code == 200
        assert resp_data["name"] == "test-dev01"
        assert resp_data["model"] == "9200-48p"
        assert resp_data["site"] == "CO"
        assert resp_data["role"] == "access"

    def test_get_all_devices_filter_site(self, test_client):
        """Validate we get a 200 and test-dev01."""
        response = test_client.get("/api/v1/devices/?site=CO")

        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["name"] == "test-dev01"

    def test_get_all_devices_filter_role(self, test_client):
        """Validate we get a 200 and return test-dev01."""
        response = test_client.get("/api/v1/devices/?role=access")

        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["name"] == "test-dev01"

    def test_get_all_devices_filter_model(self, test_client):
        """Validate we get a 200 and return test-dev01."""
        response = test_client.get("/api/v1/devices/?model=9200-48p")

        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["name"] == "test-dev01"

    def test_get_all_devices_limit_200(self, test_client):
        """Validate we get a 200 and return test-dev01."""
        response = test_client.get("/api/v1/devices/?limit=1")

        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["name"] == "test-dev999"

    def test_get_all_devices_skip_limit_200(self, test_client):
        """Validate we get a 200 and return test-dev02."""
        response = test_client.get("/api/v1/devices/?skip=1&limit=1")

        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["name"] == "test-dev01"

    def test_delete_single_device_204(self, test_client):
        """Validate we get a 204 when deleting a device."""
        # Create a command the existing device and validate it was posted
        payload = {"command": "show version", "data_type": "raw", "data": "0.1.0"}
        test_client.post("/api/v1/commands/test-dev01/", json=payload)
        assert test_client.get("/api/v1/commands/test-dev01").json()["count"] == 1

        # Delete the device
        response = test_client.delete("/api/v1/devices/test-dev01")

        assert response.status_code == 204
        # Validate our background task worked and delete command created above that was tied to the deleted device
        response = test_client.get("/api/v1/commands/test-dev01")
        assert response.status_code == 404

    def test_delete_single_device_404(self, test_client):
        """Validate we get a 404 when deleting a device that doesn't exist."""
        response = test_client.delete("/api/v1/devices/test-dev01")

        assert response.status_code == 404
        assert response.json()["detail"] == "Device 'test-dev01' does not exist in devices collection."
