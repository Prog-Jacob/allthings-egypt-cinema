// Run this in the browser console.
// Letterboxd page: https://letterboxd.com/films/popular/country/egypt/page/1/

// So far this scraper only works on the first page.
// So you have to run this script manually on each page of the list.

const movies = [...document.querySelectorAll(".film-poster a")].map(a => a.href ?? "");
await navigator.clipboard.writeText(movies.join("\n"));