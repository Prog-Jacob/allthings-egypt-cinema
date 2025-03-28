// Run this in the browser console.
// IMDb page: https://www.imdb.com/search/title/?title_type=feature,tv_series,short,tv_miniseries,tv_movie,tv_special,tv_short,video&countries=EG&sort=year,asc


// Load More entries on IMDb page
async function clickLoadMore(times) {
    for (let i = 0; i < times; i++) {
        await new Promise(resolve => setTimeout(resolve, 3000));
        const btn = document.querySelector('button.ipc-btn--single-padding:nth-child(1)');
        
        if (btn) {
            btn.click();
            console.log(`Clicked ${i + 1} time(s)...`);
        } else {
            console.log('No more button found.');
            break;
        }
    }
}


// Scrape Movie Data from the IMDb Page
const movies = [...document.querySelectorAll(".ipc-metadata-list-summary-item")].map((film) => {
	let title = `${film.querySelector(".ipc-title__text").innerHTML.split(".").slice(1).join(".").trim()}`;
	let idMatch = (film.querySelector(".ipc-lockup-overlay")?.href ?? "").match(/title\/(tt\d+?)\//);
	let year = (film.querySelector(".sc-f30335b4-7")?.innerHTML ?? "").trim().slice(0, 4);
	title = title.indexOf(",") != -1 ? `"${title.replace('"', '\"')}"` : title;
	let id = idMatch ? idMatch[1] : "";
	return [id, title, year].join(",");
});


await navigator.clipboard.writeText(movies.join("\n"));

