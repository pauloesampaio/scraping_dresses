from metaflow import FlowSpec, step
import docker


CLIENT = docker.from_env()


class CrawlPipeline(FlowSpec):
    @step
    def start(self):
        print("START")
        self.next(self.build_splash)

    @step
    def build_splash(self):
        CLIENT.images.pull(repository="scrapinghub/splash", tag="latest")
        self.next(self.build_crawler)

    @step
    def build_crawler(self):
        import os
        import pathlib

        current_dir = pathlib.Path(__file__).parent.absolute()
        os.chdir(current_dir)
        CLIENT.images.build(path=".", tag="crawler_image:latest", rm=True)
        self.next(self.start_splash)

    @step
    def start_splash(self):
        CLIENT.containers.run(
            "scrapinghub/splash", detach=True, name="splash", ports={"8050": 8050}
        )
        self.next(self.start_crawler)

    @step
    def start_crawler(self):
        CLIENT.containers.run("crawler_image", name="crawler", links={"splash": None})
        self.next(self.cleanup)

    @step
    def cleanup(self):
        CLIENT.api.stop("splash")
        CLIENT.api.remove_container("splash")
        CLIENT.api.remove_container("crawler")
        self.next(self.end)

    @step
    def end(self):
        print("DONE")


if __name__ == "__main__":
    CrawlPipeline()
