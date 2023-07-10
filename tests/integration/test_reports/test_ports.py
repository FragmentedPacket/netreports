"""Test ports report API endpoints."""


class TestPorts:
    """Test all devices API endpoints."""

    def test_create_large_payload_201(self, test_client):
        """Validate we get a 201 and can create a device."""
        payload = [
            {"device": f"device{i}", "ports_total": 192, "ports_up": 100, "ports_down": 100, "ports_shutdown": 100}
            for i in range(500000)
        ]
        response = test_client.post("/api/reports/ports/", json=payload)

        assert response.status_code == 201
        assert response.elapsed.total_seconds() < 16

    def test_get_all_ports_info_200(self, test_client):
        """Validate we get a 200 and proper count of ports."""
        response = test_client.get("/api/reports/ports/?limit=0")

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 16
        assert response.json()["count"] == 500_000
