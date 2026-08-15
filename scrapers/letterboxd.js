// Scrapes all Egyptian movies from Letterboxd.
// Launches a real Chrome window (Cloudflare blocks headless).
// Persistent profile means Cloudflare challenge clears once and sticks.
import puppeteer from "puppeteer";
import {writeFile} from "fs/promises";
import {join, dirname} from "path";
import {fileURLToPath} from "url";

const MAX_CONCURRENT_TABS = 5;
const OUTPUT_FILE = "letterboxd_movies.csv";
const PROFILE_DIR = join(dirname(fileURLToPath(import.meta.url)), ".chrome-profile");

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
    const browser = await puppeteer.launch({
        headless: false,
        userDataDir: PROFILE_DIR,
        args: [
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
        ],
    });

    // Warm-up: load one page first, wait for Cloudflare to clear
    const warmup = await browser.newPage();
    await warmup.evaluateOnNewDocument(() => {
        Object.defineProperty(navigator, "webdriver", {get: () => false});
    });
    await warmup.goto("https://letterboxd.com/films/country/egypt/page/1/", {
        waitUntil: "networkidle2",
    });
    try {
        await warmup.waitForSelector(".film-poster a", {timeout: 30000});
        console.log("Cloudflare cleared, starting scrape...");
    } catch {
        console.log("Solve the Cloudflare challenge in the browser window, then press Enter here.");
        await new Promise((r) => process.stdin.once("data", r));
    }
    await warmup.close();

    const pages = [];
    for (let i = 0; i < MAX_CONCURRENT_TABS; i++) {
        const page = await browser.newPage();
        await page.evaluateOnNewDocument(() => {
            Object.defineProperty(navigator, "webdriver", {get: () => false});
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
