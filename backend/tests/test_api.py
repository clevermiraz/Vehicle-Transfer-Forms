def test_endpoints_require_login(client):
    assert client.get("/api/transfers").status_code == 401
    assert client.get("/api/people/search?q=ab").status_code == 401


def test_wrong_password_rejected(client):
    assert client.post("/api/auth/login", json={"username": "staff", "password": "nope"}).status_code == 401


def test_create_transfer_and_generate_documents(auth_client, sample_payload):
    r = auth_client.post("/api/transfers", json=sample_payload)
    assert r.status_code == 201, r.text
    t = r.json()
    assert t["seller"]["id"] and t["buyer"]["id"] and t["vehicle"]["id"]
    assert t["created_by"] == "Test Staff"

    docs = auth_client.get(f"/api/transfers/{t['id']}/documents").json()
    assert [d["slug"] for d in docs] == ["form-20", "form-21", "form-22", "owner-particulars"]
    assert all(d["error"] is None for d in docs)

    pdf = auth_client.get(f"/api/transfers/{t['id']}/documents/form-22")
    assert pdf.headers["content-type"] == "application/pdf" and pdf.content.startswith(b"%PDF")
    assert "inline" in pdf.headers["content-disposition"]
    assert "attachment" in auth_client.get(f"/api/transfers/{t['id']}/documents/form-22?download=1").headers["content-disposition"]
    assert auth_client.get(f"/api/transfers/{t['id']}/documents/all.zip").content.startswith(b"PK")
    assert auth_client.get(f"/api/transfers/{t['id']}/documents/all.pdf").content.startswith(b"%PDF")
    assert auth_client.get(f"/api/transfers/{t['id']}/documents/nope").status_code == 404


def test_customer_and_vehicle_are_reused(auth_client, sample_payload):
    first = auth_client.post("/api/transfers", json=sample_payload).json()
    # Next sale of the same car: previous buyer is now the seller, found via search.
    found = auth_client.get("/api/people/search", params={"q": "1990123"}).json()
    assert found[0]["name"] == "SHRIMATI KRISHNA RANI DAS"
    vehicle = auth_client.get("/api/vehicles/search", params={"q": "dhaka metro ga 99"}).json()[0]
    payload = {
        **sample_payload,
        "seller": found[0],
        "buyer": {"name": "NEW BUYER", "nid": "5555555555"},
        "vehicle": vehicle,
    }
    second = auth_client.post("/api/transfers", json=payload).json()
    assert second["seller"]["id"] == first["buyer"]["id"]
    assert second["vehicle"]["id"] == first["vehicle"]["id"]


def test_edit_updates_snapshot(auth_client, sample_payload):
    t = auth_client.post("/api/transfers", json=sample_payload).json()
    body = {**t, "sale_price": 650000, "sale_price_words": None}
    updated = auth_client.put(f"/api/transfers/{t['id']}", json=body).json()
    assert updated["sale_price"] == 650000 and updated["sale_price_words"] == "Six Lac Fifty Thousand"
    assert updated["seller"]["id"] == t["seller"]["id"]


def test_search_transfers(auth_client, sample_payload):
    t = auth_client.post("/api/transfers", json=sample_payload).json()
    for q in ("DHAKA", "dhaka metro-ga-99", "1234567890", "+880 1800-000002", "krishna", "rafiqul"):
        ids = [x["id"] for x in auth_client.get("/api/transfers", params={"q": q}).json()]
        assert t["id"] in ids, q
    assert auth_client.get("/api/transfers", params={"q": "no-such-thing"}).json() == []


def test_validation_errors(auth_client, sample_payload):
    bad = {**sample_payload, "seller": {**sample_payload["seller"], "nid": "123"}}
    assert auth_client.post("/api/transfers", json=bad).status_code == 422
    same = {**sample_payload, "buyer": {**sample_payload["buyer"], "nid": sample_payload["seller"]["nid"]}}
    assert auth_client.post("/api/transfers", json=same).status_code == 422


def test_nid_conflict_gives_clear_message(auth_client, sample_payload):
    t = auth_client.post("/api/transfers", json=sample_payload).json()
    # Edit the picked seller record to use the buyer's NID -> conflict, not a crash.
    body = {**t, "seller": {**t["seller"], "nid": t["buyer"]["nid"]}, "buyer": {**t["buyer"], "nid": None}}
    r = auth_client.put(f"/api/transfers/{t['id']}", json=body)
    assert r.status_code == 409 and "NID" in r.json()["detail"]


def test_defaults_use_last_transfer(auth_client, sample_payload):
    auth_client.post("/api/transfers", json=sample_payload)
    d = auth_client.get("/api/transfers/defaults").json()
    assert d["fee_bank_name"] == "SONALI BANK PLC, TEST BRANCH"


def test_staff_cannot_manage_users(auth_client):
    assert auth_client.get("/api/users").status_code == 403
