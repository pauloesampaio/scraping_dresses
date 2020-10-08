# Scraping dresses

Web scraping with [scrapy](https://scrapy.org/), [splash](https://github.com/scrapinghub/splash), [docker](https://www.docker.com/) and [MongoDB](https://www.mongodb.com/)

Scraping the dresses category from a [retailer website](https://www.lojasrenner.com.br/) and getting:

- Product id
- Product url
- Product name
- Product price
- Url of all available images
- Crawl timestamp

Storing these on MongoDB cloud. Overwriting if product_id already on the database.

## Setting up

So you need to have a MongoDB cloud account (free tier is all you need) and have your credentials set on the `./credentials/credentials.json` file. I save and example there to help you

## Running

The retailer website uses javascript, so we are using Splash to mimic a browser behavior.
As we all love docker, running on 2 containers:

- Splash: Build from the official splash image from [scrapinghub/splash](https://hub.docker.com/r/scrapinghub/splash)
- Crawler: Minimal build with scrapy and pymongo

To run:

```bash
docker-compose up --exit-code-from crawler
```

And after is done you should be able to go to MongoDB cloud and see your results there.

## Contact

If you have any comments/questions, you can find me [here](https://pauloesampaio.github.io)