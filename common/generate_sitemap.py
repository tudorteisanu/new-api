import xml.etree.ElementTree as xml
from datetime import datetime
from settings import app
from urllib.parse import quote
from config import frontendAddress, activeLangs


def generate_sitemap():
    pass
    # xmlStart = '<?xml version="1.0" encoding="UTF-8"?>'
    # root = xml.Element("urlset")
    # root.attrib["xmlns"] = "http://www.sitemaps.org/schemas/sitemap/0.9"
    # dateNow = datetime.now().isoformat().split("T")[0]

    # urls = []

    # news = News.query.filter_by(isBlock=False).with_entities(News.id, News.shortTitle).all()
    # # services = Service.query.with_entities(Service.id, Service.linkText).all()
    # categories = PlantsCategory.query.filter_by(isBlock=False).with_entities(
    #     PlantsCategory.id, PlantsCategory.title
    # ).all()
    # categoriesIds = [item.id for item in categories]

    # products = Plant.query.filter(Plant.isBlock == False, Plant.categoryId.in_(categoriesIds)).with_entities(
    #     Plant.id, Plant.title1, Plant.categoryId
    # ).all()

    # for lang in activeLangs:
    #     urls.extend([
    #         {
    #             "loc": frontendAddress + "/",
    #             "changefreq": "weekly",
    #             "priority": "1"
    #         },
    #         {
    #             "loc": frontendAddress + "/promotions",
    #             "changefreq": "monthly",
    #             "priority": "0.7"
    #         },
    #         {
    #             "loc": frontendAddress + "/about-us",
    #             "changefreq": "weekly",
    #             "priority": "0.4"
    #         },
    #         {
    #             "loc": frontendAddress + "/delivery",
    #             "changefreq": "monthly",
    #             "priority": "0.5"
    #         },
    #         {
    #             "loc": frontendAddress + "/contacts",
    #             "changefreq": "monthly",
    #             "priority": "0.8"
    #         }
    #     ])

    #     for newsItem in news:
    #         urls.append({
    #             "loc": frontendAddress + "/promotions/content/{}/{}".format(str(newsItem.id), quote(newsItem.shortTitle[lang])),
    #             "changefreq": "monthly",
    #             "priority": "0.8"
    #         })

    #     # for servicesItem in services:
    #     #     urls.append({
    #     #         "loc": frontendAddress + "/{}/home/services/{}/{}".format(lang, str(servicesItem.id), quote(servicesItem.linkText[lang])),
    #     #         "changefreq": "monthly",
    #     #         "priority": "0.9"
    #     #     })

    #     for category in categories:
    #         urls.append({
    #             "loc": frontendAddress + "/category/{}/{}".format(str(category.id), quote(category.title[lang])),
    #             "changefreq": "weekly",
    #             "priority": "0.9"
    #         })

    #     for product in products:
    #         urls.append({
    #             "loc": frontendAddress + "/product/{}/{}".format(
    #                 product.id, product.title1[lang]
    #             ),
    #             "changefreq": "weekly",
    #             "priority": "0.9"
    #         })

    # for url in urls:
    #     urlXml = xml.Element("url")
    #     loc = xml.SubElement(urlXml, "loc")
    #     loc.text = url["loc"]
    #     changefreq = xml.SubElement(urlXml, "changefreq")
    #     changefreq.text = url["changefreq"]
    #     priority = xml.SubElement(urlXml, "priority")
    #     priority.text = url["priority"]
    #     lastmod = xml.SubElement(urlXml, "lastmod")
    #     lastmod.text = dateNow
    #     root.append(urlXml)

    # with open("static/sitemap.xml", "w") as f:
    #     f.write(xmlStart + xml.tostring(root).decode("utf-8"))