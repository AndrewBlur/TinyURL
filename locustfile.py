r"""A beginner-friendly load test for the TinyURL API.

Run the service first, then start Locust with:
    .venv\Scripts\python -m pip install -r requirements-dev.txt
    .venv\Scripts\python -m locust -f locustfile.py --host http://localhost:8000

Open http://localhost:8089 and begin with 10 users and a spawn rate of 2.
"""

from locust import HttpUser, between, task


class TinyUrlUser(HttpUser):
    # A short wait makes this closer to people using a site than an endless loop.
    wait_time = between(0.5, 1.5)

    @task(4)
    def redirect_an_existing_link(self):
        # The first link created by the current app uses the code "1".
        # Change this if your database does not contain that code.
        self.client.get("/1", name="GET /{short_code}", allow_redirects=False)

    @task(1)
    def create_a_link(self):
        self.client.post(
            "/shorten",
            json={"url": "https://example.com/load-test"},
            name="POST /shorten",
        )
