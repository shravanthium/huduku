def test_main_page(app, client):
    response = app.get("/", follow_redirects=True)
    assert response.status_code == 200
