"""Test device API endpoints."""


class TestCommands:
    """Test Commands API endpoints."""

    def test_create_command_success_201(self, test_client, device_name):
        """Validate we get a 201 and can create a command."""
        # POST command
        payload = {"command": "show version", "data_type": "raw", "data": "my raw data"}
        response = test_client.post(f"/api/v1/commands/{device_name}/", json=payload)

        assert response.status_code == 201

        resp_data = response.json()
        assert resp_data["command"] == "show version"
        assert resp_data["data_type"] == "raw"
        assert resp_data["data"] == "my raw data"
        assert resp_data["model"] == "9400-48p"
        assert resp_data["site"] == "AZ"
        assert resp_data["roles"] == ["datacenter"]

    def test_create_command_duplicate_409(self, test_client, device_name):
        """Validate we get a 409 and cannot create a duplicate command."""
        payload = {"command": "show version", "data_type": "raw", "data": "my raw data."}
        response = test_client.post(f"/api/v1/commands/{device_name}/", json=payload)

        assert response.status_code == 409

    def test_create_command_bad_device_404(self, test_client):
        """Validate we get a 404 due to bad device."""
        payload = {"command": "show version", "data_type": "raw", "data": "my raw data."}
        response = test_client.post(f"/api/v1/commands/bad-device01/", json=payload)

        assert response.status_code == 404
        assert response.json()["message"] == f"bad-device01 does not exist in devices collection."

    def test_create_command_different_data_type_201(self, test_client, device_name):
        """Validate we get a 201 and can create same command with different data_type."""
        # POST command
        payload = {"command": "show version", "data_type": "ntc_templates", "data": [{"VERSION": "4.29M"}]}
        response = test_client.post(f"/api/v1/commands/{device_name}/", json=payload)

        assert response.status_code == 201

        resp_data = response.json()
        assert resp_data["command"] == "show version"
        assert resp_data["data_type"] == "ntc_templates"
        assert resp_data["data"] == [{"VERSION": "4.29M"}]
        assert resp_data["model"] == "9400-48p"
        assert resp_data["site"] == "AZ"
        assert resp_data["roles"] == ["datacenter"]

    def test_get_all_commands_device_200(self, test_client, device_name):
        """Validate we get a 200 and return two commands."""
        payload = {"command": "show interfaces", "data_type": "genie", "data": ["interface GigabitEthernet1/0/1"]}
        response = test_client.post(f"/api/v1/commands/{device_name}/", json=payload)
        assert response.status_code == 201

        response = test_client.get(f"/api/v1/commands/{device_name}")

        assert response.status_code == 200
        assert response.json()["count"] == 3

    def test_get_all_commands_for_bad_device_404(self, test_client):
        """Validate we get a 404 due to non-existent device."""
        response = test_client.get(f"/api/v1/commands/fake-device01")

        assert response.status_code == 404

    def test_get_command_with_multiple_data_types_200(self, test_client, device_name):
        """Validate we get a 200 and can retrieve a single command."""
        response = test_client.get(f"/api/v1/commands/{device_name}/show version")

        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 2

        assert resp_data["results"][0]["command"] == "show version"
        assert resp_data["results"][0]["data_type"] == "ntc_templates"
        assert resp_data["results"][0]["data"] == [{"VERSION": "4.29M"}]
        assert resp_data["results"][0]["model"] == "9400-48p"
        assert resp_data["results"][0]["site"] == "AZ"
        assert resp_data["results"][0]["roles"] == ["datacenter"]

        assert resp_data["results"][1]["command"] == "show version"
        assert resp_data["results"][1]["data_type"] == "raw"
        assert resp_data["results"][1]["data"] == "my raw data"
        assert resp_data["results"][1]["model"] == "9400-48p"
        assert resp_data["results"][1]["site"] == "AZ"
        assert resp_data["results"][1]["roles"] == ["datacenter"]

    def test_get_single_command_404(self, test_client):
        """Validate we get a 404 due to non-existent device."""
        response = test_client.get(f"/api/v1/commands/fake-device01/show version")

        assert response.status_code == 404

    def test_delete_single_command_204(self, test_client, device_name):
        """Validate we get a 204 when deleting a command."""
        response = test_client.delete(f"/api/v1/commands/{device_name}/show version/raw")

        assert response.status_code == 204
        assert response.json()["message"] == f"'show version' was deleted for {device_name}"

    def test_delete_single_command_bad_command_404(self, test_client, device_name):
        """Validate we get a 404 when deleting a command that doesn't exist."""
        response = test_client.delete(f"/api/v1/commands/{device_name}/show versions/raw")

        assert response.status_code == 404
        assert response.json()["message"] == f"'show versions' for {device_name} not found"

    def test_delete_single_command_bad_device_404(self, test_client):
        """Validate we get a 404 when deleting a device that doesn't exist."""
        response = test_client.delete(f"/api/v1/commands/fake-device01/show version/raw")

        assert response.status_code == 404
        assert response.json()["message"] == f"fake-device01 does not exist in devices collection."

    def test_commands_filtering_for_command(self, test_client, device_name):
        """Validate we only get a single command due to filtering."""
        payload = {"command": "show version", "data_type": "raw", "data": "test command filter"}
        payload2 = {"command": "show ip bgp", "data_type": "raw", "data": "my bgp output"}

        response = test_client.post(f"/api/v1/commands/{device_name}/", json=payload)
        assert response.status_code == 201

        response = test_client.post(f"/api/v1/commands/{device_name}/", json=payload2)
        assert response.status_code == 201

        response = test_client.get(f"/api/v1/commands/?command=show version")
        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 2
        assert resp_data["results"][0]["command"] == "show version"
        assert resp_data["results"][0]["data_type"] == "ntc_templates"
        assert resp_data["results"][1]["command"] == "show version"
        assert resp_data["results"][1]["data_type"] == "raw"

    def test_commands_filtering_for_data_type(self, test_client):
        """Validate we only get a single command due to filtering."""
        response = test_client.get(f"/api/v1/commands/?data_type=ntc_templates")
        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["command"] == "show version"
        assert resp_data["results"][0]["data_type"] == "ntc_templates"

    def test_commands_filtering_for_site(self, test_client):
        """Validate we only get a single command due to filtering."""
        response = test_client.get(f"/api/v1/commands/?site=AZ")
        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 4

    def test_commands_filtering_for_model(self, test_client):
        """Validate we only get a single command due to filtering."""
        response = test_client.get(f"/api/v1/commands/?model=9400-48p")
        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 4

    def test_commands_filtering_for_roles(self, test_client):
        """Validate we only get a single command due to filtering."""
        response = test_client.get(f"/api/v1/commands/?roles=datacenter")
        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 4

    def test_device_command_filtering_for_data_type(self, test_client, device_name):
        """Validate we only get a single command due to filtering."""
        response = test_client.get(f"/api/v1/commands/{device_name}/?data_type=ntc_templates")
        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["command"] == "show version"
        assert resp_data["results"][0]["data_type"] == "ntc_templates"

    def test_device_command_filtering_show_version_for_data_type(self, test_client, device_name):
        """Validate we only get a single command due to filtering."""
        response = test_client.get(f"/api/v1/commands/{device_name}/show version/?data_type=ntc_templates")
        assert response.status_code == 200

        resp_data = response.json()
        assert resp_data["count"] == 1
        assert resp_data["results"][0]["command"] == "show version"
        assert resp_data["results"][0]["data_type"] == "ntc_templates"
