// This script all Egyptian movies from Letterboxd
// and saves them to a CSV file.
import puppeteer from "puppeteer";
import {writeFile} from "fs/promises";

const MAX_CONCURRENT_TABS = 5;
const OUTPUT_FILE = "letterboxd_movies.csv";

async function fetchMoviesPage(pageNum, page) {
    const url = `https://letterboxd.com/films/country/egypt/page/${pageNum}/`;

    try {
        await page.goto(url, {waitUntil: "networkidle2"});
        await page.waitForSelector(".film-poster a", {timeout: 10000});

        const links = await page.evaluate(() =>
            [...document.querySelectorAll(".film-poster a")].map(
                (a) => a.href ?? ""
            )
        );
        return links.filter(Boolean);
    } catch (err) {
        console.warn(`Page ${pageNum} failed: ${err.message}`);
        return [];
    }
}

async function main() {
    const browser = await puppeteer.launch({headless: "new"});
    const pages = [];

    for (let i = 0; i < MAX_CONCURRENT_TABS; i++) {
        const page = await browser.newPage();
        await page.setRequestInterception(true);
        page.on("request", (req) => {
            const type = req.resourceType();
            if (["image", "font", "media"].includes(type)) req.abort();
            else req.continue();
        });
        page.setDefaultNavigationTimeout(30000);
        pages.push(page);
    }

    const allMovies = new Set();
    let nextPageToFetch = 1;
    let noResultsCount = 0;
    let done = false;

    async function worker(tab) {
        while (!done) {
            const currentPage = nextPageToFetch++;
            const links = await fetchMoviesPage(currentPage, tab);

            if (links.length === 0) {
                noResultsCount++;
                if (noResultsCount >= 2) done = true;
                break;
            } else {
                noResultsCount = 0;
                links.forEach((url) => allMovies.add(url));
                console.log(
                    `Fetched page ${currentPage}, got ${links.length} links`
                );
            }
        }
    }

    const workers = pages.map((page) => worker(page));
    await Promise.all(workers);

    await Promise.all(pages.map((p) => p.close()));
    await browser.close();

    await writeFile(OUTPUT_FILE, "url\n" + [...allMovies].join("\n"));
    console.log(`Saved ${allMovies.size} unique links to ${OUTPUT_FILE}`);
}

main();
