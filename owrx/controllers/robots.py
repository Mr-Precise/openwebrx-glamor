from owrx.controllers import Controller


class RobotsController(Controller):
    def indexAction(self):
        # search engines should not be crawling internal / API routes
        self.send_response(
            """User-agent: *
Disallow: /
""",
            content_type="text/plain",
        )
