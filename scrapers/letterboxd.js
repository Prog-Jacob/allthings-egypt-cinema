// Run this in the browser console.
// Letterboxd page: https://letterboxd.com/films/popular/country/egypt/page/1/

// So far this scraper only works on the first page.
// So you have to run this script manually on each page of the list.

// Using firefox, you might need to enable clipboard async access:
//   type `about:config` in the address bar
//   search for `dom.events.testing.asyncClipboard`
//   set it to `true`

const movies = [...document.querySelectorAll(".film-poster a")].map(a => a.href ?? "");
await navigator.clipboard.writeText(movies.join("\n"));